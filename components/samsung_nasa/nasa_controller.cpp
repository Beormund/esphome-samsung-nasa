#include <algorithm>
#include <cstdio>
#include "esphome/core/log.h"
#include "esphome/core/application.h"
#include "nasa_controller.h"
#include "vector"
#include "nasa.h"

namespace esphome {
namespace samsung_nasa {

bool debug_log_raw_bytes = false;
bool debug_log_undefined_messages = false;
bool debug_log_messages = false;
uint32_t diag_session = 0;
uint32_t diag_rx_seq = 0;
uint32_t diag_ok = 0, diag_err_size = 0, diag_err_end = 0, diag_err_crc = 0, diag_err_uart = 0;

// Unmodified packet bytes in numbered parts, so no log line exceeds typical syslog/API line limits:
// RAW s=<session> n=<receive number> <kind> len=<bytes> p=<part>/<parts> <hex>
void diag_log_raw(const char *kind, const uint8_t *data, size_t len) {
  static const size_t PART = 160;
  const size_t parts = len == 0 ? 1 : (len + PART - 1) / PART;
  char hex[2 * PART + 1];
  for (size_t p = 0; p < parts; p++) {
    const size_t from = p * PART, n = std::min(PART, len - from);
    for (size_t i = 0; i < n; i++)
      snprintf(hex + 2 * i, 3, "%02X", data[from + i]);
    hex[2 * n] = 0;
    ESP_LOGW(TAG, "RAW s=%08X n=%u %s len=%u p=%u/%u %s", (unsigned) diag_session, (unsigned) diag_rx_seq, kind,
             (unsigned) len, (unsigned) (p + 1), (unsigned) parts, hex);
  }
}

void NASA_Controller::setup() {
  // register callbacks with NASA_Client
  this->nasa_client_->register_address_callback([this](std::string address) { this->register_address(address); });
  this->nasa_client_->register_receive_callback([this](std::string source_address, MessageSet &message) -> bool {
    auto result = false;
    auto it = this->components_.find(message.messageNumber);
    if (it != this->components_.end()) {
      auto components = it->second;
      for (auto const &component : components) {
        auto device_address = component->get_address();
        if (source_address == device_address) {
          if (message.type == Structure)
            component->on_receive_structure(message.structure.data, message.structure.size);
          else
            component->on_receive(message.value);
          result = true;
        }
      }
    }
    return result;
  });
  // Do an initial read request for all registered components
  std::vector<uint16_t> numbers;
  for (auto const &pair : this->components_) {
    numbers.push_back(pair.first);
  }
  this->read(numbers);
}

void NASA_Controller::register_device(NASA_Device *device) { this->devices_.emplace(device->get_address(), device); }

void NASA_Controller::register_component(NASA_Base *component) {
  auto message = component->get_message();
  if (this->components_.contains(message)) {
    this->components_[message].push_back(component);
  } else {
    this->components_[message] = {component};
  }
}

void NASA_Controller::read(const std::vector<uint16_t> &numbers) { this->nasa_client_->publish_read(numbers); }

void NASA_Controller::send_structure(const std::string &address, uint16_t number, uint8_t type,
                                    const std::vector<uint8_t> &payload) {
  this->nasa_client_->publish_structure(address, number, (DataType) type, payload);
}

void NASA_Controller::write(const std::string &address, const uint16_t &number, long value) {
  this->nasa_client_->publish_request(address, number, value);
}

void NASA_Controller::update() {
  if (debug_log_messages) {
    ESP_LOGW(TAG, "NASA controller update");
  }

  ESP_LOGCONFIG(TAG, "Configured devices:");
  for (const auto &pair : devices_) {
    auto address = pair.first;
    auto address_class = pair.second->get_address_class();
    auto it = AddressClass_Labels.find(address_class);
    auto label = (it != AddressClass_Labels.end()) ? it->second : "Other";
    ESP_LOGCONFIG(TAG, "* %s: %s", label.c_str(), address.c_str());
  }

  ESP_LOGCONFIG(TAG, "Discovered devices:");
  for (const auto &address : addresses_) {
    auto addr = Address::parse(address);
    auto address_class = addr.klass;
    auto it = AddressClass_Labels.find(address_class);
    auto label = (it != AddressClass_Labels.end()) ? it->second : "Other";
    ESP_LOGCONFIG(TAG, "* %s: %s", label.c_str(), address.c_str());
  }
}

}  // namespace samsung_nasa
}  // namespace esphome
