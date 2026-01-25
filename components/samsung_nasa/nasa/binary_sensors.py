from esphome.const import (
    DEVICE_CLASS_EMPTY,
    CONF_ENTITY_CATEGORY,
    CONF_DEFAULTS,
    CONF_DEVICE_CLASS,
    DEVICE_CLASS_HEAT,
    ENTITY_CATEGORY_NONE,
    CONF_ICON,
    CONF_FILTERS,
    ICON_EMPTY
)
from .const import (
    NASA_LABEL,
    NASA_MODE,
    CONTROLLER_MODE_STATUS
)

def binary_sensor_defaults(
    icon = ICON_EMPTY,
    device_class = DEVICE_CLASS_EMPTY,
    entity_category = ENTITY_CATEGORY_NONE,
    filters = []
):
    return lambda: {
        CONF_ICON: icon,
        CONF_DEVICE_CLASS: device_class,
        CONF_ENTITY_CATEGORY: entity_category,
        CONF_FILTERS: filters
    }

ICON_HEAT = "mdi:heat-wave"
ICON_VALVE = "mdi:valve"
ICON_COMPRESSOR = "mdi:heat-pump"
ICON_HOT_GAS = "mdi:gas-burner"
ICON_LIQUID = "mdi:cup-water"
ICON_VAPOUR = "mdi:waves-arrow-up"
ICON_THERMOSTAT = "mdi:thermostat-cog"
ICON_DEFROST = "mdi:snowflake-melt"
ICON_PUMP = "mdi:pump"

binary_sensors = {
    0x4028: {
        NASA_LABEL: "ENUM_IN_STATE_THERMO",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon=ICON_COMPRESSOR)
    },
    0x402E: {
        CONF_ICON: ICON_HEAT,
        NASA_LABEL: "ENUM_IN_STATE_DEFROST_MODE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_DEFROST)
    },
    0x4067: {
        NASA_LABEL: "ENUM_IN_3WAY_VALVE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_VALVE)
    },
    0x406C: {
        CONF_ICON: ICON_HEAT,
        NASA_LABEL: "ENUM_IN_BACKUP_HEATER",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(
            icon = ICON_HEAT,
            device_class = DEVICE_CLASS_HEAT
        )
    },
    0x406F: {
        NASA_LABEL: "ENUM_IN_REFERENCE_EHS_TEMP",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_THERMOSTAT)
    },
    0x4087: {
        NASA_LABEL: "ENUM_IN_BOOSTER_HEATER",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(
            icon = ICON_HEAT,
            device_class = DEVICE_CLASS_HEAT
        )
    },
    0x4089: {
        NASA_LABEL: "ENUM_IN_STATE_WATER_PUMP",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_PUMP)
    },
    0x8010: {
        NASA_LABEL: "ENUM_OUT_LOAD_COMP1",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_COMPRESSOR)
    },
    0x8017: {
        NASA_LABEL: "ENUM_OUT_LOAD_HOTGAS",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_HOT_GAS)
    },
    0x8019: {
        NASA_LABEL: "ENUM_OUT_LOAD_LIQUID",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_LIQUID)
    },
    0x8021: {
        NASA_LABEL: "ENUM_OUT_LOAD_EVI_BYPASS",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_VAPOUR)
    },
    0x801A: {
        NASA_LABEL: "ENUM_OUT_LOAD_4WAY",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(icon = ICON_VALVE)
    },
    0x80AF: {
        NASA_LABEL: "BASE_HEATER",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(
            icon = ICON_HEAT,
            device_class = DEVICE_CLASS_HEAT
        )
    },
    0x80D7: {
        NASA_LABEL: "ENUM_OUT_LOAD_PHEHEATER",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_DEFAULTS: binary_sensor_defaults(
            icon = ICON_HEAT,
            device_class = DEVICE_CLASS_HEAT
        )
    }
}