#pragma once

#include "esphome/core/automation.h"
#include "esphome/core/defines.h"
#include "esphome/core/log.h"
#include "nasa_base.h"
// Only include the platforms the config actually uses, so a sensors-only
// (read-only) config compiles without a switch/select/number component.
#ifdef USE_SAMSUNG_NASA_SWITCH
#include "switch/nasa_switch.h"
#endif
#ifdef USE_SAMSUNG_NASA_SELECT
#include "select/nasa_select.h"
#endif
#ifdef USE_SAMSUNG_NASA_NUMBER
#include "number/nasa_number.h"
#endif
#include "nasa_controller.h"
#include <vector>
#include <functional>
#include <algorithm>
#include <initializer_list>
#include <map>
#include <string>

namespace esphome {
namespace samsung_nasa {

template<typename... Ts> class NASA_Request_Read_Action : public Action<Ts...> {
 public:
  explicit NASA_Request_Read_Action(NASA_Controller *controller) : controller_(controller) {}

  void request_read(std::vector<NASA_Base *> components) { this->components_ = components; }
  // true: send the read to each component's device address instead of broadcasting it
  void set_addressed(bool addressed) { this->addressed_ = addressed; }

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
    if (!this->addressed_) {
      this->controller_->read(messages);
      return;
    }
    std::map<std::string, std::vector<uint16_t>> by_address;
    for (auto *c : this->components_)
      by_address[c->get_address()].push_back(c->get_message());
    for (auto &entry : by_address)
      this->controller_->read_from(entry.first, entry.second);
  }

 protected:
  std::vector<NASA_Base *> components_;
  bool addressed_{false};
  NASA_Controller *controller_;
};

template<typename... Ts> class NASA_Request_Write_Action : public Action<Ts...> {
 public:
  explicit NASA_Request_Write_Action(NASA_Controller *controller) : controller_(controller) {}

#ifdef USE_SAMSUNG_NASA_SWITCH
  void add_write(NASA_Switch *obj, TemplatableValue<bool, Ts...> value) {
    actions_.push_back([obj, value](const Ts &...x) {
      bool val = value.value(x...);
      if (debug_log_messages) {
        ESP_LOGI(TAG, "  -> Write Switch: 0x%X = %s", obj->get_message(), val ? "ON" : "OFF");
      }
      if (val) obj->turn_on(); else obj->turn_off();
    });
  }
#endif

#ifdef USE_SAMSUNG_NASA_NUMBER
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
#endif

#ifdef USE_SAMSUNG_NASA_SELECT
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
#endif

  void play(const Ts &...x) override {
    for (auto &action : actions_) {
      action(x...);
    }
  }

 protected:
  NASA_Controller *controller_;
  std::vector<std::function<void(const Ts &...)>> actions_;
};

template<typename... Ts> class NASA_Send_Structure_Action : public Action<Ts...> {
 public:
  explicit NASA_Send_Structure_Action(NASA_Controller *controller) : controller_(controller) {}

  void set_address(const std::string &address) { this->address_ = address; }
  void set_message(uint16_t message) { this->message_ = message; }
  void set_data_type(uint8_t data_type) { this->data_type_ = data_type; }
  void set_payload(const std::vector<uint8_t> &payload) { this->payload_ = payload; }

  void play(const Ts &...x) override {
    if (debug_log_messages) {
      ESP_LOGI(TAG, "Send Structure Action: 0x%X to %s (%u bytes)", this->message_, this->address_.c_str(),
               (unsigned) this->payload_.size());
    }
    this->controller_->send_structure(this->address_, this->message_, this->data_type_, this->payload_);
  }

 protected:
  NASA_Controller *controller_;
  std::string address_;
  uint16_t message_{0};
  uint8_t data_type_{1};
  std::vector<uint8_t> payload_;
};

}  // namespace samsung_nasa
}  // namespace esphome
