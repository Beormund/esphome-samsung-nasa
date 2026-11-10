#include "nasa_address.h"

namespace esphome {
namespace samsung_nasa {

Address Address::parse(const std::string &str) {
  Address address;
  char *pEnd;
  address.klass = (AddressClass) strtol(str.c_str(), &pEnd, 16);
  pEnd++;  // .
  address.channel = strtol(pEnd, &pEnd, 16);
  pEnd++;  // .
  address.address = strtol(pEnd, &pEnd, 16);
  return address;
}

// Source address of this component, 80.ff.00 unless source_address is configured
static Address my_address = Address::parse("80.ff.00");

Address Address::get_my_address() { return my_address; }

void Address::set_my_address(const std::string &str) { my_address = Address::parse(str); }

Address Address::get_broadcast_address() {
  Address address;
  address.klass = AddressClass::ADDRESS_CLASS_BROADCAST_SET_LAYER;
  address.channel = 0x00;
  address.address = 0x20;
  return address;
}

void Address::decode(std::vector<uint8_t> &data, unsigned int index) {
  klass = (AddressClass) data[index];
  this->channel = data[index + 1];
  this->address = data[index + 2];
}

void Address::encode(std::vector<uint8_t> &data) {
  data.push_back((uint8_t) klass);
  data.push_back(channel);
  data.push_back(address);
}

std::string Address::to_string() {
  char str[9];
  sprintf(str, "%02x.%02x.%02x", (uint8_t) klass, (uint8_t) channel, (uint8_t) address);
  return std::string(str);
}

}  // namespace samsung_nasa
}  // namespace esphome
