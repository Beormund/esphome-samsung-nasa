#include "nasa_sensor.h"

namespace esphome {
namespace samsung_nasa {

void NASA_Sensor::on_receive(long value) {
  auto new_value = static_cast<float>(value);
  this->publish_state(new_value);
}

void NASA_Sensor::set_parent(NASA_Controller *controller) { this->controller_ = controller; }

}  // namespace samsung_nasa
}  // namespace esphome