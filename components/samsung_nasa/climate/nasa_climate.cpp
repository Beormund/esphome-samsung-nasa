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
    this->select_presets_->add_on_state_callback([this](size_t index) {
      auto state = this->select_presets_->traits.get_options()[index];
      this->on_preset_select(state, index);
    });
  }
  if (this->mode_select_ != nullptr) {
    this->mode_select_->add_on_state_callback([this](size_t index) {
      auto value = this->mode_select_->traits.get_options()[index];
      climate::ClimateMode new_mode;
      if (value == "Heat")
        new_mode = climate::CLIMATE_MODE_HEAT;
      else if (value == "Cool")
        new_mode = climate::CLIMATE_MODE_COOL;
      else if (value == "Dry")
        new_mode = climate::CLIMATE_MODE_DRY;
      else if (value == "Fan")
        new_mode = climate::CLIMATE_MODE_FAN_ONLY;
      else if (value == "Auto")
        new_mode = climate::CLIMATE_MODE_HEAT_COOL;
      else
        return;  // Unknown mode

      if (this->mode == climate::CLIMATE_MODE_OFF) {
        // If the unit is OFF, just remember this mode for next time it turns ON
        this->last_active_mode_ = new_mode;
      } else {
        // If the unit is ON, update the actual state
        this->on_mode_select(new_mode);
      }
    });
  }
}

void NASA_Climate::on_power(bool state) {
  if (state) {
    // 1. Power turned ON. 
    // If the UI currently says OFF, restore the last known working mode.
    if (this->mode == climate::CLIMATE_MODE_OFF) {
      if (this->update_mode(this->last_active_mode_)) {
        this->publish_state();
      }
    }
  } else {
    // 2. Power turned OFF.
    // First, save what we were doing (Heat, Cool, etc.) BEFORE we switch to OFF.
    if (this->mode != climate::CLIMATE_MODE_OFF) {
      this->last_active_mode_ = this->mode;
    }    
    // Update UI to OFF
    if (this->update_mode(climate::CLIMATE_MODE_OFF)) {
      this->publish_state();
    }
  }
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

void NASA_Climate::on_mode_select(climate::ClimateMode mode) {
    // If we update the mode, we should also update the memory 
    // so the next power toggle stays on this mode.
    if (mode != climate::CLIMATE_MODE_OFF) {
        this->last_active_mode_ = mode;
    }
    if (this->update_mode(mode)) {
        this->publish_state();
    }
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
    climate::ClimateMode new_mode = *call.get_mode();
    auto updated = this->update_mode(new_mode);
    if (this->power_ != nullptr && updated) {
      if (this->mode == climate::ClimateMode::CLIMATE_MODE_OFF) {
        this->power_->turn_off();
      } else {
        this->power_->turn_on();

        if (this->mode_select_ != nullptr) {
          auto call_sel = this->mode_select_->make_call();
          // Map ClimateMode to Select options strings
          if (new_mode == climate::CLIMATE_MODE_HEAT)
            call_sel.set_option("Heat");
          else if (new_mode == climate::CLIMATE_MODE_COOL)
            call_sel.set_option("Cool");
          else if (new_mode == climate::CLIMATE_MODE_DRY)
            call_sel.set_option("Dry");
          else if (new_mode == climate::CLIMATE_MODE_FAN_ONLY)
            call_sel.set_option("Fan");
          else if (new_mode == climate::CLIMATE_MODE_HEAT_COOL)
            call_sel.set_option("Auto");
          call_sel.perform();
        }
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

bool NASA_Climate::update_custom_preset(const char *new_value) { return this->set_custom_preset_(new_value); }

climate::ClimateTraits NASA_Climate::traits() {
  climate::ClimateTraits traits{};
  traits.add_feature_flags(climate::CLIMATE_SUPPORTS_CURRENT_TEMPERATURE);
  traits.add_feature_flags(climate::CLIMATE_SUPPORTS_ACTION);

  if (this->supported_modes_.empty()) {
    // Default fallback
    traits.set_supported_modes({climate::CLIMATE_MODE_OFF, climate::CLIMATE_MODE_HEAT});
  } else {
    traits.add_supported_mode(climate::CLIMATE_MODE_OFF);
    for (auto mode : this->supported_modes_) {
      traits.add_supported_mode(mode);
    }
  }

  traits.set_supported_presets({});
  if (this->select_presets_ != nullptr) {
    const auto &options = this->select_presets_->traits.get_options();
    std::vector<const char *> preset_pointers(options.begin(), options.end());
    traits.set_supported_custom_presets(preset_pointers);
  }
  return traits;
}

}  // namespace samsung_nasa
}  // namespace esphome
