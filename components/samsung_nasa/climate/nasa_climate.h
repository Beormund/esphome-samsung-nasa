#pragma once

#include "../switch/nasa_switch.h"
#include "../number/nasa_number.h"
#include "../sensor/nasa_sensor.h"
#include "../select/nasa_select.h"
#include "esphome/core/component.h"
#include "esphome/components/climate/climate.h"
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
  void set_power_switch(NASA_Switch *power) { this->power_ = power; };
  void set_target_temp(NASA_Number *target_temp) { this->target_temp_ = target_temp; };
  void set_current_temp(NASA_Sensor *current_temp) { this->current_temp_ = current_temp; }
  void set_action_sensor(NASA_Sensor *action_sens) { this->action_sens_ = action_sens; }
  void set_action_map(ClimateActionMap *mappings) { this->mappings_ = mappings; }
  void set_custom_preset_select(NASA_Select *custom_presets) { this->custom_presets_ = custom_presets; }
  bool update_action(climate::ClimateAction new_action);

 protected:
  void control(const climate::ClimateCall &call) override;
  std::set<std::string> get_custom_presets();
  void on_power(bool state);
  void on_target_temp(float state);
  void on_current_temp(float state);
  void on_action_sens(float state);
  void on_preset_select(std::string state, size_t index);
  bool update_mode(climate::ClimateMode new_mode);
  bool update_current_temp(float new_temp);
  bool update_target_temp(float new_temp);
  bool update_custom_preset(std::string new_value);
  climate::ClimateTraits traits() override;

  NASA_Switch *power_{nullptr};
  NASA_Number *target_temp_{nullptr};
  NASA_Sensor *current_temp_{nullptr};
  NASA_Sensor *action_sens_{nullptr};
  NASA_Select *custom_presets_{nullptr};
  ClimateActionMap *mappings_{nullptr};
};

}  // namespace samsung_nasa
}  // namespace esphome