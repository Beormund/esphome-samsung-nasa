#pragma once

#include <string>
#include "nasa.h"

namespace esphome {
namespace samsung_nasa {

enum class ControllerMode : uint8_t;
class NASA_Device;

class NASA_Base {
 public:
  NASA_Base(const std::string label, const uint16_t message, const ControllerMode nasa_mode, const NASA_Device *device)
      : label_{label}, message_{message}, nasa_mode_{nasa_mode}, device_{device} {};
  const uint16_t get_message() const { return this->message_; }
  const std::string get_label() const { return this->label_; }
  const ControllerMode get_mode() const { return this->nasa_mode_; }
  const NASA_Device* get_device() const { return this->device_; }
  // Must implement in each component type
  virtual void on_receive(long value) = 0;
  // Not all components write (e.g., sensor)
  virtual void write(long value) {};

 protected:
  const std::string label_;
  const uint16_t message_;
  const ControllerMode nasa_mode_;
  const NASA_Device* const device_;
};

}  // namespace samsung_nasa
}  // namespace esphome