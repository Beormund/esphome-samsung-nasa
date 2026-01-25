from esphome.const import (
    CONF_DATA,
    CONF_DEFAULTS,
    CONF_ENTITY_CATEGORY,
    ENTITY_CATEGORY_CONFIG,
    CONF_ICON
)
from .const import *

ICON_TOGGLE_SWITCH = "mdi:toggle-switch"

def bool_defaults(
    lambda_from="return (x != 0);",
    lambda_to="return (x ? 1 : 0);"
):
    return lambda: {
        CONF_ICON: ICON_TOGGLE_SWITCH,
        NASA_LAMBDA_FROM: lambda_from,
        NASA_LAMBDA_TO: lambda_to
    }

def fsv_switch_data(code):
    return lambda: {
        CONF_ENTITY_CATEGORY: ENTITY_CATEGORY_CONFIG,
        NASA_FSV: code
    }

def empty_data(): return lambda: {}

switches = {
    0x4000: {
        NASA_LABEL: "ENUM_IN_OPERATION_POWER",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },
    0x4046: {
        NASA_LABEL: "ENUM_IN_SILENCE",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },
    0x4065: {
        NASA_LABEL: "ENUM_IN_WATER_HEATER_POWER",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },
    0x406D: {
        NASA_LABEL: "ENUM_IN_OUTING_MODE",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },
    0x411E: {
        NASA_LABEL: "ENUM_IN_OPERATION_POWER_ZONE2",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },
    0x4098: {
        NASA_LABEL: "ENUM_IN_FSV_3031",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(3031),
        CONF_DEFAULTS: bool_defaults()        
    },
    0x4099: {
        NASA_LABEL: "ENUM_IN_FSV_3041",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(3041),
        CONF_DEFAULTS: bool_defaults()
    },
    0x409B: {
        NASA_LABEL: "ENUM_IN_FSV_3051",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(3051),
        CONF_DEFAULTS: bool_defaults()
    },
    0x40A1: {
        NASA_LABEL: "ENUM_IN_FSV_4023",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(4023),
        CONF_DEFAULTS: bool_defaults()
    },
    0x40A2: {
        NASA_LABEL: "ENUM_IN_FSV_4031",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(4031),
        CONF_DEFAULTS: bool_defaults()
    },
    0x40A3: {
        NASA_LABEL: "ENUM_IN_FSV_4032",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(4032),
        CONF_DEFAULTS: bool_defaults()
    },
    0x4111: {
        NASA_LABEL: "ENUM_IN_OPERATION_AUTOMATIC_CLEANING",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },
    0x411A: {
        NASA_LABEL: "ENUM_IN_FSV_4061",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(4061),
        CONF_DEFAULTS: bool_defaults()
    },
    0x4128: {
        NASA_LABEL: "ENUM_IN_FSV_5022",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(5022),
        CONF_DEFAULTS: bool_defaults()
    },
    0x40A4: {
        NASA_LABEL: "ENUM_IN_FSV_5041",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(5041),
        CONF_DEFAULTS: bool_defaults()
    },
    0x40A7: {
        NASA_LABEL: "ENUM_IN_FSV_5051",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(5051),
        CONF_DEFAULTS: bool_defaults()
    },
    0x411B: {
        NASA_LABEL: "ENUM_IN_FSV_5081",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(5081),
        CONF_DEFAULTS: bool_defaults()
    },
    0x411C: {
        NASA_LABEL: "ENUM_IN_FSV_5091",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(5091),
        CONF_DEFAULTS: bool_defaults()
    },
    0x411D: {
        NASA_LABEL: "ENUM_IN_FSV_5094",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_switch_data(5094),
        CONF_DEFAULTS: bool_defaults()
    },

}