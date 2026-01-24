#pragma once

#include "../nasa_base.h"
#include "../nasa_controller.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include <functional>

namespace esphome {
namespace samsung_nasa {

class NASA_TextSensor : public text_sensor::TextSensor, public NASA_Base {
 public:
  inline NASA_TextSensor(const std::string label, const uint16_t message, const ControllerMode nasa_mode,
                         const NASA_Device *device)
      : NASA_Base(label, message, nasa_mode, device) {};

  void on_receive(long value) override;
  void set_parent(NASA_Controller *controller);

  // Method to receive the lambda generated in text_sensor.py
  void set_lookup_logic(std::function<std::string(long)> &&func) { this->lookup_func_ = std::move(func); }

 protected:
  NASA_Controller *controller_{nullptr};
  std::function<std::string(long)> lookup_func_;
};

}  // namespace samsung_nasa
}  // namespace esphome
