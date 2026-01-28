import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from esphome.core import Lambda
from ..nasa.fsv import fsv
from ..nasa.selects import selects
from ..nasa.nasa import NASA_Select, available_as
from esphome.const import (
    CONF_DATA,
    CONF_DEFAULTS,
    CONF_ID,
    CONF_OPTIONS
)
from ..nasa.const import (
    NASA_FSV, 
    NASA_LABEL,
    NASA_LAMBDA_FROM,
    NASA_LAMBDA_TO,
    NASA_MESSAGE,
    NASA_MODE,
    NASA_TYPE
)
from .. import (
    nasa_item_base_schema,
    NASA_CONTROLLER_ID,  
    NASA_DEVICE_ID,
)


AUTO_LOAD = ["samsung_nasa"]
DEPENDENCIES = ["samsung_nasa"]

def validate(config):
    if (message := config.get(NASA_MESSAGE)) is not None:
        if (nasa_select := selects.get(message)) is None:
            types = available_as(message)
            if len(types):
                raise cv.Invalid("Wrong component for message {}. Re-implement as {}".format(message, ', '.join(types)))
            else:
                raise cv.Invalid("Invalid NASA message: {}".format(message))
    elif (fsvcode := config.get(NASA_FSV)) is not None:
        if (number := fsv.get(fsvcode)) is None:
           raise cv.Invalid("Invalid FSV code: {}".format(fsvcode))
        elif (nasa_select := selects.get(number)) is None:
            types = available_as(number)
            if len(types):
                raise cv.Invalid("Wrong component for FSV {}. Re-implement as {}".format(fsvcode, ', '.join(types)))
            else:
                raise cv.Invalid("Component could not be found for FSV {}".format(fsvcode))
        else:
            config[NASA_MESSAGE] = cv.hex_int(number)
    config[NASA_LABEL] = nasa_select[NASA_LABEL]
    config[NASA_MODE] = nasa_select[NASA_MODE]
    config[NASA_TYPE] = "select"
    entries = nasa_select[CONF_DEFAULTS]() | nasa_select[CONF_DATA]()
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
        "Auto configured NASA message {} as select component {}".format(config[NASA_MESSAGE], log_fsv)
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
    select.select_schema(NASA_Select)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(NASA_Select),
            cv.Optional(NASA_MESSAGE): cv.hex_int,
            cv.Optional(NASA_FSV): cv.int_range(1011, 5094),
            cv.Required(NASA_TYPE): cv.string_strict, 
            cv.Required(NASA_LAMBDA_FROM): cv.returning_lambda,
            cv.Required(NASA_LAMBDA_TO): cv.returning_lambda,
            cv.Required(CONF_OPTIONS): cv.ensure_list(str)
        }
    )
    .extend(nasa_item_base_schema)
)

async def to_code(config):
    lambda_expr_from = await cg.process_lambda(config[NASA_LAMBDA_FROM], [(cg.size_t, 'x')], return_type=cg.size_t)
    lambda_expr_to = await cg.process_lambda(config[NASA_LAMBDA_TO], [(cg.size_t,'x')], return_type=cg.size_t)
    device = await cg.get_variable(config[NASA_DEVICE_ID])
    controller = await cg.get_variable(config[NASA_CONTROLLER_ID])
    var_select = cg.new_Pvariable(
        config[CONF_ID],
        config[NASA_LABEL],
        config[NASA_MESSAGE],
        config[NASA_MODE],
        device
    )
    cg.add(var_select.set_lambdas(lambda_expr_from, lambda_expr_to))
    cg.add(var_select.set_parent(controller))
    await select.register_select(var_select, config, options=config[CONF_OPTIONS])
    cg.add(controller.register_component(var_select))

