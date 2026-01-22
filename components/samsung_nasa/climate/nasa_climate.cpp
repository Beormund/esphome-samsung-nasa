#include "nasa_climate.h"
#include "../nasa.h"
#include "esphome/components/climate/climate.h"
#include "esphome/core/log.h"
#include <vector>

namespace esphome {
namespace samsung_nasa {

void NASA_Climate::setup() {
  if (this->power_ != nullptr) {
    this->power_->add_on_state_callback([this](bool state) { this->on_power(state); });
  }
  if (this->target_temp_ != nullptr) {
    this->target_temp_->add_on_state_callback([this](float state) { this->on_target_temp(state); });
  }
  if (this->current_temp_ != nullptr) {
    this->current_temp_->add_on_state_callback([this](float state) { this->on_current_temp(state); });
  }
  if (this->action_sens_ != nullptr && this->mappings_ != nullptr) {
    this->action_sens_->add_on_state_callback([this](float state) { this->on_action_sens(state); });
  }
  if (this->select_presets_ != nullptr) {
    this->select_presets_->add_on_state_callback(
        [this](size_t index) { 
            auto state = this->select_presets_->traits.get_options()[index];
            this->on_preset_select(state, index); 
        });
  }
}

void NASA_Climate::on_power(bool state) {
  auto new_mode = state ? climate::ClimateMode::CLIMATE_MODE_HEAT : climate::ClimateMode::CLIMATE_MODE_OFF;
  if (this->update_mode(new_mode))
    this->publish_state();
}

void NASA_Climate::on_target_temp(float state) {
  if (this->update_target_temp(state))
    this->publish_state();
}

void NASA_Climate::on_current_temp(float state) {
  if (this->update_current_temp(state))
    this->publish_state();
}

void NASA_Climate::on_preset_select(std::string state, size_t index) {
  if (this->update_custom_preset(state.c_str()))
    this->publish_state();
}

void NASA_Climate::on_action_sens(float state) {
  if (this->mappings_ == nullptr)
    return;
  for (auto const &[key, value] : this->mappings_->get_map()) {
    if (static_cast<int>(state) == key) {
      if (this->update_action(value))
        this->publish_state();
      break;
    }
  }
}

void NASA_Climate::control(const climate::ClimateCall &call) {
  auto update = false;
  if (call.get_mode().has_value()) {
    auto updated = this->update_mode(*call.get_mode());
    if (this->power_ != nullptr && updated) {
      if (this->mode == climate::ClimateMode::CLIMATE_MODE_OFF) {
        this->power_->turn_off();
      } else if (this->mode == climate::ClimateMode::CLIMATE_MODE_HEAT) {
        this->power_->turn_on();
      }
      update = true;
    }
  }
  if (call.get_target_temperature().has_value()) {
    auto updated = this->update_target_temp(*call.get_target_temperature());
    if (this->target_temp_ != nullptr && updated) {
      auto call = this->target_temp_->make_call();
      call.set_value(this->target_temperature);
      call.perform();
      update = true;
    }
  }
  if (call.has_custom_preset()) {
    auto updated = this->update_custom_preset(call.get_custom_preset().c_str());
    if (this->select_presets_ != nullptr && updated) {
      auto call = this->select_presets_->make_call();
      call.set_option(this->get_custom_preset().c_str());
      call.perform();
      this->preset.reset();
      update = true;
    }
  }
  if (update)
    this->publish_state();
}

bool NASA_Climate::update_action(climate::ClimateAction new_action) {
  if (this->action != new_action) {
    this->action = new_action;
    return true;
  }
  return false;
}

bool NASA_Climate::update_mode(climate::ClimateMode new_mode) {
  if (this->mode != new_mode) {
    this->mode = new_mode;
    return true;
  }
  return false;
}

bool NASA_Climate::update_current_temp(float new_temp) {
  if (this->current_temperature != new_temp) {
    this->current_temperature = new_temp;
    return true;
  }
  return false;
}

bool NASA_Climate::update_target_temp(float new_temp) {
  if (this->target_temperature != new_temp) {
    this->target_temperature = new_temp;
    return true;
  }
  return false;
}

bool NASA_Climate::update_custom_preset(const char *new_value) {
    return this->set_custom_preset_(new_value);
}

climate::ClimateTraits NASA_Climate::traits() {
  climate::ClimateTraits traits{};
  traits.add_feature_flags(climate::CLIMATE_SUPPORTS_CURRENT_TEMPERATURE);
  traits.add_feature_flags(climate::CLIMATE_SUPPORTS_ACTION);
  traits.set_supported_modes({climate::CLIMATE_MODE_OFF, climate::CLIMATE_MODE_HEAT});
  traits.set_supported_presets({});
  if (this->select_presets_ != nullptr) {
    std::vector<const char *> preset_pointers;    
    const auto &options = this->select_presets_->traits.get_options();    
    for (const std::string &option : options) {
      preset_pointers.push_back(option.c_str());
    }    
    traits.set_supported_custom_presets(preset_pointers);
  }
  return traits;
}

}  // namespace samsung_nasa
}  // namespace esphome