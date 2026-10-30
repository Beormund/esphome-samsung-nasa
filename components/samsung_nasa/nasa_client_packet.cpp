#include "nasa_client_packet.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome {
namespace samsung_nasa {

Packet Packet::create_partial(Address da, DataType dataType) {
  Packet packet;
  packet.sa = Address::get_my_address();
  packet.da = da;
  packet.command.packetInformation = true;
  packet.command.packetType = PacketType::Normal;
  packet.command.dataType = dataType;
  packet.command.packetNumber = Packet::get_packet_number();
  return packet;
}

int Packet::packet_counter_ = 0;

int Packet::get_packet_number() { return ++packet_counter_; }

DecodeResult Packet::decode(std::vector<uint8_t> &data) {
  if (data.size() < 4) {
    return {DecodeResultType::Fill};
  }
  // read the length only after the buffer check above (data[1..2] may not exist yet)
  const uint16_t size = (uint16_t) data[1] << 8 | (uint16_t) data[2];
  // shortest valid packet: size(2) + addresses(3+3) + command(3) + capacity(1) + crc(2) + end(1) = 14;
  // anything shorter would make the crc range negative and the header reads go past the packet
  if (size < 14) {
    ESP_LOGW(TAG, "Packet too short: size %u", (unsigned) size);
    return {DecodeResultType::Discard};
  }
  if (size > 1500) {
    char hex_buf_33[512];
    ESP_LOGW(TAG, "Packet exceeds size limits: %s", format_hex_to(hex_buf_33, data));
    return {DecodeResultType::Discard};
  }
  if (size + 2 > data.size())
    return {DecodeResultType::Fill};
  if (data[size + 1] != 0x34) {
    char hex_buf_39[512];
    ESP_LOGW(TAG, "invalid end byte: %s", format_hex_to(hex_buf_39, data));
    return {DecodeResultType::Discard};
  }
  uint16_t crc_actual = crc16be(data.data() + 3, size - 4);
  uint16_t crc_expected = (int) data[size - 1] << 8 | (int) data[size];
  if (crc_expected != crc_actual) {
    char hex_buf_46[512];
    ESP_LOGW(TAG, "NASA: invalid crc - got %d but should be %d: %s", crc_actual, crc_expected,
             format_hex_to(hex_buf_46, data));
    return {DecodeResultType::Discard};
  }
  unsigned int cursor = 3;
  sa.decode(data, cursor);
  cursor += sa.size;
  da.decode(data, cursor);
  cursor += da.size;
  command.decode(data, cursor);
  cursor += command.size;
  int capacity = (int) data[cursor];
  cursor++;
  messages.clear();
  for (int i = 1; i <= capacity; ++i) {
    MessageSet set = MessageSet::decode(data, cursor, capacity, size + 2);
    messages.push_back(set);
    cursor += set.size;
  }
  return {DecodeResultType::Processed, (uint16_t) (size + 2)};
}

std::vector<uint8_t> Packet::encode() {
  std::vector<uint8_t> data;
  data.push_back(0x32);
  data.push_back(0);  // size
  data.push_back(0);  // size
  sa.encode(data);
  da.encode(data);
  command.encode(data);
  data.push_back((uint8_t) messages.size());
  for (int i = 0; i < messages.size(); i++) {
    messages[i].encode(data);
  }
  int endPosition = data.size() + 1;
  data[1] = (uint8_t) (endPosition >> 8);
  data[2] = (uint8_t) (endPosition & (int) 0xFF);
  uint16_t checksum = crc16be(data.data() + 3, endPosition - 4);
  data.push_back((uint8_t) ((unsigned int) checksum >> 8));
  data.push_back((uint8_t) ((unsigned int) checksum & (unsigned int) 0xFF));
  data.push_back(0x34);
  return data;
}

std::vector<std::string> Packet::to_string(optional<std::string> prefix) {
  std::vector<std::string> lines;
  std::string line = prefix ? *prefix + " " : "";
  line += "#Packet Src:" + sa.to_string() + " Dst:" + da.to_string() + " " + command.to_string();
  lines.push_back(line);
  for (int i = 0; i < messages.size(); i++) {
    lines.push_back(" > " + messages[i].to_string());
  }
  return lines;
}

void Packet::log_multiline(optional<std::string> prefix, log_lines_t func) {
  // packet dumps (Read, Write, Request, Response, Ack, Nack) are debug output; without
  // debug_log_messages every poll and every external write would end up as a warning
  if (!debug_log_messages)
    return;
  for (const auto &line : this->to_string(prefix)) {
    func(TAG, line.c_str());
  }
}

}  // namespace samsung_nasa
}  // namespace esphome