import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.core import Lambda
from esphome.const import  CONF_DATA,CONF_DEFAULTS
from ..nasa.nasa import NASA_Switch, available_as
from ..nasa.fsv import fsv
from ..nasa.switches import switches
from ..nasa.const import (
    NASA_FSV, 
    NASA_LABEL,
    NASA_LAMBDA_FROM,
    NASA_LAMBDA_TO,
    NASA_MESSAGE,
    NASA_MODE
)
from .. import (
    nasa_item_base_schema,
    NASA_CONTROLLER_ID,
    NASA_DEVICE_ID
)


AUTO_LOAD = ["samsung_nasa"]
DEPENDENCIES = ["samsung_nasa"]

def validate(config, switches_map=None, fsv_map=None, available_as_func=None):
    """
    Validate a NASA switch configuration.
    Optional user-defined mappings and filter function can be provided.
    """
    switches_map = switches_map or switches
    fsv_map = fsv_map or fsv
    available_as_func = available_as_func or available_as

    nasa_switch = None

    # Resolve NASA_MESSAGE
    if (message := config.get(NASA_MESSAGE)) is not None:
        nasa_switch = switches_map.get(message)
        if nasa_switch is None:
            types = available_as_func(message)
            if types:
                raise cv.Invalid(
                    f"Wrong component type for NASA message {message}. "
                    f"Please re-implement as: {', '.join(types)}"
                )
            raise cv.Invalid(f"Invalid NASA message: {message}")

    # Resolve NASA_FSV
    elif (fsvcode := config.get(NASA_FSV)) is not None:
        number = fsv_map.get(fsvcode)
        if number is None:
            raise cv.Invalid(f"Invalid FSV code: {fsvcode}")

        nasa_switch = switches_map.get(number)
        if nasa_switch is None:
            types = available_as_func(number)
            if types:
                raise cv.Invalid(
                    f"Wrong component type for FSV {fsvcode}. "
                    f"Please re-implement as: {', '.join(types)}"
                )
            raise cv.Invalid(f"No suitable component found for FSV code {fsvcode}")
        config[NASA_MESSAGE] = cv.hex_int(number)

    # Ensure a valid switch was resolved
    if not nasa_switch:
        raise cv.Invalid("Unable to determine a valid NASA switch from the configuration")

    # Apply static metadata (do not overwrite user values)
    config.setdefault(NASA_LABEL, nasa_switch[NASA_LABEL])
    config.setdefault(NASA_MODE, nasa_switch[NASA_MODE])

    # Merge defaults and data entries
    entries = nasa_switch.get(CONF_DEFAULTS, lambda: {})() | nasa_switch.get(CONF_DATA, lambda: {})()
    for key, value in entries.items():
        config.setdefault(key, value)

    # Convert lambda strings to Lambda objects
    if (nasa_lambda_from := config.get(NASA_LAMBDA_FROM)) is not None:
        config[NASA_LAMBDA_FROM] = Lambda(nasa_lambda_from)

    if (nasa_lambda_to := config.get(NASA_LAMBDA_TO)) is not None:
        config[NASA_LAMBDA_TO] = Lambda(nasa_lambda_to)

    # Logging
    if (fsvcode := config.get(NASA_FSV)) is not None:
        log_fsv = "[FSV {}]".format(fsvcode)
    else:
        log_fsv = ""
    cv._LOGGER.log(
        cv.logging.INFO, 
        "Auto configured NASA message {} as switch component {}".format(config[NASA_MESSAGE], log_fsv)
    )

    return config

nasa_schema = cv.All(
    cv.Schema(
        {
            cv.Optional(NASA_MESSAGE): cv.hex_int,
            cv.Optional(NASA_FSV): cv.int_range(1011, 5094)
        },
        extra=cv.ALLOW_EXTRA,
    ),
    cv.has_at_most_one_key(NASA_MESSAGE, NASA_FSV),
    validate
)

CONFIG_SCHEMA = cv.All(
    nasa_schema,
    switch.switch_schema(NASA_Switch)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(NASA_Switch),
            cv.Optional(NASA_MESSAGE): cv.hex_int,
            cv.Optional(NASA_FSV): cv.int_range(1011, 5094), 
            cv.Required(NASA_LAMBDA_FROM): cv.returning_lambda,
            cv.Required(NASA_LAMBDA_TO): cv.returning_lambda,
        }
    )
    .extend(nasa_item_base_schema)
)

async def to_code(config):
    lambda_expr_from = await cg.process_lambda(config[NASA_LAMBDA_FROM], [(cg.int_, 'x')], return_type=cg.bool_)
    lambda_expr_to = await cg.process_lambda(config[NASA_LAMBDA_TO], [(cg.bool_,'x')], return_type=cg.int_)
    device = await cg.get_variable(config[NASA_DEVICE_ID])
    controller = await cg.get_variable(config[NASA_CONTROLLER_ID])
    var_switch = await switch.new_switch(
        config,
        config[NASA_LABEL],
        config[NASA_MESSAGE],
        config[NASA_MODE],
        device
    )
    cg.add(var_switch.set_lambdas(lambda_expr_from, lambda_expr_to))
    cg.add(var_switch.set_parent(controller))
    cg.add(controller.register_component(var_switch))

