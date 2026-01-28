#pragma once

#include "esphome/core/automation.h"
#include "esphome/core/log.h"
#include "nasa_base.h"
#include "switch/nasa_switch.h"
#include "select/nasa_select.h"
#include "number/nasa_number.h"
#include "nasa_controller.h"
#include <vector>
#include <functional>
#include <algorithm>
#include <initializer_list>

namespace esphome {
namespace samsung_nasa {

template<typename... Ts> class NASA_Request_Read_Action : public Action<Ts...> {
 public:
  explicit NASA_Request_Read_Action(NASA_Controller *controller) : controller_(controller) {}

  void request_read(std::vector<NASA_Base *> components) { this->components_ = components; }

  void play(Ts... x) override {
    if (debug_log_messages) {
      ESP_LOGI(TAG, "Request Read Action for messages:");
    }
    std::vector<uint16_t> messages;
    std::for_each(begin(components_), end(components_), [&messages](NASA_Base *c) {
      if (debug_log_messages) {
        ESP_LOGI(TAG, "  -> 0x%X [%s]", c->get_message(), c->get_label().c_str());
      };
      messages.push_back(c->get_message());
    });
    this->controller_->read(messages);
  }

 protected:
  std::vector<NASA_Base *> components_;
  NASA_Controller *controller_;
};

template<typename... Ts> class NASA_Request_Write_Action : public Action<Ts...> {
 public:
  explicit NASA_Request_Write_Action(NASA_Controller *controller) : controller_(controller) {}

  void add_write(NASA_Switch *obj, TemplatableValue<bool, Ts...> value) {
    actions_.push_back([obj, value](const Ts &...x) {
      bool val = value.value(x...);
      if (debug_log_messages) {
        ESP_LOGI(TAG, "  -> Write Switch: 0x%X = %s", obj->get_message(), val ? "ON" : "OFF");
      }
      if (val) obj->turn_on(); else obj->turn_off();
    });
  }

  void add_write(NASA_Number *obj, TemplatableValue<float, Ts...> value) {
    actions_.push_back([obj, value](const Ts &...x) {
      float val = value.value(x...);
      if (val < obj->traits.get_min_value() || val > obj->traits.get_max_value()) {
        ESP_LOGE(TAG, "Validation Error: %f out of range for 0x%X", val, obj->get_message());
        return;
      }
      if (debug_log_messages) {
        ESP_LOGI(TAG, "  -> Write Number: 0x%X = %.1f", obj->get_message(), val);
      }
      auto call = obj->make_call();
      call.set_value(val);
      call.perform();
    });
  }

  void add_write(NASA_Select *obj, TemplatableValue<std::string, Ts...> value) {
    actions_.push_back([obj, value](const Ts &...x) {
      std::string val = value.value(x...);
      if (!obj->has_option(val)) {
        ESP_LOGE(TAG, "Validation Error: '%s' invalid for 0x%X", val.c_str(), obj->get_message());
        return;
      }
      if (debug_log_messages) {
        ESP_LOGI(TAG, "  -> Write Select: 0x%X = %s", obj->get_message(), val.c_str());
      }
      auto call = obj->make_call();
      call.set_option(val);
      call.perform();
    });
  }

  void play(const Ts &...x) override {
    for (auto &action : actions_) {
      action(x...);
    }
  }

 protected:
  NASA_Controller *controller_;
  std::vector<std::function<void(const Ts &...)>> actions_;
};

}  // namespace samsung_nasa
}  // namespace esphome