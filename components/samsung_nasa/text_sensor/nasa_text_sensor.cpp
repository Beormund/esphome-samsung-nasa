#include "nasa_text_sensor.h"

namespace esphome {
namespace samsung_nasa {

void NASA_TextSensor::on_receive(long value) {
  if (this->lookup_func_) {
    std::string translated_value = this->lookup_func_(value);
    this->publish_state(translated_value);
  } else {
    // Fallback if no mapping was provided
    this->publish_state(std::to_string(value));
  }
}

void NASA_TextSensor::set_parent(NASA_Controller *controller) { this->controller_ = controller; }

}  // namespace samsung_nasa
}  // namespace esphome
