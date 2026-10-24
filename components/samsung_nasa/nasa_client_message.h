#pragma once

#include <vector>
#include <string>

namespace esphome {
namespace samsung_nasa {

enum MessageSetType : uint8_t { Enum = 0, Variable = 1, LongVariable = 2, Structure = 3 };

struct Buffer {
  uint8_t size;
  uint8_t data[255];
};

struct MessageSet {
  uint16_t messageNumber;
  MessageSetType type = Enum;
  union {
    long value;
    Buffer structure;
  };
  uint16_t size = 2;
  MessageSet(uint16_t messageNumber) {
    this->messageNumber = messageNumber;
    this->type = (MessageSetType) (((uint32_t) messageNumber & 1536) >> 9);
  };
  static MessageSet decode(std::vector<uint8_t> &data, unsigned int index, int capacity, unsigned int packet_end);
  void encode(std::vector<uint8_t> &data);
  std::string to_string();
};

}  // namespace samsung_nasa
}  // namespace esphome