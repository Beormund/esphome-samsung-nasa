#pragma once

#include <string>
#include "nasa.h"
#include "nasa_device.h"

namespace esphome {
namespace samsung_nasa {

enum class ControllerMode : uint8_t;

class NASA_Base {
 public:
  inline NASA_Base(const std::string label, const uint16_t message, const ControllerMode nasa_mode,
                   const NASA_Device *device)
      : label_{label}, message_{message}, nasa_mode_{nasa_mode}, device_{device} {};
  virtual ~NASA_Base() {};
  uint16_t get_message() const { return this->message_; }
  const std::string get_label() const { return this->label_; }
  ControllerMode get_mode() const { return this->nasa_mode_; }
  const std::string get_address() const { return this->device_->get_address(); }
  // Must implement in each component type
  virtual void on_receive(long value) = 0;

 protected:
  const std::string label_;
  const uint16_t message_;
  const ControllerMode nasa_mode_;
  const NASA_Device *const device_;
};

class NASA_Write : public NASA_Base {
 public:
  NASA_Write(const std::string label, const uint16_t message, const ControllerMode nasa_mode,
              const NASA_Device *device)
      : NASA_Base(label, message, nasa_mode, device) {};
  // Must implement in reach component type
  virtual void write(long value) = 0;
};

}  // namespace samsung_nasa
}  // namespace esphome