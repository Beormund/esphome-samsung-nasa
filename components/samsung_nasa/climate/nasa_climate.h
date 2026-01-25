#pragma once

#include "esphome/core/component.h"
#include "esphome/components/climate/climate.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/select/select.h"
#include "esphome/components/number/number.h"
#include "esphome/components/switch/switch.h"
#include <map>
#include <set>

namespace esphome {
namespace samsung_nasa {

using climateActionMap_t = std::map<int, climate::ClimateAction>;

class ClimateActionMap {
 public:
  ClimateActionMap() = default;
  ClimateActionMap(climateActionMap_t cam) : mappings_{cam} {};
  void add_map_entry(int key, climate::ClimateAction value) { mappings_.emplace(key, value); }
  auto get_map() { return this->mappings_; }

 protected:
  climateActionMap_t mappings_;
};

class NASA_Climate : public climate::Climate, public Component {
 public:
  void setup() override;
  climate::ClimateCall make_call() { return climate::ClimateCall(this); }
  void set_power_switch(switch_::Switch *power) { this->power_ = power; };
  void set_target_temp(number::Number *target_temp) { this->target_temp_ = target_temp; };
  void set_current_temp(sensor::Sensor *current_temp) { this->current_temp_ = current_temp; }
  void set_action_sensor(sensor::Sensor *action_sens) { this->action_sens_ = action_sens; }
  void set_action_map(ClimateActionMap *mappings) { this->mappings_ = mappings; }
  void set_custom_preset_select(select::Select *custom_presets) { this->select_presets_ = custom_presets; }
  void set_mode_select(select::Select *mode_select) { this->mode_select_ = mode_select; }
  void set_supported_modes(std::vector<climate::ClimateMode> modes) { 
    this->supported_modes_ = {modes.begin(), modes.end()}; 
  }
  bool update_action(climate::ClimateAction new_action);

 protected:
  void control(const climate::ClimateCall &call) override;
  void on_power(bool state);
  void on_target_temp(float state);
  void on_current_temp(float state);
  void on_action_sens(float state);
  void on_preset_select(std::string state, size_t index);
  void on_mode_select(climate::ClimateMode mode);
  bool update_mode(climate::ClimateMode new_mode);
  bool update_current_temp(float new_temp);
  bool update_target_temp(float new_temp);
  bool update_custom_preset(const char* new_value);
  climate::ClimateTraits traits() override;

  switch_::Switch *power_{nullptr};
  number::Number *target_temp_{nullptr};
  sensor::Sensor *current_temp_{nullptr};
  sensor::Sensor *action_sens_{nullptr};
  select::Select *select_presets_{nullptr};
  select::Select *mode_select_{nullptr};
  std::set<climate::ClimateMode> supported_modes_{};
  ClimateActionMap *mappings_{nullptr};
  climate::ClimateMode last_active_mode_{climate::CLIMATE_MODE_HEAT};
};

}  // namespace samsung_nasa
}  // namespace esphome
