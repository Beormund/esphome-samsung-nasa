#include "nasa_switch.h"

namespace esphome {
namespace samsung_nasa {

void NASA_Switch::write_state(bool value) {
  this->publish_state(value);
  this->write(this->lambda_to_(value));
};

void NASA_Switch::on_receive(long value) {
  auto new_state = this->lambda_from_(value);
  // Switch::publish_state() does not set has_state, so has_state() would stay false in lambdas forever
  this->set_has_state(true);
  this->publish_state(new_state);
}

void NASA_Switch::write(long value) {
  this->controller_->write(this->get_address(), this->get_message(), value);
}

void NASA_Switch::set_lambdas(lambda_from lamda_from, lambda_to lambda_to) {
  this->lambda_from_ = lamda_from;
  this->lambda_to_ = lambda_to;
}

void NASA_Switch::set_parent(NASA_Controller *controller) { this->controller_ = controller; };

}  // namespace samsung_nasa
}  // namespace esphome