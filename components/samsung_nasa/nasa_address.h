#pragma once

#include "nasa.h"
#include <vector>
#include <string>

namespace esphome {
namespace samsung_nasa {

struct Address {
  AddressClass klass;
  uint8_t channel;
  uint8_t address;
  uint8_t size = 3;
  static Address parse(const std::string &str);
  static Address get_my_address();
  static void set_my_address(const std::string &str);
  static Address get_broadcast_address();
  void decode(std::vector<uint8_t> &data, unsigned int index);
  void encode(std::vector<uint8_t> &data);
  std::string to_string();
};

}  // namespace samsung_nasa
}  // namespace esphome
