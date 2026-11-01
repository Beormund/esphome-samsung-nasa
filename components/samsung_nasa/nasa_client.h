#pragma once

#include <vector>
#include <functional>
#include <queue>
#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "nasa.h"
#include "nasa_client_common.h"
#include "nasa_client_message.h"
#include "nasa_client_packet.h"
#include "nasa_limited_queue.h"

namespace esphome {
namespace samsung_nasa {

enum class DataResult;

void defaultAddressCallback(std::string address);
bool defaultReceiveCallback(std::string source_address, MessageSet &message);

struct OutgoingData {
  uint8_t id;
  std::vector<uint8_t> data;
  uint32_t nextRetry;
  uint32_t timeout;
  uint8_t retries;
};

class NASA_Client : public PollingComponent, public uart::UARTDevice {
 public:
  using RegisterAddressFunc = std::function<void(std::string)>;
  using RegisterReceiveFunc = std::function<bool(std::string, MessageSet &)>;

  NASA_Client(uint32_t update_interval) : PollingComponent(update_interval) {};
  float get_setup_priority() const override { return setup_priority::DATA; };
  void setup() override;
  void update() override;
  void loop() override;
  void dump_config() override;
  void publish_read(const std::vector<uint16_t> &messages);
  // Read sent directly to one device instead of the broadcast address
  void publish_read_to(const std::string &address, const std::vector<uint16_t> &messages);
  void publish_from_queue(std::vector<uint16_t> &messages);
  void publish_request(const std::string &address, uint16_t message, long value);
  // Single value message with an explicit data type (e.g. Write instead of Request)
  void publish_value(const std::string &address, uint16_t message, long value, DataType type);
  // Single structure message with a fixed payload to one device (e.g. 0x461E error history, 0x860B pre-error cycle data)
  void publish_structure(const std::string &address, uint16_t message, DataType type, const std::vector<uint8_t> &payload);
  void set_flow_control_pin(GPIOPin *flow_control_pin) { this->flow_control_pin_ = flow_control_pin; }
  void set_silence_interval(uint16_t value) { silence_interval = value; }
  void set_retry_interval(uint16_t value) { retry_interval = value; }
  void set_min_retries(uint8_t value) { min_retries = value; }
  void set_send_timeout(uint16_t value) { send_timeout = value; }
  void register_address_callback(RegisterAddressFunc raf) { this->addressFunc_ = raf; }
  void register_receive_callback(RegisterReceiveFunc rrf) { this->receiveFunc_ = rrf; }

 protected:
  GPIOPin *flow_control_pin_{nullptr};
  std::vector<uint8_t> data_;
  Packet packet_;
  uint32_t last_transmission_ = 0;
  uint16_t skip_data(int from);
  bool data_processing_init = true;
  void process_nasa_packet();
  void ack_data(uint8_t id);
  bool read_data();
  bool write_data();
  void before_write();
  void after_write();
  void publish_data(uint8_t id, std::vector<uint8_t> &&data);
  void process_messageset(std::string source, std::string dest, MessageSet &message);
  DecodeResult process_data();
  RegisterAddressFunc addressFunc_ = defaultAddressCallback;
  RegisterReceiveFunc receiveFunc_ = defaultReceiveCallback;
  // Construct a queue dispatcher that will dispatch messages via a callback
  // 100 = limit to 100 messages, Any more and they will be discarded
  // Batch deliver 10 messages every 200 millisecs. Avoids overloading the bus
  BatchDispatcher<uint16_t> dispatcher_{100, 10, 200};
  std::deque<OutgoingData> send_queue_;

};

}  // namespace samsung_nasa
}  // namespace esphome