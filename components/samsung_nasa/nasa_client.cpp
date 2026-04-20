#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
#include "nasa_client.h"

namespace esphome {
namespace samsung_nasa {

uint16_t silence_interval = 100;
uint16_t retry_interval = 500;
uint8_t min_retries = 1;
uint16_t send_timeout = 4000;

void defaultAddressCallback(std::string address) {};
bool defaultReceiveCallback(std::string source_address, MessageSet &message) { return false; };

log_lines_t log_lines_func = [](const char *tag, const char *line) { ESP_LOGW(tag, line); };

void NASA_Client::setup() {
  if (debug_log_messages) {
    ESP_LOGW(TAG, "NASA Client Setup");
  }
  if (this->flow_control_pin_ != nullptr) {
    this->flow_control_pin_->setup();
  }
  this->dispatcher_.setup();
  this->dispatcher_.register_receive_callback(
      [this](std::vector<uint16_t> messages) { this->publish_from_queue(messages); });
}

void NASA_Client::update() {
  // Waiting for first update before beginning processing data
  if (this->data_processing_init) {
    ESP_LOGCONFIG(TAG, "Data processing starting");
    data_processing_init = false;
  }
}

void NASA_Client::loop() {
  this->dispatcher_.update();
  if (data_processing_init)
    return;
  if (!read_data())
    return;
  if (write_data())
    return;
}

uint16_t NASA_Client::skip_data(int from) {
  return std::find(this->data_.begin() + from, this->data_.end(), 0x32) - this->data_.begin();
}

void NASA_Client::ack_data(uint8_t id) {
  if (!send_queue_.empty()) {
    auto senddata = &send_queue_.front();
    if (senddata->id == id) {
      send_queue_.pop_front();
    }
  }
}

bool NASA_Client::read_data() {
  // Process a maximum number of bytes per tick to prevent WDT resets
  // if there is a massive backlog of data on the RS485 bus.
  const int MAX_BYTES_PER_LOOP = 256; 
  int bytes_read = 0;

  // read as long as there is anything to read, up to the limit
  while (this->available() && bytes_read < MAX_BYTES_PER_LOOP) {
    uint8_t c;
    if (this->read_byte(&c)) {
      this->data_.push_back(c);
    } else {
      // If available() is true but read_byte fails (e.g., framing error),
      // break immediately so we don't get stuck in an infinite loop.
      ESP_LOGW(TAG, "Failed to read byte from UART; flushing to prevent loop.");
      this->flush(); //  Clears the corrupted UART buffer
      break;
    }
    bytes_read++;
  }

  if (this->data_.empty())
    return true;

  const uint32_t now = millis();
  auto result = process_data();
  
  if (result.type == DecodeResultType::Fill)
    return false;
    
  if (result.type == DecodeResultType::Discard) {
    if (result.bytes == this->data_.size() && now - this->last_transmission_ < 1000)
      return false;
  }
  
  if (result.bytes == this->data_.size()) {
    this->data_.clear();
  } else {
    std::move(this->data_.begin() + result.bytes, this->data_.end(), this->data_.begin());
    this->data_.resize(this->data_.size() - result.bytes);
  }
  
  this->last_transmission_ = now;
  return false;
}

bool NASA_Client::write_data() {
  if (send_queue_.empty())
    return false;
  auto senddata = &send_queue_.front();
  const uint32_t now = millis();
  if (senddata->timeout <= now && senddata->retries >= min_retries) {
    ESP_LOGW(TAG, "Packet sending timeout %d after %d retries", senddata->id, senddata->retries);
    send_queue_.pop_front();
    return true;
  }
  if (now - this->last_transmission_ > silence_interval && senddata->nextRetry < now) {
    if (senddata->nextRetry > 0) {
      ESP_LOGW(TAG, "Retry sending packet %d", senddata->id);
      senddata->retries++;
    }
    this->last_transmission_ = now;
    senddata->nextRetry = now + retry_interval;
    this->before_write();
    this->write_array(senddata->data);
    this->flush();
    this->after_write();
  }
  return true;
}

void NASA_Client::before_write() {
  if (this->flow_control_pin_ != nullptr) {
    ESP_LOGD(TAG, "Switching flow_control_pin to write");
    this->flow_control_pin_->digital_write(true);
  }
}

void NASA_Client::after_write() {
  if (this->flow_control_pin_ != nullptr) {
    ESP_LOGD(TAG, "switching flow_control_pin to read");
    this->flow_control_pin_->digital_write(false);
  }
}

DecodeResult NASA_Client::process_data() {
  if (*this->data_.begin() != 0x32)
    return {DecodeResultType::Discard, skip_data(0)};
  DecodeResult result = {DecodeResultType::Fill, 0};
  result = this->packet_.decode(this->data_);
  if (result.type == DecodeResultType::Processed) {
    this->process_nasa_packet();
  }
  if (result.type == DecodeResultType::Discard) {
    return {DecodeResultType::Discard, this->skip_data(1)};
  }
  return result;
}

void NASA_Client::process_nasa_packet() {
  const auto source = this->packet_.sa.to_string();
  const auto dest = this->packet_.da.to_string();
  const auto me = Address::get_my_address().to_string();
  // Invoke the address callback
  this->addressFunc_(source);
  switch (this->packet_.command.dataType) {
    case DataType::Undefined: {
      return;
    }
    case DataType::Ack: {
      this->packet_.log_multiline(std::string("Ack"), log_lines_func);
      if (dest == me) {
        this->ack_data(this->packet_.command.packetNumber);
        ESP_LOGW(TAG, "Internal request (packet id %d) acknowledged", this->packet_.command.packetNumber);
      } else {
        ESP_LOGW(TAG, "External request (packet id %d) acknowledged", this->packet_.command.packetNumber);
      }
      return;
    }
    case DataType::Request: {
      this->packet_.log_multiline(std::string("Request"), log_lines_func);
      return;
    }
    case DataType::Response: {
      this->packet_.log_multiline(std::string("Response"), log_lines_func);
      // Response type has no ACK so log it and call ack_data to remove from outgoing queue
      if (dest == me) {
        this->ack_data(this->packet_.command.packetNumber);
        break;
      } else {
        return;
      }
    }
    case DataType::Write: {
      this->packet_.log_multiline(std::string("Write"), log_lines_func);
      return;
    }
    case DataType::Nack: {
      this->packet_.log_multiline(std::string("Nack"), log_lines_func);
      return;
    }
    case DataType::Read: {
      this->packet_.log_multiline(std::string("Read"), log_lines_func);
      return;
    }
    case DataType::Notification: {
      break;
    }
  }
  for (auto &message : this->packet_.messages) {
    this->process_messageset(source, dest, message);
  }
}

void NASA_Client::process_messageset(std::string source, std::string dest, MessageSet &message) {
  // Invoike the message received callback
  auto result = this->receiveFunc_(source, message);
  if (debug_log_messages && result) {
    ESP_LOGW(TAG, "Src:%s Dst:%s 0x%X = %ld", source.c_str(), dest.c_str(), message.messageNumber, message.value);
  } else if (debug_log_undefined_messages && !result) {
    ESP_LOGW(TAG, "Undefined s:%s d:%s %s", source.c_str(), dest.c_str(), message.to_string().c_str());
  }
}

// Dont directly publish - use  batched dispatcher
void NASA_Client::publish_read(const std::vector<uint16_t> &messages) { this->dispatcher_.push(messages); }

void NASA_Client::publish_from_queue(std::vector<uint16_t> &messages) {
  Address destAddress = Address::get_broadcast_address();
  Packet packet = Packet::create_partial(destAddress, DataType::Read);
  for (const auto &message : messages) {
    MessageSet request(message);
    request.value = 0;
    packet.messages.push_back(request);
  }
  if (packet.messages.size() == 0)
    return;
  packet.log_multiline(std::string("Read"), log_lines_func);
  this->publish_data(packet.command.packetNumber, packet.encode());
}

void NASA_Client::publish_request(const std::string &address, uint16_t message, long value) {
  Packet packet = Packet::create_partial(Address::parse(address), DataType::Request);
  MessageSet message_set(message);
  message_set.value = value;
  packet.messages.push_back(message_set);
  if (packet.messages.size() == 0)
    return;
  packet.log_multiline(std::string("Request"), log_lines_func);
  this->publish_data(packet.command.packetNumber, packet.encode());
  // Issue a read to confirm command was successful
  this->dispatcher_.push(message);
}

void NASA_Client::dump_config() {
  ESP_LOGCONFIG(TAG, "NASA Controller:");
  LOG_PIN("  Flow Control Pin: ", this->flow_control_pin_);
}

void NASA_Client::publish_data(uint8_t id, std::vector<uint8_t> &&data) {
  const uint32_t now = millis();
  if (id == 0) {
    last_transmission_ = now;
    this->before_write();
    this->write_array(data);
    this->flush();
    this->after_write();
    return;
  }
  OutgoingData outData;
  outData.id = id;
  outData.data = std::move(data);
  outData.nextRetry = 0;
  outData.retries = 0;
  outData.timeout = now + send_timeout;
  send_queue_.push_back(std::move(outData));
}

}  // namespace samsung_nasa
}  // namespace esphome