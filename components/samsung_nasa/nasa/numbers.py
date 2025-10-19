from esphome.const import (
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_DISTANCE,
    UNIT_EMPTY,
    UNIT_CELSIUS,
    UNIT_MINUTE,
    UNIT_HOUR,
    UNIT_KILOWATT,
    UNIT_SECOND,
    CONF_ENTITY_CATEGORY,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_DEVICE_CLASS,
    ENTITY_CATEGORY_CONFIG,
    ENTITY_CATEGORY_NONE,
    CONF_ICON,
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_STEP,
    CONF_DATA,
    CONF_DEFAULTS,
    ICON_EMPTY,
    ICON_POWER,
    ICON_THERMOMETER,
    ICON_TIMELAPSE
)
from .const import *

UNIT_DAY = "day"
ICON_VALVE = "mdi:valve"
ICON_PUMP = "mdi:pump"


def fsv_numeric_data(code, min_val=0, max_val=1, step = 1):
    return lambda: {
        CONF_MIN_VALUE: min_val, 
        CONF_MAX_VALUE: max_val,
        CONF_STEP: step,
        CONF_ENTITY_CATEGORY: ENTITY_CATEGORY_CONFIG,
        NASA_FSV: code
    }

def cmd_numeric_data(min_val = 0, max_val = 1, step = 1):
    return lambda: {
        CONF_MIN_VALUE: min_val, 
        CONF_MAX_VALUE: max_val,
        CONF_STEP: step,
        CONF_ENTITY_CATEGORY: ENTITY_CATEGORY_NONE
    }

def number_defaults(
        device_class = DEVICE_CLASS_EMPTY,
        unit_of_measurement = UNIT_EMPTY,
        icon = ICON_EMPTY,
        lambda_from = "return x;", 
        lambda_to = "return x;"
):
    return lambda: {
        CONF_DEVICE_CLASS: device_class,
        CONF_UNIT_OF_MEASUREMENT: unit_of_measurement,
        CONF_ICON: icon,
        NASA_LAMBDA_FROM: lambda_from,
        NASA_LAMBDA_TO: lambda_to
    }

def temperature_defaults():
    return number_defaults(
        DEVICE_CLASS_TEMPERATURE,
        UNIT_CELSIUS,
        ICON_THERMOMETER,
        "return ((int16_t)x) * 0.1;",
        "return (uint16_t)(x * 10);"
    )

def lambda_defaults(
    lambda_from = "return x;", 
    lambda_to = "return x;"
): return lambda: {
    NASA_LAMBDA_FROM: lambda_from,
    NASA_LAMBDA_TO: lambda_to
}

