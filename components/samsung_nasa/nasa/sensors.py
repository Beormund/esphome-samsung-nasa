from esphome.core import Lambda
from esphome.const import (
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_VOLUME_FLOW_RATE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_FREQUENCY,
    STATE_CLASS_TOTAL_INCREASING,
    STATE_CLASS_NONE,
    STATE_CLASS_MEASUREMENT,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_WATT,
    UNIT_KILOWATT_HOURS,
    UNIT_EMPTY,
    UNIT_PERCENT,
    UNIT_REVOLUTIONS_PER_MINUTE,
    UNIT_VOLT,
    UNIT_HERTZ,
    CONF_ENTITY_CATEGORY,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_DEVICE_CLASS,
    ENTITY_CATEGORY_DIAGNOSTIC,
    ENTITY_CATEGORY_NONE,
    CONF_STATE_CLASS,
    CONF_DELTA,
    CONF_ICON,
    CONF_ACCURACY_DECIMALS,
    CONF_DEFAULTS,
    CONF_FILTERS,
    CONF_LAMBDA,
    CONF_MULTIPLY,
    ICON_COUNTER,
    ICON_EMPTY,
    ICON_FAN,
    ICON_THERMOMETER,
    ICON_FLASH,
    ICON_TIMELAPSE
)
from .const import *

ICON_ALERT = "mdi:alert"
ICON_HUMIDITY = "mdi:water-percent"
ICON_FLOW = "mdi:water-circle"
ICON_SINE_WAVE= "mdi:sine-wave"
UNIT_LITRES_PER_MIN = "L/min"

def sensor_defaults(
    unit_of_measurement = UNIT_EMPTY,
    icon = ICON_EMPTY,
    accuracy_decimals = 0,
    device_class = DEVICE_CLASS_EMPTY,
    state_class = STATE_CLASS_NONE,
    entity_category = ENTITY_CATEGORY_NONE,
    filters = []
):
    return lambda: {
        CONF_UNIT_OF_MEASUREMENT: unit_of_measurement,
        CONF_ICON: icon,
        CONF_ACCURACY_DECIMALS: accuracy_decimals,
        CONF_DEVICE_CLASS: device_class,
        CONF_STATE_CLASS: state_class,
        CONF_ENTITY_CATEGORY: entity_category,
        CONF_FILTERS: filters
    }

def temp_sensor_defaults():
    return sensor_defaults(
        UNIT_CELSIUS, 
        ICON_THERMOMETER, 
        1, 
        DEVICE_CLASS_TEMPERATURE, 
        STATE_CLASS_MEASUREMENT,
        ENTITY_CATEGORY_NONE,
        [{CONF_LAMBDA: Lambda("return (int16_t)x;")}, {CONF_MULTIPLY: 0.1}]        
    )

