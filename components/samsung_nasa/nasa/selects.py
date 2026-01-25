from esphome.const import (
    CONF_ENTITY_CATEGORY,
    ENTITY_CATEGORY_CONFIG,
    ENTITY_CATEGORY_NONE,
    CONF_DATA,
    CONF_DEFAULTS,
    CONF_OPTIONS,
    CONF_ICON
)
from .const import *

ICON_FORM_DROPDOWN = "mdi:form-dropdown"

def select_defaults(
    offset:int = 0
): 
    return lambda: {
        CONF_ICON: ICON_FORM_DROPDOWN,
        NASA_LAMBDA_FROM: "return {};".format("x-"+str(offset) if offset > 0 else "x"),
        NASA_LAMBDA_TO: "return {};".format("x+"+str(offset) if offset > 0 else "x")
    }

def fsv_select_data(code:int, options:list):
    return lambda: {
        NASA_FSV: code,
        CONF_OPTIONS: options,
        CONF_ENTITY_CATEGORY: ENTITY_CATEGORY_CONFIG,
    }

def cmd_select_data(options:list):
    return lambda: {
        CONF_OPTIONS: options,
        CONF_ENTITY_CATEGORY: ENTITY_CATEGORY_NONE
    }

selects = {
    0x4001: {
        NASA_LABEL: "ENUM_IN_OPERATION_MODE",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_select_data(["Auto", "Cool", "Dry", "Fan", "Heat"]),
        CONF_DEFAULTS: select_defaults()
    },
    0x4066: {
        NASA_LABEL: "ENUM_IN_WATER_HEATER_MODE",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_select_data(["Economy", "Standard", "Power", "Force"]),
        CONF_DEFAULTS: select_defaults()
    },
    0x406F: {
        NASA_LABEL: "ENUM_IN_REFERENCE_EHS_TEMP",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_select_data(["Indoor Temp", "Water Out"]),
        CONF_DEFAULTS: select_defaults()
    },
    0x4093: {
        NASA_LABEL: "VAR_IN_FSV_2041",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(2041, ["WL1", "WL2"]),
        CONF_DEFAULTS: select_defaults(offset=1)
    },
    0x4094: {
        NASA_LABEL: "VAR_IN_FSV_2081",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(2081, ["WL1", "WL2"]),
        CONF_DEFAULTS: select_defaults(offset=1)
    },
    0x4095: {
        NASA_LABEL: "VAR_IN_FSV_2091",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(2091, [
            "None", 
            "Thermostat On/Off Only", 
            "Thermostat On/Off + WL #1", 
            "Thermostat On/Off + WL #2", 
            "Thermostat On/Off + WL #3"]),
        CONF_DEFAULTS: select_defaults()
    },
    0x4096: {
        NASA_LABEL: "VAR_IN_FSV_2092",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(2092, [
            "None", 
            "Thermostat On/Off Only", 
            "Thermostat On/Off + WL #1", 
            "Thermostat On/Off + WL #2", 
            "Thermostat On/Off + WL #3"]),
        CONF_DEFAULTS: select_defaults()
    },
    0x4127: {
        NASA_LABEL: "VAR_IN_FSV_2093",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(2093, [
            "Thermostat On/Off Only", 
            "Thermostat On/Off + WL #1", 
            "Thermostat On/Off + WL #2", 
            "Thermostat On/Off + WL #3"]),
        CONF_DEFAULTS: select_defaults(offset=1)
    },
    0x4097: {
        NASA_LABEL: "VAR_IN_FSV_3011",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(3011, ["Off", "Thermo (On) #1", "Thermo (Off) #2"]),
        CONF_DEFAULTS: select_defaults()        
    },
    0x409A: {
        NASA_LABEL: "VAR_IN_FSV_3042",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(3042, [
            "Sunday", 'Monday', "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "All"
        ]),
        CONF_DEFAULTS: select_defaults()           
    },
    0x409C: {
        NASA_LABEL: "VAR_IN_FSV_3061",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(3061, [
            "No", "Solar + DHW", "DHW Thermostat"
        ]),
        CONF_DEFAULTS: select_defaults()  
    },
    0x409D: {
        NASA_LABEL: "VAR_IN_FSV_3071",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(3071, [
            "Room", "Tank"
        ]),
        CONF_DEFAULTS: select_defaults()  
    },
    0x409E: {
        NASA_LABEL: "VAR_IN_FSV_4011",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(4011, [
            "DHW", "Heating"
        ]),
        CONF_DEFAULTS: select_defaults()          
    },
    0x409F: {
        NASA_LABEL: "VAR_IN_FSV_4021",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(4021, [
            "No", "2 stage backup heater", "1 stage backup heater"
        ]),
        CONF_DEFAULTS: select_defaults()          
    },
    0x40A0: {
        NASA_LABEL: "VAR_IN_FSV_4022",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(4022, [
            "Both", "BUH", "BSH"
        ]),
        CONF_DEFAULTS: select_defaults()          
    },
    0x40C0: {
        NASA_LABEL: "VAR_IN_FSV_4041",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(4041, [
            "No", "Temp Difference", "WL"
        ]),
        CONF_DEFAULTS: select_defaults()          
    },
    0x40C2: {
        NASA_LABEL: "VAR_IN_FSV_4051",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(4051, [
            "Not use", "Output 100%", "Output 70%"
        ]),
        CONF_DEFAULTS: select_defaults()          
    },
    0x40A5: {
        NASA_LABEL: "ENUM_IN_FSV_5042",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(5042, [
            "Compressor + Booster Permitted", "Compressor Only Permitted", "Booster Only Permitted", "None Permitted"
        ]),
        CONF_DEFAULTS: select_defaults()          
    },
    0x40A6: {
        NASA_LABEL: "ENUM_IN_FSV_5043",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_select_data(5043, [
            "Low", "High"
        ]),
        CONF_DEFAULTS: select_defaults()          
    },
    0x8003: {
        NASA_LABEL: "ENUM_OUT_OPERATION_HEATCOOL",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_select_data(["Cool", "Heat", "CoolMain", "HeatMain"]),
        CONF_DEFAULTS: select_defaults(offset=1)
    }
}