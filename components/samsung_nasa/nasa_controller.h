#pragma once

#include "esphome/core/component.h"
#include "nasa.h"
#include "nasa_base.h"
#include "nasa_client.h"
#include <map>
#include <set>
#include <vector>

namespace esphome {
namespace samsung_nasa {


class NASA_Device {
 public:
  NASA_Device(std::string address, uint8_t address_class) : address_{address}, address_class_{address_class} {};
  auto get_address() { return this->address_; };
  auto get_address_class() { return this->address_class_; };

 protected:
  std::string address_;         // E.g. "20.00.00"
  AddressClass address_class_;  // E.g. 0x20
};

class NASA_Controller : public PollingComponent {
 public:
  NASA_Controller(NASA_Client *nasa_client) : nasa_client_{nasa_client} {};
  void setup() override;
  void update() override;
  void write(const std::string address, uint16_t number, long value);
  void read(const std::vector<uint16_t> &numbers);
  void register_device(NASA_Device *device);
  void register_component(NASA_Base *component);
  void set_debug_log_messages(bool value) { debug_log_messages = value; }
  void set_debug_log_messages_raw(bool value) { debug_log_raw_bytes = value; }
  void set_debug_log_undefined_messages(bool value) { debug_log_undefined_messages = value; }
  void register_address(const std::string address) { addresses_.insert(address); }

 protected:
  std::map<std::string, NASA_Device *> devices_;
  std::set<std::string> addresses_;
  std::map<uint16_t, std::vector<NASA_Base *>> components_;
  NASA_Client *nasa_client_;
};

}  // namespace samsung_nasa
}  // namespace esphome