#include "nasa_text_sensor.h"

namespace esphome {
namespace samsung_nasa {

void NASA_TextSensor::on_receive(long value) {
  // Only process and publish if the numeric value has changed
  if (value != this->last_numeric_value_) {
    if (this->lookup_func_) {
      this->publish_state(this->lookup_func_(value));
    } else {
      this->publish_state(std::to_string(value));
    }
    this->last_numeric_value_ = value;
  }
}

void NASA_TextSensor::set_parent(NASA_Controller *controller) { this->controller_ = controller; }

}  // namespace samsung_nasa
}  // namespace esphome
