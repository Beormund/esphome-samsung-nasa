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
  void on_receive_structure(const uint8_t *data, uint8_t size) override;
  // 0 = text if printable, else hex (default), 1 = Samsung part number with date "DB91-02103B 231108",
  // 2 = product option "[0]12300-[1]10000-[2]00000-[3]00002"
  void set_structure_format(uint8_t format) { this->structure_format_ = format; }
  void set_parent(NASA_Controller *controller);

  // Method to receive the lambda generated in text_sensor.py
  void set_lookup_logic(std::function<std::string(long)> &&func) { this->lookup_func_ = std::move(func); }

 protected:
  NASA_Controller *controller_{nullptr};
  std::function<std::string(long)> lookup_func_;
  long last_numeric_value_ = -1; // Sentinel value
  std::string last_structure_;
  uint8_t structure_format_{0};
};

}  // namespace samsung_nasa
}  // namespace esphome