sensors = {
    0x24FC: {
        NASA_LABEL: "LVAR_NM_OUT_SENSOR_VOLTAGE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_FLASH,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT        
        )
    },
    0x4002: {
        NASA_LABEL: "ENUM_IN_OPERATION_MODE_REAL",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },
    0x4038: {
        NASA_LABEL: "ENUM_IN_STATE_HUMIDITY_PERCENT",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_HUMIDITY,
            device_class=DEVICE_CLASS_HUMIDITY,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x4067: {
        NASA_LABEL: "ENUM_IN_3WAY_VALVE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },
    0x4069: {
        NASA_LABEL: "ENUM_IN_THERMOSTAT1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },
    0x406A: {
        NASA_LABEL: "ENUM_IN_THERMOSTAT2",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },
    0x408A: {
        NASA_LABEL: "ENUM_IN_2WAY_VALVE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },
    0x40C4: {
        NASA_LABEL: "ENUM_IN_WATERPUMP_PWM_VALUE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_FLOW,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x4202: {
        NASA_LABEL: "VAR_IN_DHW_HEAT_UNTIL",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x4204: {
        NASA_LABEL: "VAR_IN_WATER_OUT_TW2",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x4205: {
        NASA_LABEL: "VAR_IN_TEMP_EVA_IN_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x4206: {
        NASA_LABEL: "VAR_IN_TEMP_EVA_OUT_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x4236: {
        NASA_LABEL: "VAR_IN_TEMP_WATER_IN_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },     
    0x4237: {
        NASA_LABEL: "VAR_IN_TEMP_WATER_TANK_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x4238: {
        NASA_LABEL: "VAR_IN_TEMP_WATER_OUT_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },   
    0x427F: {
        NASA_LABEL: "VAR_IN_TEMP_WATER_LAW_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },   
    0x4203: {
        NASA_LABEL: "VAR_IN_TEMP_ROOM_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x42D4: {
        NASA_LABEL: "VAR_IN_TEMP_ZONE2_F",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x42E8: {
        NASA_LABEL: "VAR_IN_FLOW_SENSOR_VOLTAGE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_FLASH,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_MULTIPLY: 0.1}]
        )
    },
    0x42E9: {
        NASA_LABEL: "VAR_IN_FLOW_SENSOR_CALC",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_LITRES_PER_MIN,
            icon=ICON_FLOW,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLUME_FLOW_RATE,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_MULTIPLY: 0.1}]
        )
    },
    0x4284: {
        NASA_LABEL: "NASA_INDOOR_POWER_CONSUMPTION",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_WATT,
            icon=ICON_FLASH,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT            
        )
    },
    0x4423: {
        NASA_LABEL: "LVAR_IN_MINS_SINCE_INST",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement= "d",
            icon=ICON_TIMELAPSE,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DURATION,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_LAMBDA: Lambda("return x / 1440.0;")}]
        )
    },
    0x4424: {
        NASA_LABEL: "LVAR_IN_MINS_ACTIVE_SINCE_INST",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement= "h",
            icon=ICON_TIMELAPSE,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DURATION,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_LAMBDA: Lambda("return x / 60.0;")}]
        )
    },    
    0x4426: {
        NASA_LABEL: "LVAR_IN_4426",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS:sensor_defaults(
            unit_of_measurement=UNIT_WATT,
            icon=ICON_FLASH,
            accuracy_decimals=1, 
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_LAMBDA: Lambda("return (int16_t)x;")}] 
        )
    },    
    0x4427: {
        NASA_LABEL: "LVAR_IN_4427",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS:sensor_defaults(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            icon=ICON_COUNTER,
            accuracy_decimals=3, 
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            filters=[{CONF_MULTIPLY: 0.001}]
        )
    },
    0x8000: {
        NASA_LABEL: "ENUM_OUT_OPERATION_SERVICE_OP",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },
    0x8001: {
        NASA_LABEL: "ENUM_OUT_OPERATION_ODU_MODE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },
    0x8061: {
        NASA_LABEL: "ENUM_OUT_DEICE_STEP_INDOOR",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults()
    },    
    0x8204: {
        NASA_LABEL: "VAR_OUT_SENSOR_AIROUT",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x8206: {
        NASA_LABEL: "VAR_OUT_SENSOR_HIGHPRESS",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement='kgf/cm²',
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_PRESSURE,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_MULTIPLY: 0.1}]
        )
    },
    0x8208: {
        NASA_LABEL: "VAR_OUT_SENSOR_LOWPRESS",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement='kgf/cm²',
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_PRESSURE,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_MULTIPLY: 0.1}]
        )
    },
    0x820A: {
        NASA_LABEL: "VAR_OUT_SENSOR_DISCHARGE1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x8217: {
        NASA_LABEL: "VAR_OUT_SENSOR_CT1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
            filters=[{CONF_MULTIPLY: 0.1}]
        )
    },
    0x8218: {
        NASA_LABEL: "VAR_OUT_SENSOR_CONDOUT",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x821A: {
        NASA_LABEL: "VAR_OUT_SENSOR_SUCTION",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x821C: {
        NASA_LABEL: "VAR_OUT_SENSOR_DOUBLETUBE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x821E: {
        NASA_LABEL: "VAR_OUT_SENSOR_EVIIN",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x8220: {
        NASA_LABEL: "VAR_OUT_SENSOR_EVIOUT",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x8235: {
        NASA_LABEL: "VAR_OUT_ERROR_CODE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            accuracy_decimals=0,
            icon=ICON_ALERT,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            filters=[{CONF_DELTA: 1}]
        )
    },
    0x8236: {
        NASA_LABEL: "VAR_OUT_CONTROL_ORDER_CFREQ_COMP1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_HERTZ,
            icon=ICON_SINE_WAVE,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x8237: {
        NASA_LABEL: "VAR_OUT_CONTROL_TARGET_CFREQ_COMP1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_HERTZ,
            icon=ICON_SINE_WAVE,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x8238: {
        NASA_LABEL: "VAR_OUT_CONTROL_CFREQ_COMP1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_HERTZ,
            icon=ICON_SINE_WAVE,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x823B: {
        NASA_LABEL: "VAR_OUT_SENSOR_DCLINK_VOLTAGE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_FLASH,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x823D: {
        NASA_LABEL: "VAR_OUT_LOAD_FANRPM1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_REVOLUTIONS_PER_MINUTE,
            icon=ICON_FAN,
            accuracy_decimals=0, 
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x8240: {
        NASA_LABEL: "NASA_OUTDOOR_ODU_CAPA1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_FLASH,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x8254: {
        NASA_LABEL: "VAR_OUT_SENSOR_IPM1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x827A: {
        NASA_LABEL: "VAR_OUT_CONTROL_DSH1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x8280: {
        NASA_LABEL: "VAR_OUT_SENSOR_TOP1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x829F: {
        NASA_LABEL: "VAR_OUT_SENSOR_SAT_TEMP_HIGH_PRESSURE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x82A0: {
        NASA_LABEL: "VAR_OUT_SENSOR_SAT_TEMP_LOW_PRESSURE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x82DE: {
        NASA_LABEL: "VAR_OUT_SENSOR_EVAIN",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x82DF: {
        NASA_LABEL: "VAR_OUT_SENSOR_TW1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x82E0: {
        NASA_LABEL: "VAR_OUT_SENSOR_TW2",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: temp_sensor_defaults()
    },
    0x8411: {
        NASA_LABEL: "NASA_OUTDOOR_CONTROL_WATTMETER_1UNIT",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_WATT,
            icon=ICON_FLASH,
            accuracy_decimals=0, 
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT
        )
    },
    0x8413: {
        NASA_LABEL: "LVAR_OUT_CONTROL_WATTMETER_1W_1MIN_SUM",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_WATT,
            icon=ICON_FLASH,
            accuracy_decimals=1, 
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT            
        )        
    },
    0x8414: {
        NASA_LABEL: "LVAR_OUT_CONTROL_WATTMETER_ALL_UNIT_ACCUM",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: sensor_defaults(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            icon=ICON_COUNTER,
            accuracy_decimals=3, 
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            filters=[{CONF_MULTIPLY: 0.001}]
        )
    }
}
