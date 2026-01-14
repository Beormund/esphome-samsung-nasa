import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.core import Lambda
from ..nasa.nasa import  NASA_Number, available_as
from esphome.const import (
    CONF_DATA,
    CONF_DEFAULTS,
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_STEP,
)
from .. import (
    NASA_CONTROLLER_ID,
    NASA_DEVICE_ID,
    nasa_item_base_schema
)
from ..nasa.const import (
    NASA_MESSAGE,
    NASA_LABEL,
    NASA_MODE,
    NASA_FSV,
    NASA_LAMBDA_FROM,
    NASA_LAMBDA_TO
)
from ..nasa.fsv import fsv
from ..nasa.numbers import numbers


AUTO_LOAD = ["samsung_nasa"]
DEPENDENCIES = ["samsung_nasa"]

def validate(
    config,
    numbers_map=None,        # User-defined mapping table for NASA messages
    fsv_map=None,            # User-defined mapping table for FSV codes
    available_as_func=None   # Function to check alternative component types
):
    # Fallback to defaults if nothing is provided
    numbers_map = numbers_map or numbers
    fsv_map = fsv_map or fsv
    available_as_func = available_as_func or available_as

    nasa_number = None

    # Check NASA_MESSAGE
    if (message := config.get(NASA_MESSAGE)) is not None:
        if (nasa_number := numbers_map.get(message)) is None:
            types = available_as_func(message)
            if types:
                raise cv.Invalid(
                    f"Wrong component type for NASA message {message}. "
                    f"Please re-implement it as: {', '.join(types)}"
                )
            else:
                raise cv.Invalid(f"Invalid NASA message: {message}")

    # Check NASA_FSV
    elif (fsvcode := config.get(NASA_FSV)) is not None:
        if (number := fsv_map.get(fsvcode)) is None:
            raise cv.Invalid(f"Invalid FSV code: {fsvcode}")
        elif (nasa_number := numbers_map.get(number)) is None:
            types = available_as_func(number)
            if types:
                raise cv.Invalid(
                    f"Wrong component type for FSV {fsvcode}. "
                    f"Please re-implement it as: {', '.join(types)}"
                )
            else:
                raise cv.Invalid(
                    f"No suitable component found for FSV code {fsvcode}"
                )
        else:
            config[NASA_MESSAGE] = cv.hex_int(number)

    # Ensure a valid NASA number was resolved
    if not nasa_number:
        raise cv.Invalid("Unable to determine a valid NASA message from the configuration")

    # Apply static metadata
    config[NASA_LABEL] = nasa_number[NASA_LABEL]
    config[NASA_MODE] = nasa_number[NASA_MODE]

    # Merge default and data entries
    entries = (
        nasa_number.get(CONF_DEFAULTS, lambda: {})()
        | nasa_number.get(CONF_DATA, lambda: {})()
    )
    for key, value in entries.items():
        config.setdefault(key, value)

    # Convert lambda strings to Lambda objects if present
    if (nasa_lambda_from := config.get(NASA_LAMBDA_FROM)) is not None:
        config[NASA_LAMBDA_FROM] = Lambda(nasa_lambda_from)

    if (nasa_lambda_to := config.get(NASA_LAMBDA_TO)) is not None:
        config[NASA_LAMBDA_TO] = Lambda(nasa_lambda_to)

    # Logging
    log_fsv = f"[FSV {config[NASA_FSV]}]" if config.get(NASA_FSV) else ""

    cv._LOGGER.log(
        cv.logging.INFO,
        f"Auto-configured NASA message {config[NASA_MESSAGE]} "
        f"as number component {log_fsv}"
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
    number.number_schema(NASA_Number)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(NASA_Number),
            cv.Optional(NASA_MESSAGE): cv.hex_int,
            cv.Optional(NASA_FSV): cv.int_range(1011, 5094),      
            cv.Required(CONF_MAX_VALUE): cv.float_,
            cv.Required(CONF_MIN_VALUE): cv.float_,
            cv.Required(CONF_STEP): cv.positive_float,
            cv.Required(NASA_LAMBDA_FROM): cv.returning_lambda,
            cv.Required(NASA_LAMBDA_TO): cv.returning_lambda,
        }
    )
    .extend(nasa_item_base_schema)
)

async def to_code(config):
    lambda_expr_from = await cg.process_lambda(config[NASA_LAMBDA_FROM], [(float, 'x')], return_type=cg.float_)
    lambda_expr_to = await cg.process_lambda(config[NASA_LAMBDA_TO], [(float,'x')], return_type=cg.uint16)
    device = await cg.get_variable(config[NASA_DEVICE_ID])
    controller = await cg.get_variable(config[NASA_CONTROLLER_ID])
    var_number = await number.new_number(
        config,
        config[NASA_LABEL],
        config[NASA_MESSAGE],
        config[NASA_MODE],
        device,
        min_value=config[CONF_MIN_VALUE],
        max_value=config[CONF_MAX_VALUE],
        step=config[CONF_STEP]
    )
    cg.add(var_number.set_lambdas(lambda_expr_from, lambda_expr_to))
    cg.add(var_number.set_parent(controller))
    cg.add(controller.register_component(var_number))

    

