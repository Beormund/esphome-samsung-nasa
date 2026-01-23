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
    MODEL_REGISTRY,
    NASA_CONTROLLER_ID,
    NASA_DEVICE_ID,
    nasa_item_base_schema
)
from ..nasa.const import (
    CONF_OVERRIDES,
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

def validate(config):
    if (message := config.get(NASA_MESSAGE)) is not None:
        if (nasa_number := numbers.get(message)) is None:
            types = available_as(message)
            if len(types):
                raise cv.Invalid("Wrong component for message {}. Re-implement as {}".format(message, ', '.join(types)))
            else:
                raise cv.Invalid("Invalid NASA message: {}".format(message))
    elif (fsvcode := config.get(NASA_FSV)) is not None:
        if (number := fsv.get(fsvcode)) is None:
           raise cv.Invalid("Invalid FSV code: {}".format(fsvcode))
        elif (nasa_number := numbers.get(number)) is None:
            types = available_as(number)
            if len(types):
                raise cv.Invalid("Wrong component for FSV {}. Re-implement as {}".format(fsvcode, ', '.join(types)))
            else:
                raise cv.Invalid("Component could not be found for FSV {}".format(fsvcode))
        else:
            config[NASA_MESSAGE] = cv.hex_int(number)
            
    config[NASA_LABEL] = nasa_number[NASA_LABEL]
    config[NASA_MODE] = nasa_number[NASA_MODE]
    entries = nasa_number[CONF_DEFAULTS]() | nasa_number[CONF_DATA]()

    for key, value in entries.items():
        config[key] = value
    if (nasa_lambda_from := config.get(NASA_LAMBDA_FROM)) is not None:
         config[NASA_LAMBDA_FROM] = Lambda(nasa_lambda_from)
    if (nasa_lambda_to := config.get(NASA_LAMBDA_TO)) is not None:
        config[NASA_LAMBDA_TO] = Lambda(nasa_lambda_to)
    if (fsvcode := config.get(NASA_FSV)) is not None:
        log_fsv = "[FSV {}]".format(fsvcode)
    else:
        log_fsv = ""
    cv._LOGGER.log(
        cv.logging.INFO, 
        "Auto configured NASA message {} as number component {}".format(config[NASA_MESSAGE], log_fsv)
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

    controller_id_str = str(config[NASA_CONTROLLER_ID])
    selected_model = MODEL_REGISTRY.get(controller_id_str, "STANDARD")

    message_hex = config[NASA_MESSAGE]
    nasa_number = numbers.get(message_hex)

    # Start with the defaults from the YAML (which came from numbers.py)
    min_val = config[CONF_MIN_VALUE]
    max_val = config[CONF_MAX_VALUE]

    # Apply overrides if they exist for this specific model
    if nasa_number and CONF_OVERRIDES in nasa_number:
        if selected_model in nasa_number[CONF_OVERRIDES]:
            m_overrides = nasa_number[CONF_OVERRIDES][selected_model]
            min_val = m_overrides.get(CONF_MIN_VALUE, min_val)
            max_val = m_overrides.get(CONF_MAX_VALUE, max_val)

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
        min_value=min_val,
        max_value=max_val,
        step=config[CONF_STEP]
    )
    cg.add(var_number.set_lambdas(lambda_expr_from, lambda_expr_to))
    cg.add(var_number.set_parent(controller))
    cg.add(controller.register_component(var_number))
