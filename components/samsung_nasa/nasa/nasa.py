import esphome.codegen as cg
import esphome.components.number as number
import esphome.components.select as select
import esphome.components.sensor as sensor
import esphome.components.text_sensor as text_sensor
import esphome.components.binary_sensor as binary_sensor
import esphome.components.switch as switch
import esphome.components.climate as climate
from esphome.config_validation import enum
from .const import *


samsung_nasa_ns = cg.esphome_ns.namespace("samsung_nasa")
ControllerMode = samsung_nasa_ns.enum("ControllerMode", is_class=True)
AddressClass = samsung_nasa_ns.enum("AddressClass", is_class=True)

NASA_Base   = samsung_nasa_ns.class_("NASA_Base")
NASA_Write  = samsung_nasa_ns.class_("NASA_Write", NASA_Base)
NASA_Number = samsung_nasa_ns.class_("NASA_Number", number.Number, NASA_Write, NASA_Base)
NASA_Select = samsung_nasa_ns.class_("NASA_Select", select.Select, NASA_Write, NASA_Base)
NASA_Sensor = samsung_nasa_ns.class_("NASA_Sensor", sensor.Sensor, NASA_Base)
NASA_TextSensor = samsung_nasa_ns.class_("NASA_TextSensor", text_sensor.TextSensor, NASA_Base)
NASA_BinarySensor = samsung_nasa_ns.class_("NASA_BinarySensor", binary_sensor.BinarySensor, NASA_Base)
NASA_Switch = samsung_nasa_ns.class_("NASA_Switch", switch.Switch, NASA_Write, NASA_Base)
NASA_Climate = samsung_nasa_ns.class_("NASA_Climate", climate.Climate, cg.Component)


CONTROLLER_MODES = {
    CONTROLLER_MODE_STATUS: ControllerMode.CONTROLLER_MODE_STATUS,
    CONTROLLER_MODE_CONTROL: ControllerMode.CONTROLLER_MODE_CONTROL,
    CONTROLLER_MODE_SCHEDULE: ControllerMode.CONTROLLER_MODE_SCHEDULE,
    CONTROLLER_MODE_ENERGY: ControllerMode.CONTROLLER_MODE_ENERGY,
    CONTROLLER_MODE_OPTION: ControllerMode.CONTROLLER_MODE_OPTION,
    CONTROLLER_MODE_SERVICE: ControllerMode.CONTROLLER_MODE_SERVICE,
    CONTROLLER_MODE_FSV: ControllerMode.CONTROLLER_MODE_FSV
}

ADDRESS_CLASSES = {
  ADDRESS_CLASS_OUTDOOR: AddressClass.ADDRESS_CLASS_OUTDOOR,
  ADDRESS_CLASS_HTU: AddressClass.ADDRESS_CLASS_HTU,
  ADDRESS_CLASS_INDOOR: AddressClass.ADDRESS_CLASS_INDOOR,
  ADDRESS_CLASS_ERV:  AddressClass.ADDRESS_CLASS_ERV,
  ADDRESS_CLASS_DIFFUSER: AddressClass.ADDRESS_CLASS_DIFFUSER,
  ADDRESS_CLASS_MCU: AddressClass.ADDRESS_CLASS_MCU,
  ADDRESS_CLASS_RMC: AddressClass.ADDRESS_CLASS_RMC,
  ADDRESS_CLASS_WIRED_REMOTE: AddressClass.ADDRESS_CLASS_WIRED_REMOTE,
  ADDRESS_CLASS_PIM: AddressClass.ADDRESS_CLASS_PIM,
  ADDRESS_CLASS_SIM: AddressClass.ADDRESS_CLASS_SIM,
  ADDRESS_CLASS_PEAK: AddressClass.ADDRESS_CLASS_PEAK,
  ADDRESS_CLASS_POWER_DIVIDER: AddressClass.ADDRESS_CLASS_POWER_DIVIDER,
  ADDRESS_CLASS_ON_OFF_CONTROLLER: AddressClass.ADDRESS_CLASS_ON_OFF_CONTROLLER,
  ADDRESS_CLASS_WIFI_KIT:AddressClass.ADDRESS_CLASS_WIFI_KIT,
  ADDRESS_CLASS_CENTRAL_CONTROLLER: AddressClass.ADDRESS_CLASS_CENTRAL_CONTROLLER,
  ADDRESS_CLASS_DMS: AddressClass.ADDRESS_CLASS_DMS,
  ADDRESS_CLASS_JIG_TESTER: AddressClass.ADDRESS_CLASS_JIG_TESTER,
  ADDRESS_CLASS_BROADCAST_SELF_LAYER: AddressClass.ADDRESS_CLASS_BROADCAST_SELF_LAYER,
  ADDRESS_CLASS_BROADCAST_CONTROL_LAYER: AddressClass.ADDRESS_CLASS_BROADCAST_CONTROL_LAYER,
  ADDRESS_CLASS_BROADCAST_SET_LAYER: AddressClass.ADDRESS_CLASS_BROADCAST_SET_LAYER,
  ADDRESS_CLASS_BROADCAST_CONTROL_AND_SET_LAYER: AddressClass.ADDRESS_CLASS_BROADCAST_CONTROL_AND_SET_LAYER,
  ADDRESS_CLASS_BROADCAST_MODULE_LAYER: AddressClass.ADDRESS_CLASS_BROADCAST_MODULE_LAYER,
  ADDRESS_CLASS_BROADCAST_CSM: AddressClass.ADDRESS_CLASS_BROADCAST_CSM,
  ADDRESS_CLASS_BROADCAST_LOCAL_LAYER: AddressClass.ADDRESS_CLASS_BROADCAST_LOCAL_LAYER,
  ADDRESS_CLASS_BROADCAST_CSML: AddressClass.ADDRESS_CLASS_BROADCAST_CSML,
  ADDRESS_CLASS_UNDEFINED: AddressClass.ADDRESS_CLASS_UNDEFINED
}

