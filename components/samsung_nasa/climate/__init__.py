import esphome.codegen as cg
import esphome.config_validation as cv
import esphome.automation as automation
from esphome.components import (
    climate, 
    sensor, 
    select,
    number,
    switch
)
from esphome.const import (
    CONF_ID,
    CONF_ICON,
    CONF_VALUE
)
from ..nasa.nasa import  (
    samsung_nasa_ns,
    NASA_Climate
)

CODEOWNERS = ["Beormund"]
AUTO_LOAD = ["samsung_nasa"]
DEPENDENCIES = ["samsung_nasa"]

ClimateAction = climate.climate_ns.enum("ClimateAction")
CLIMATE_ACTION = {
    "CLIMATE_ACTION_OFF": ClimateAction.CLIMATE_ACTION_OFF,
    "CLIMATE_ACTION_COOLING": ClimateAction.CLIMATE_ACTION_COOLING,
    "CLIMATE_ACTION_HEATING": ClimateAction.CLIMATE_ACTION_HEATING,
    "CLIMATE_ACTION_IDLE": ClimateAction.CLIMATE_ACTION_IDLE
}

# Actions
ClimateSetAction = samsung_nasa_ns.class_("ClimateSetAction", automation.Action)
ClimateActionMap = samsung_nasa_ns.class_("ClimateActionMap")

CLIMATE_POWER_SWITCH_ID = "power_switch_id"
CLIMATE_CURRENT_TEMP_ID = "current_temp_sensor_id"
CLIMATE_TARGET_TEMP_ID = "target_temp_number_id"
CLIMATE_ACTION_SENSOR = "action_mode_sensor"
CLIMATE_CUSTOM_PRESET_SELECT_ID = "custom_preset_select_id"
CLIMATE_ACTION_MAPPINGS_ID = "mappings_id"
CLIMATE_ACTION_MAPPINGS = "mappings"
CLIMATE_MODE_SELECT_ID = "mode_select_id"
CLIMATE_SUPPORTED_MODES = "supported_modes"
ICON_THERMOSTAT = "mdi:thermostat"

def to_pair_schema(config):
    return cv.All(
        {
            cv.Required("key"): cv.int_,
            cv.Required("value"): cv.enum(CLIMATE_ACTION, upper=True)
        }
    )(config)

def validate_mapping(config):
    if not isinstance(config, dict):
        raise cv.Invalid("A dictionary is required. E.g. 1: CLIMATE_ACTION_IDLE")
    d = {}
    for key, value in config.items():
        pair = to_pair_schema({"key": key, "value": value})
        d[pair['key']] = pair['value']
    return d

CLIMATE_ACTION_MAPPING_SCHEMA = cv.Schema(
    {
         cv.Required(CONF_ID): cv.use_id(sensor.Sensor),
         cv.GenerateID(CLIMATE_ACTION_MAPPINGS_ID): cv.declare_id(ClimateActionMap),
         cv.Required(CLIMATE_ACTION_MAPPINGS): validate_mapping
    }
)

CONFIG_SCHEMA = cv.Schema(
    climate.climate_schema(NASA_Climate)
    .extend(
        {  
            cv.Optional(CONF_ICON, default=ICON_THERMOSTAT): cv.icon,
            cv.Optional(CLIMATE_POWER_SWITCH_ID): cv.use_id(switch.Switch),
            cv.Optional(CLIMATE_MODE_SELECT_ID): cv.use_id(select.Select),
            cv.Optional(CLIMATE_CURRENT_TEMP_ID): cv.use_id(sensor.Sensor),
            cv.Optional(CLIMATE_TARGET_TEMP_ID): cv.use_id(number.Number),
            cv.Optional(CLIMATE_ACTION_SENSOR): CLIMATE_ACTION_MAPPING_SCHEMA,
            cv.Optional(CLIMATE_CUSTOM_PRESET_SELECT_ID): cv.use_id(select.Select),
            cv.Optional(CLIMATE_SUPPORTED_MODES): cv.ensure_list(climate.validate_climate_mode),
        }
    )
)

CLIMATE_ACTION_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.use_id(NASA_Climate),
        cv.Required(CONF_VALUE): cv.templatable(
            cv.enum(CLIMATE_ACTION, upper=True)
        ),
    }
)

@automation.register_action("climate.action", ClimateSetAction, CLIMATE_ACTION_SCHEMA)
async def climate_action_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    if (action := config[CONF_VALUE]) is not None:
        template_ = await cg.templatable(action, args, ClimateAction)
        cg.add(var.set_value(template_))
    return var

async def to_code(config):
    var = await climate.new_climate(config)
    await cg.register_component(var, config)
    if CLIMATE_POWER_SWITCH_ID in config:
        power = await cg.get_variable(config[CLIMATE_POWER_SWITCH_ID])
        cg.add(var.set_power_switch(power))
    if CLIMATE_MODE_SELECT_ID in config:
        mode_sel = await cg.get_variable(config[CLIMATE_MODE_SELECT_ID])
        cg.add(var.set_mode_select(mode_sel))
    if CLIMATE_SUPPORTED_MODES in config:
        cg.add(var.set_supported_modes(config[CLIMATE_SUPPORTED_MODES]))
    if CLIMATE_CURRENT_TEMP_ID in config:
        current = await cg.get_variable(config[CLIMATE_CURRENT_TEMP_ID])
        cg.add(var.set_current_temp(current))
    if CLIMATE_TARGET_TEMP_ID in config:
        target = await cg.get_variable(config[CLIMATE_TARGET_TEMP_ID])
        cg.add(var.set_target_temp(target))
    if CLIMATE_CUSTOM_PRESET_SELECT_ID in config:
        custpre = await cg.get_variable(config[CLIMATE_CUSTOM_PRESET_SELECT_ID])
        cg.add(var.set_custom_preset_select(custpre))
    if (ams := config.get(CLIMATE_ACTION_SENSOR)) is not None:
        if (action_id := ams.get(CONF_ID)) is not None:
            if (mapping_id := ams.get(CLIMATE_ACTION_MAPPINGS_ID)) is not None:
                if (cam := ams.get(CLIMATE_ACTION_MAPPINGS)) is not None:
                    var_action = await cg.get_variable(action_id)
                    cg.add(var.set_action_sensor(var_action))
                    var_map = cg.new_Pvariable(mapping_id)
                    for key, value in cam.items():                       
                        cg.add(var_map.add_map_entry(key, value))
                    cg.add(var.set_action_map(var_map))
