import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_DEFAULTS, CONF_ID, CONF_NAME
from ..nasa.nasa import NASA_TextSensor
from ..nasa.nasa_labels import nasa_labels
from ..nasa.const import (
    NASA_LABEL,
    NASA_MAPPING,
    NASA_MESSAGE,
    NASA_MODE,
)
from .. import (
    nasa_item_base_schema,
    NASA_CONTROLLER_ID,
    NASA_DEVICE_ID
)
from ..nasa.text_sensors import text_sensors

CONF_STRUCTURE_FORMAT = "structure_format"
STRUCTURE_FORMATS = {"hex": 0, "dbcode": 1, "product_option": 2, "dbcode_inverter": 3}
# Defaults for structure messages whose layout was verified against Samsung S-NET Pro 2
STRUCTURE_FORMAT_DEFAULTS = {
    0x0600: "product_option",  # Product option: [0]12300-[1]10000-[2]00000-[3]00002
    0x0608: "dbcode",          # Main micom: DB91-02103B 231108
    0x060C: "dbcode",          # EEPROM version: DB82-07086A 220622
    0x8601: "dbcode_inverter", # Inverter micom: DB91-02411A 100004 (bytes 0-3 and 8-10)
}

AUTO_LOAD = ["samsung_nasa"]
DEPENDENCIES = ["samsung_nasa"]

def validate(config):
    if NASA_MESSAGE not in config:
        return config

    nasa_message = config[NASA_MESSAGE]
    nasa_text_sensor = text_sensors.get(nasa_message)

    # 1. Basic Defaults
    if nasa_text_sensor is not None:
        config[NASA_LABEL] = nasa_text_sensor.get(NASA_LABEL)
        config[NASA_MODE] = nasa_text_sensor.get(NASA_MODE)

        if CONF_NAME not in config and CONF_NAME in nasa_text_sensor:
             config.setdefault(CONF_NAME, nasa_text_sensor[CONF_NAME])

        defaults_fn = nasa_text_sensor.get(CONF_DEFAULTS)
        if callable(defaults_fn):
            defaults = defaults_fn() or {}
            for key, value in defaults.items():
                config.setdefault(key, value)
    else:
        config.setdefault(
            NASA_LABEL,
            nasa_labels.get(nasa_message, "NASA_UNKNOWN_LABEL")
        )

    # 2. Intelligent Mapping Merge
    library_mapping = nasa_text_sensor.get(NASA_MAPPING, {}) if nasa_text_sensor else {}
    user_mapping = config.get(NASA_MAPPING, {})

    if library_mapping or user_mapping:
        # We create a new dict starting with library values, 
        # then overwritten/extended by user values.
        merged_mapping = {**library_mapping, **user_mapping}
        config[NASA_MAPPING] = merged_mapping

    # 3. Enhanced Logging
    source = "Auto" if nasa_text_sensor else "User"
    log_msg = f"{source} configured NASA message {hex(nasa_message)} as text sensor component"
    
    if user_mapping and library_mapping:
        cv._LOGGER.info("%s: Merged user mapping with library defaults", log_msg)
    elif user_mapping:
        cv._LOGGER.info("%s: Using custom user mapping", log_msg)
    elif library_mapping:
        cv._LOGGER.info("%s: Using library mapping", log_msg)
    else:
        cv._LOGGER.info("%s: No mapping applied", log_msg)

    return config

CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.Required(NASA_MESSAGE): cv.hex_int,
        cv.Optional(NASA_MAPPING): cv.Schema({cv.hex_int: cv.string_strict}),
        cv.Optional(CONF_STRUCTURE_FORMAT): cv.one_of(*STRUCTURE_FORMATS, lower=True),
    }, extra=cv.ALLOW_EXTRA),
    validate,
    text_sensor.text_sensor_schema(NASA_TextSensor)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(NASA_TextSensor),
            cv.Required(NASA_MESSAGE): cv.hex_int,
            cv.Optional(NASA_MAPPING): cv.Schema({cv.hex_int: cv.string_strict}),
            cv.Optional(CONF_STRUCTURE_FORMAT): cv.one_of(*STRUCTURE_FORMATS, lower=True),
        }
    )
    .extend(nasa_item_base_schema)
)

async def to_code(config):
    device = await cg.get_variable(config[NASA_DEVICE_ID])
    controller = await cg.get_variable(config[NASA_CONTROLLER_ID])
    
    # Use the official text_sensor helper instead of manual Pvariable
    var = await text_sensor.new_text_sensor(
        config,
        config[NASA_LABEL],
        config[NASA_MESSAGE],
        config[NASA_MODE],
        device
    )

    if NASA_MAPPING in config:
        mapping = config[NASA_MAPPING]
        lookup_code = "switch(x) {\n"
        for val, text in mapping.items():
            lookup_code += f'  case {val}: return "{text}";\n'
        lookup_code += '  default: return "Unknown (" + std::to_string(x) + ")";\n}'

        cg.add(var.set_lookup_logic(cg.RawExpression(
            f"[](long x) -> std::string {{ {lookup_code} }}"
        )))

    fmt = config.get(CONF_STRUCTURE_FORMAT, STRUCTURE_FORMAT_DEFAULTS.get(config[NASA_MESSAGE], "hex"))
    if fmt != "hex":
        cg.add(var.set_structure_format(STRUCTURE_FORMATS[fmt]))

    cg.add(var.set_parent(controller))
    cg.add(controller.register_component(var))