ADDRESS_CLASS_LABELS = {
  ADDRESS_CLASS_OUTDOOR: "Outdoor",
  ADDRESS_CLASS_HTU: "HTU",
  ADDRESS_CLASS_INDOOR: "Indoor",
  ADDRESS_CLASS_ERV: "ERV",
  ADDRESS_CLASS_DIFFUSER: "Diffuser",
  ADDRESS_CLASS_MCU: "MCU",
  ADDRESS_CLASS_RMC: "RMC",
  ADDRESS_CLASS_WIRED_REMOTE: "Wired Remote",
  ADDRESS_CLASS_PIM: "PIM",
  ADDRESS_CLASS_SIM: "SIM",
  ADDRESS_CLASS_PEAK: "Peak",
  ADDRESS_CLASS_POWER_DIVIDER: "Power Divider",
  ADDRESS_CLASS_ON_OFF_CONTROLLER: "On/Off Controller",
  ADDRESS_CLASS_WIFI_KIT: "WIFI Kit",
  ADDRESS_CLASS_CENTRAL_CONTROLLER: "Central Controller",
  ADDRESS_CLASS_DMS: "DMS",
  ADDRESS_CLASS_JIG_TESTER: "JIG Tester",
  ADDRESS_CLASS_BROADCAST_SELF_LAYER: "Broadcast Self Layer",
  ADDRESS_CLASS_BROADCAST_CONTROL_LAYER: "Broadcast Control Layer",
  ADDRESS_CLASS_BROADCAST_SET_LAYER: "Broadcast Set Layer",
  ADDRESS_CLASS_BROADCAST_CONTROL_AND_SET_LAYER: "Broadcast Control and Set Layer",
  ADDRESS_CLASS_BROADCAST_MODULE_LAYER: "Broadcast Module Layer",
  ADDRESS_CLASS_BROADCAST_CSM: "Broadcast CSM",
  ADDRESS_CLASS_BROADCAST_LOCAL_LAYER: "Broadcast Local Layer",
  ADDRESS_CLASS_BROADCAST_CSML: "Broadcast CSML",
  ADDRESS_CLASS_UNDEFINED: "Unknown"
}

def controller_mode(value):
    return enum(CONTROLLER_MODES, lower=False)(value)

def address_class(value):
    return enum(ADDRESS_CLASSES, lower=False)(value)

def available_as(message:int):
    from .numbers import numbers
    from .selects import selects
    from .sensors import sensors
    from .text_sensors import text_sensors
    from .binary_sensors import binary_sensors
    from .switches import switches
    result = set()
    if numbers.get(message) is not None:
        result.add("number")
    if selects.get(message) is not None:
        result.add("select")
    if sensors.get(message) is not None:
        result.add("sensor")
    if text_sensors.get(message) is not None:
        result.add("text_sensor")    
    if binary_sensors.get(message) is not None:
        result.add("binary_sensor")
    if switches.get(message) is not None:
        result.add("switch")
    return result
