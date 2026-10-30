#include "nasa_text_sensor.h"
#include <cstdio>

namespace esphome {
namespace samsung_nasa {

void NASA_TextSensor::on_receive(long value) {
  // Only process and publish if the numeric value has changed
  if (value != this->last_numeric_value_) {
    if (this->lookup_func_) {
      this->publish_state(this->lookup_func_(value));
    } else {
      this->publish_state(this->format_numeric_(value));
    }
    this->last_numeric_value_ = value;
  }
}

std::string NASA_TextSensor::format_numeric_(long value) const {
  if (!this->numeric_hex_)
    return std::to_string(value);
  // 32-bit two's complement, so negative values show the bit pattern as sent on the bus
  char buf[11];
  snprintf(buf, sizeof(buf), "0x%08X", (unsigned) (uint32_t) value);
  return std::string(buf);
}

void NASA_TextSensor::on_receive_structure(const uint8_t *data, uint8_t size) {
  std::string s;
  char buf[48];
  if (this->structure_format_ == 1 && size >= 7) {
    snprintf(buf, sizeof(buf), "DB%02X-%02X%02X%02X %02X%02X%02X", data[0], data[1], data[2], data[3], data[4], data[5],
             data[6]);
    s = buf;
  } else if (this->structure_format_ == 3 && size >= 11) {
    snprintf(buf, sizeof(buf), "DB%02X-%02X%02X%02X %02X%02X%02X", data[0], data[1], data[2], data[3], data[8], data[9],
             data[10]);
    s = buf;
  } else if (this->structure_format_ == 4 && size >= 6) {
    for (uint8_t i = 0; i < 6; i++) {
      snprintf(buf, sizeof(buf), i ? ":%02X" : "%02X", data[i]);
      s += buf;
    }
  } else if (this->structure_format_ == 2 && size >= 10) {
    std::string digits;
    for (uint8_t i = 0; i < 10; i++) {
      snprintf(buf, sizeof(buf), "%02X", data[i]);
      digits += buf;
    }
    for (uint8_t g = 0; g < 4; g++)
      s += (g ? "-[" : "[") + std::to_string(g) + "]" + digits.substr(g * 5, 5);
  } else {
    // text if all bytes (ignoring trailing 0x00/0xFF/space) are printable ASCII, otherwise hex "08 08 00 12 33"
    uint8_t n = size;
    while (n > 0 && (data[n - 1] == 0x00 || data[n - 1] == 0xFF || data[n - 1] == ' '))
      n--;
    // text with a leading length byte, e.g. 0x061A: 11 'EHS MONO LOWTEMP' 00
    uint8_t start = (n >= 3 && data[0] < 0x20 && data[0] <= size - 1) ? 1 : 0;
    bool text = n - start >= 2;
    for (uint8_t i = start; i < n && text; i++)
      text = data[i] >= 0x20 && data[i] < 0x7F;
    if (text) {
      s.assign(reinterpret_cast<const char *>(data + start), n - start);
    } else {
      for (uint8_t i = 0; i < size; i++) {
        snprintf(buf, sizeof(buf), i ? " %02X" : "%02X", data[i]);
        s += buf;
      }
    }
  }
  if (s != this->last_structure_) {
    this->last_structure_ = s;
    this->publish_state(s);
  }
}

void NASA_TextSensor::set_parent(NASA_Controller *controller) { this->controller_ = controller; }

}  // namespace samsung_nasa
}  // namespace esphome
