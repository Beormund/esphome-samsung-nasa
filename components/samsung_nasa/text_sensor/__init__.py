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

AUTO_LOAD = ["samsung_nasa"]
DEPENDENCIES = ["samsung_nasa"]

def validate(config):
    if NASA_MESSAGE not in config:
        return config

    nasa_message = config[NASA_MESSAGE]
    # Fetch from text_sensors.py dictionary
    nasa_text_sensor = text_sensors.get(nasa_message)

    # --- Sensor found → Auto-Config ---
    if nasa_text_sensor is not None:
        config[NASA_LABEL] = nasa_text_sensor.get(NASA_LABEL)
        config[NASA_MODE] = nasa_text_sensor.get(NASA_MODE)

        # If the user didn't provide a 'name' in YAML, use our dict's name
        if CONF_NAME not in config and CONF_NAME in nasa_text_sensor:
             config[CONF_NAME] = nasa_text_sensor[CONF_NAME]

        # Load preset values (Icons, Entity Category)
        defaults_fn = nasa_text_sensor.get(CONF_DEFAULTS)
        if callable(defaults_fn):
            defaults = defaults_fn() or {}
            for key, value in defaults.items():
                config.setdefault(key, value)
    
    # --- Unknown sensor ---
    else:
        config.setdefault(
            NASA_LABEL,
            nasa_labels.get(nasa_message, "NASA_UNKNOWN_LABEL")
        )

    # --- Logging ---
    label = "Auto" if nasa_text_sensor else "User"
    cv._LOGGER.log(
        cv.logging.INFO,
        "{} configured NASA message {} as text sensor component"
        .format(label, hex(nasa_message))
    )

    return config

CONFIG_SCHEMA = cv.All(
    cv.Schema({cv.Required(NASA_MESSAGE): cv.hex_int}, extra=cv.ALLOW_EXTRA),
    validate,
    text_sensor.text_sensor_schema(NASA_TextSensor)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(NASA_TextSensor),
            cv.Required(NASA_MESSAGE): cv.hex_int,
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

    # Inject the lookup logic (the switch statement)
    spec = text_sensors.get(config[NASA_MESSAGE])
    if spec and NASA_MAPPING in spec:
        lookup_code = "switch(x) {\n"
        for val, text in spec[NASA_MAPPING].items():
            # Standardizing quotes for C++
            lookup_code += f'  case {val}: return "{text}";\n'
        lookup_code += '  default: return "Unknown (" + std::to_string(x) + ")";\n}'

        cg.add(var.set_lookup_logic(cg.RawExpression(
            f"[](long x) -> std::string {{ {lookup_code} }}"
        )))

    cg.add(var.set_parent(controller))
    cg.add(controller.register_component(var))
