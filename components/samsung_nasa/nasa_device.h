#pragma once

#include "nasa.h"
#include <string>

namespace esphome {
namespace samsung_nasa {

class NASA_Device {
 public:
  NASA_Device(const std::string address, const AddressClass address_class)
      : address_{address}, address_class_{address_class} {};
  const std::string get_address() const { return this->address_; };
  AddressClass get_address_class() const { return this->address_class_; };

 protected:
  const std::string address_;         // E.g. "20.00.00"
  const AddressClass address_class_;  // E.g. 0x20
};

}  // namespace samsung_nasa
}  // namespace esphome