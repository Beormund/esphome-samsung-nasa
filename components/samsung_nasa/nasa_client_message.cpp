#include "nasa.h"
#include "nasa_client_message.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome {
namespace samsung_nasa {

MessageSet MessageSet::decode(std::vector<uint8_t> &data, unsigned int index, int capacity, unsigned int packet_end) {
  MessageSet set = MessageSet(((uint32_t) data[index] * 256U + (uint32_t) data[index + 1]));
  switch (set.type) {
    case Enum:
      set.value = (int) data[index + 2];
      set.size = 3;
      break;
    case Variable:
      set.value = (int) data[index + 2] << 8 | (int) data[index + 3];
      set.size = 4;
      break;
    case LongVariable:
      set.value = (int) data[index + 2] << 24 | (int) data[index + 3] << 16 | (int) data[index + 4] << 8 |
                  (int) data[index + 5];
      set.size = 6;
      break;
    case Structure:
      if (capacity != 1) {
        ESP_LOGE(TAG, "structure messages can only have one message but is %d", capacity);
        return set;
      }
      Buffer buffer;
      set.size = (int) packet_end - (int) index - 3;  // 3 = CRC + end byte // use the packet end, not the buffer size: the buffer may already hold the next packet
      if (set.size < 2 || set.size - 2 > (int) sizeof(buffer.data)) {
        ESP_LOGE(TAG, "structure size out of range: %d", set.size);
        buffer.size = 0;
        set.structure = buffer;
        return set;
      }
      buffer.size = set.size - 2;
      for (int i = 0; i < buffer.size; i++) {
        buffer.data[i] = data[index + 2 + i];  // payload starts after the 2-byte message number
      }
      set.structure = buffer;
      break;
    default:
      ESP_LOGE(TAG, "Unkown type");
  }
  return set;
};

void MessageSet::encode(std::vector<uint8_t> &data) {
  data.push_back((uint8_t) (this->messageNumber >> 8) & 0xff);
  data.push_back((uint8_t) (this->messageNumber & 0xff));
  switch (type) {
    case Enum:
      data.push_back((uint8_t) value);
      break;
    case Variable:
      if (value < 0)
        value += 65535;
      data.push_back((uint8_t) (value >> 8) & 0xff);
      data.push_back((uint8_t) (value & 0xff));
      break;
    case LongVariable:
      data.push_back((uint8_t) (value & 0x000000ff));
      data.push_back((uint8_t) ((value & 0x0000ff00) >> 8));
      data.push_back((uint8_t) ((value & 0x00ff0000) >> 16));
      data.push_back((uint8_t) ((value & 0xff000000) >> 24));
      break;
    case Structure:
      for (int i = 0; i < structure.size; i++) {
        data.push_back(structure.data[i]);
      }
      break;
    default:
      ESP_LOGE(TAG, "Unkown type");
  }
}

std::string MessageSet::to_string() {
  switch (type) {
    case Enum:
      return "Enum " + format_hex_pretty(messageNumber, '\0', false) + " = " + std::to_string(value);
    case Variable:
      return "Variable " + format_hex_pretty(messageNumber, '\0', false) + " = " + std::to_string(value);
    case LongVariable:
      return "LongVariable " + format_hex_pretty(messageNumber, '\0', false) + " = " + std::to_string(value);
    case Structure:
      return "Structure " + format_hex_pretty(messageNumber, '\0', false) + " = " + std::to_string(structure.size);
    default:
      return "Unknown";
  }
}

}  // namespace samsung_nasa
}  // namespace esphome
