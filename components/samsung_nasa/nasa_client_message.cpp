#include "nasa.h"
#include "nasa_client_message.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome {
namespace samsung_nasa {

MessageSet MessageSet::decode(std::vector<uint8_t> &data, unsigned int index, int capacity) {
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
      set.size = data.size() - index - 3;  // 3=end bytes
      buffer.size = set.size - 2;
      for (int i = 0; i < buffer.size; i++) {
        buffer.data[i] = data[i];
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
  char buf[64];
  switch (type) {
    case Enum:
      snprintf(buf, sizeof(buf), "Enum %04X = %ld", messageNumber, value);
      return std::string(buf);
    case Variable:
      snprintf(buf, sizeof(buf), "Variable %04X = %ld", messageNumber, value);
      return std::string(buf);
    case LongVariable:
      snprintf(buf, sizeof(buf), "LongVariable %04X = %ld", messageNumber, value);
      return std::string(buf);
    case Structure:
      snprintf(buf, sizeof(buf), "Structure %04X = %zu", messageNumber, structure.size);
      return std::string(buf);
    default:
      return "Unknown";
  }
}


}  // namespace samsung_nasa
}  // namespace esphome
