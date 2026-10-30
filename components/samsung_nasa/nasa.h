#pragma once

#include <cstdint>
#include <cstddef>
#include <map>
#include <string>

namespace esphome {
namespace samsung_nasa {

static const char *TAG = "samsung_nasa";
extern bool debug_log_raw_bytes;
extern bool debug_log_undefined_messages;
extern bool debug_log_messages;
// Diagnostics: session id, receive number per packet and error counters
extern uint32_t diag_session;
extern uint32_t diag_rx_seq;
extern uint32_t diag_ok, diag_err_size, diag_err_end, diag_err_crc, diag_err_uart;
void diag_log_raw(const char *kind, const uint8_t *data, size_t len);
extern uint16_t silence_interval;
extern uint16_t retry_interval;
extern uint8_t min_retries;
extern uint16_t send_timeout;

enum class ControllerMode : uint8_t {
  CONTROLLER_MODE_STATUS = 0,
  CONTROLLER_MODE_CONTROL = 1,
  CONTROLLER_MODE_SCHEDULE = 2,
  CONTROLLER_MODE_ENERGY = 3,
  CONTROLLER_MODE_OPTION = 4,
  CONTROLLER_MODE_SERVICE = 5,
  CONTROLLER_MODE_FSV = 6
};

enum class AddressClass : uint8_t {
  ADDRESS_CLASS_OUTDOOR = 0x10,
  ADDRESS_CLASS_HTU = 0x11,
  ADDRESS_CLASS_INDOOR = 0x20,
  ADDRESS_CLASS_ERV = 0x30,
  ADDRESS_CLASS_DIFFUSER = 0x35,
  ADDRESS_CLASS_MCU = 0x38,
  ADDRESS_CLASS_RMC = 0x40,
  ADDRESS_CLASS_WIRED_REMOTE = 0x50,
  ADDRESS_CLASS_PIM = 0x58,
  ADDRESS_CLASS_SIM = 0x59,
  ADDRESS_CLASS_PEAK = 0x5A,
  ADDRESS_CLASS_POWER_DIVIDER = 0x5B,
  ADDRESS_CLASS_ON_OFF_CONTROLLER = 0x60,
  ADDRESS_CLASS_WIFI_KIT = 0x62,
  ADDRESS_CLASS_CENTRAL_CONTROLLER = 0x65,
  ADDRESS_CLASS_DMS = 0x6A,
  ADDRESS_CLASS_JIG_TESTER = 0x80,
  ADDRESS_CLASS_BROADCAST_SELF_LAYER = 0xB0,
  ADDRESS_CLASS_BROADCAST_CONTROL_LAYER = 0xB1,
  ADDRESS_CLASS_BROADCAST_SET_LAYER = 0xB2,
  ADDRESS_CLASS_BROADCAST_CONTROL_AND_SET_LAYER = 0xB3,
  ADDRESS_CLASS_BROADCAST_MODULE_LAYER = 0xB4,
  ADDRESS_CLASS_BROADCAST_CSM = 0xB7,
  ADDRESS_CLASS_BROADCAST_LOCAL_LAYER = 0xB8,
  ADDRESS_CLASS_BROADCAST_CSML = 0xBF,
  ADDRESS_CLASS_UNDEFINED = 0xFF
};

const std::map<AddressClass, std::string> AddressClass_Labels = {
    {AddressClass::ADDRESS_CLASS_OUTDOOR, "Outdoor"},
    {AddressClass::ADDRESS_CLASS_HTU, "HTU"},
    {AddressClass::ADDRESS_CLASS_INDOOR, "Indoor"},
    {AddressClass::ADDRESS_CLASS_ERV, "ERV"},
    {AddressClass::ADDRESS_CLASS_DIFFUSER, "Diffuser"},
    {AddressClass::ADDRESS_CLASS_MCU, "MCU"},
    {AddressClass::ADDRESS_CLASS_RMC, "RMC"},
    {AddressClass::ADDRESS_CLASS_WIRED_REMOTE, "Wired Remote"},
    {AddressClass::ADDRESS_CLASS_PIM, "PIM"},
    {AddressClass::ADDRESS_CLASS_SIM, "SIM"},
    {AddressClass::ADDRESS_CLASS_PEAK, "Peak"},
    {AddressClass::ADDRESS_CLASS_POWER_DIVIDER, "Power Divider"},
    {AddressClass::ADDRESS_CLASS_ON_OFF_CONTROLLER, "On/Off Controller"},
    {AddressClass::ADDRESS_CLASS_WIFI_KIT, "WIFI Kit"},
    {AddressClass::ADDRESS_CLASS_CENTRAL_CONTROLLER, "Central Controller"},
    {AddressClass::ADDRESS_CLASS_DMS, "DMS"},
    {AddressClass::ADDRESS_CLASS_JIG_TESTER, "JIG Tester"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_SELF_LAYER, "Broadcast Self Layer"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_CONTROL_LAYER, "Broadcast Control Layer"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_SET_LAYER, "Broadcast Set Layer"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_CONTROL_AND_SET_LAYER, "Broadcast Control and Set Layer"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_MODULE_LAYER, "Broadcast Module Layer"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_CSM, "Broadcast CSM"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_LOCAL_LAYER, "Broadcast Local Layer"},
    {AddressClass::ADDRESS_CLASS_BROADCAST_CSML, "Broadcast CSML"},
    {AddressClass::ADDRESS_CLASS_UNDEFINED, "Unknown"}};

}  // namespace samsung_nasa
}  // namespace esphome