numbers = {
    0x4201: {
        NASA_LABEL: "VAR_IN_TEMP_TARGET_F",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_numeric_data(16, 30),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4248: {
        NASA_LABEL: "VAR_IN_TEMP_WATER_LAW_TARGET_F",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_numeric_data(-5, 5),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x42D6: {
        NASA_LABEL: "VAR_IN_TEMP_TARGET_ZONE2_F",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_numeric_data(16, 30),
        CONF_DEFAULTS: temperature_defaults()
    },        
    0x4235: {
        NASA_LABEL: "VAR_IN_TEMP_WATER_HEATER_TARGET_F",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_numeric_data(30, 65),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4247: {
        NASA_LABEL: "VAR_IN_TEMP_WATER_OUTLET_TARGET_F",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_numeric_data(15, 55),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x424A: {
        NASA_LABEL: "VAR_IN_FSV_1011",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1011, 18, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x424B: {
        NASA_LABEL: "VAR_IN_FSV_1012",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1012, 5, 18),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x424C: {
        NASA_LABEL: "VAR_IN_FSV_1021",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1021, 28, 30),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x424D: {
        NASA_LABEL: "VAR_IN_FSV_1022",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1022, 18, 28),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x424E: {
        NASA_LABEL: "VAR_IN_FSV_1031",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1031, 37, 65),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x424F: {
        NASA_LABEL: "VAR_IN_FSV_1032",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1032, 15, 37),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4250: {
        NASA_LABEL: "VAR_IN_FSV_1041",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1041, 18, 30),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4251: {
        NASA_LABEL: "VAR_IN_FSV_1042",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1042, 16, 18),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4252: {
        NASA_LABEL: "VAR_IN_FSV_1051",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1051, 50, 70),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4253: {
        NASA_LABEL: "VAR_IN_FSV_1052",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(1052, 30, 40),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4254: {
        NASA_LABEL: "VAR_IN_FSV_2011",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2011, -20, 5),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4255: {
        NASA_LABEL: "VAR_IN_FSV_2012",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2012, 10, 20),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4256: {
        NASA_LABEL: "VAR_IN_FSV_2021",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2021, 17, 65),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4257: {
        NASA_LABEL: "VAR_IN_FSV_2022",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2022, 17, 65),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4258: {
        NASA_LABEL: "VAR_IN_FSV_2031",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2031, 17, 65),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4259: {
        NASA_LABEL: "VAR_IN_FSV_2032",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2032, 17, 65),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x425A: {
        NASA_LABEL: "VAR_IN_FSV_2051",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2051, 25, 35),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x425B: {
        NASA_LABEL: "VAR_IN_FSV_2052",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2052, 35, 45),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x425C: {
        NASA_LABEL: "VAR_IN_FSV_2061",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2061, 5, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x425D: {
        NASA_LABEL: "VAR_IN_FSV_2062",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2062, 5, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x425E: {
        NASA_LABEL: "VAR_IN_FSV_2071",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2071, 5, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x425F: {
        NASA_LABEL: "VAR_IN_FSV_2072",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2072, 5, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4260: {
        NASA_LABEL: "VAR_IN_FSV_3021",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3021, 45, 65),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4261: {
        NASA_LABEL: "VAR_IN_FSV_3022",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3022, 0, 10),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4262: {
        NASA_LABEL: "VAR_IN_FSV_3023",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3023, 5, 30),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4263: {
        NASA_LABEL: "VAR_IN_FSV_3024",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3024, 1, 20),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DURATION, UNIT_MINUTE, ICON_TIMELAPSE)
    },
    0x4264: {
        NASA_LABEL: "VAR_IN_FSV_3025",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3025, 5, 95, 5),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DURATION, UNIT_MINUTE, ICON_TIMELAPSE)
    },
    0x4265: {
        NASA_LABEL: "VAR_IN_FSV_3026",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3026, 0.5, 10, 0.5),
        CONF_DEFAULTS: number_defaults(
            DEVICE_CLASS_DURATION, 
            UNIT_HOUR, 
            ICON_TIMELAPSE, 
            "return ((int16_t)x) / 60;",
            "return (uint16_t)(x * 60);"
        )
    },
     0x4266: {
        NASA_LABEL: "VAR_IN_FSV_3032",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3032, 20, 95, 5),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DURATION, UNIT_MINUTE, ICON_TIMELAPSE)
    },
     0x4267: {
        NASA_LABEL: "VAR_IN_FSV_3033",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3033, 0, 4),
        CONF_DEFAULTS: temperature_defaults()
    },
     0x4269: {
        NASA_LABEL: "VAR_IN_FSV_3043",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3043, 0, 23),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DURATION, UNIT_HOUR, ICON_TIMELAPSE)
    },
     0x426A: {
        NASA_LABEL: "VAR_IN_FSV_3044",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3044, 40, 70, 5),
        CONF_DEFAULTS: temperature_defaults()
    },
     0x426B: {
        NASA_LABEL: "VAR_IN_FSV_3045",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3045, 5, 60, 5),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DURATION, UNIT_MINUTE, ICON_TIMELAPSE)
    },
     0x426C: {
        NASA_LABEL: "VAR_IN_FSV_3052",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3052, 30, 300, 10),
        CONF_DEFAULTS: number_defaults(
            DEVICE_CLASS_DURATION, 
            UNIT_MINUTE, 
            ICON_TIMELAPSE,
            "return (x * 10);",
            "return (x / 10);"
        )
    },
     0x42CE: {
        NASA_LABEL: "VAR_IN_FSV_3046",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3046, 1, 24),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DURATION, UNIT_HOUR, ICON_TIMELAPSE)
    },
    0x42ED: {
        NASA_LABEL: "VAR_IN_FSV_3081",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3081, 1, 6),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_POWER, UNIT_KILOWATT, ICON_POWER)
    },
    0x42EE: {
        NASA_LABEL: "VAR_IN_FSV_3082",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3082, 0, 6),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_POWER, UNIT_KILOWATT, ICON_POWER)
    },
    0x42EF: {
        NASA_LABEL: "VAR_IN_FSV_3083",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(3083, 1, 6),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_POWER, UNIT_KILOWATT, ICON_POWER)
    },
    0x426D: {
        NASA_LABEL: "VAR_IN_FSV_4012",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4012, -15, 20),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x426E: {
        NASA_LABEL: "VAR_IN_FSV_4013",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4013, 10, 45),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4270: {
        NASA_LABEL: "VAR_IN_FSV_4024",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4024, -25, 35),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4271: {
        NASA_LABEL: "VAR_IN_FSV_4025",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4025, 10, 55, 5),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4272: {
        NASA_LABEL: "VAR_IN_FSV_4033",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4033, -20, 5),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4286: {
        NASA_LABEL: "VAR_IN_FSV_4042",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4042, 5, 15),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4287: {
        NASA_LABEL: "VAR_IN_FSV_4043",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4043, 5, 15),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x40C1: {
        NASA_LABEL: "VAR_IN_FSV_4044",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4044, 1, 5),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DISTANCE, UNIT_EMPTY, ICON_VALVE)
    },
     0x4288: {
        NASA_LABEL: "VAR_IN_FSV_4045",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4045, 1, 30),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DURATION, UNIT_MINUTE, ICON_TIMELAPSE)
    },
     0x4289: {
        NASA_LABEL: "VAR_IN_FSV_4046",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4046, 60, 240, 30),
        CONF_DEFAULTS: number_defaults(
            DEVICE_CLASS_DURATION, 
            UNIT_SECOND, 
            ICON_TIMELAPSE,  
            "return (x * 10);",
            "return (x / 10);"
        )
    },
    0x428A: {
        NASA_LABEL: "VAR_IN_FSV_4052",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4052, 2, 8),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x40C3: {
        NASA_LABEL: "VAR_IN_FSV_4053",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(4053, 1, 3),
        CONF_DEFAULTS: number_defaults(DEVICE_CLASS_DISTANCE, UNIT_EMPTY, ICON_PUMP)
    },
    0x4273: {
        NASA_LABEL: "VAR_IN_FSV_5011",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5011, 5, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4274: {
        NASA_LABEL: "VAR_IN_FSV_5012",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5012, 18, 30),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4275: {
        NASA_LABEL: "VAR_IN_FSV_5013",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5013, 15, 55),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4276: {
        NASA_LABEL: "VAR_IN_FSV_5014",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5014, 16, 30),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4277: {
        NASA_LABEL: "VAR_IN_FSV_5015",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5015, 5, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4278: {
        NASA_LABEL: "VAR_IN_FSV_5016",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5016, 5, 25),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4279: {
        NASA_LABEL: "VAR_IN_FSV_5017",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5017, 15, 55),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x427A: {
        NASA_LABEL: "VAR_IN_FSV_5018",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5018, 15, 55),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x427B: {
        NASA_LABEL: "VAR_IN_FSV_5019",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5019, 30, 70),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x427C: {
        NASA_LABEL: "VAR_IN_FSV_5021",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5021, 0, 40),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x42F0: {
        NASA_LABEL: "VAR_IN_FSV_5023",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5023, 0, 40),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x42DB: {
        NASA_LABEL: "VAR_IN_FSV_5082",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5082, 1, 20),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x42DC: {
        NASA_LABEL: "VAR_IN_FSV_5083",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5083, 1, 50),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x42DD: {
        NASA_LABEL: "VAR_IN_FSV_5092",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5092, 1, 50),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x42DE: {
        NASA_LABEL: "VAR_IN_FSV_5093",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(5093, 1, 40),
        CONF_DEFAULTS: temperature_defaults()
    },
}