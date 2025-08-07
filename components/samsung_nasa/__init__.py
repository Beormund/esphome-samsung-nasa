from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome import pins
from esphome.cpp_helpers import gpio_pin_expression
from .nasa.const import ADDRESS_CLASS_UNDEFINED
from esphome.const import (
    CONF_ID, 
    CONF_FLOW_CONTROL_PIN
)
import re
from .nasa.const import (
    NASA_LABEL,
    NASA_MODE
)
from .nasa.nasa import (
    samsung_nasa_ns, 
    controller_mode,
    CONTROLLER_MODE_STATUS, 
    ADDRESS_CLASSES,
    NASA_Base
)


MULTI_CONF = False
CODEOWNERS = ["Beormund"]
DEPENDENCIES = ["uart"]

NASA_Controller = samsung_nasa_ns.class_("NASA_Controller", cg.PollingComponent)
NASA_Request_Read_Action = samsung_nasa_ns.class_("NASA_Request_Read_Action")
NASA_Client = samsung_nasa_ns.class_("NASA_Client", cg.PollingComponent, uart.UARTDevice)
NASA_Device = samsung_nasa_ns.class_("NASA_Device")
NASA_CONTROLLER_ID = "nasa_controller_id"
NASA_CLIENT = "nasa_client"
NASA_CLIENT_ID =  "nasa_client_id"
NASA_SILENCE_INTERVAL = "silence_interval"
NASA_RETRY_INTERVAL = "retry_interval"
NASA_MIN_RETRIES = "min_retries"
NASA_SEND_TIMEOUT = "send_timeout"
NASA_DEVICE_ID = "nasa_device_id"
NASA_DEVICE_ADDRESS = "address"
NASA_DEVICE_CLASS = "class"
NASA_DEVICES = "devices"
NASA_DEBUG_LOG_MESSAGES = "debug_log_messages"
NASA_DEBUG_LOG_MESSAGES_RAW = "debug_log_messages_raw"
NASA_DEBUG_LOG_UNDEFINED_MESSAGES = "debug_log_undefined_messages"
address_pattern = re.compile("([0-9a-f]{2})(?:\\.[0-9a-f]{2}){2}", re.IGNORECASE)

def device_validator(config):
    if (m := address_pattern.match(config[NASA_DEVICE_ADDRESS])) is not None:
        group = m.group(1)
        address_class = cv.hex_int(int(group,16))
        address_label = ADDRESS_CLASSES.get(
            cv.hex_int(int(group,16)),
            ADDRESS_CLASSES[ADDRESS_CLASS_UNDEFINED])
        config[NASA_DEVICE_CLASS] = address_class
        cv._LOGGER.log(
            cv.logging.INFO, 
            "Auto configured NASA device {} as {} unit ({})".format(
                config[NASA_DEVICE_ADDRESS], address_label, address_class
            )
        )
    else:
        raise cv.Invalid("Device address invalid. Valid example: 20.00.00")
    return config

device_schema = cv.All(    
    cv.Schema(
        {        
            cv.GenerateID(): cv.declare_id(NASA_Device),
            cv.Required(NASA_DEVICE_ADDRESS):cv.string_strict
        }
    ),
    device_validator,
)

client_schema = cv.Schema(
    {
        cv.GenerateID(NASA_CLIENT_ID): cv.declare_id(NASA_Client),
        cv.Optional(CONF_FLOW_CONTROL_PIN): pins.gpio_output_pin_schema,
        cv.Optional(NASA_SILENCE_INTERVAL, default=100): cv.int_range(50, 1000),
        cv.Optional(NASA_RETRY_INTERVAL, default=500): cv.int_range(200, 5000),
        cv.Optional(NASA_MIN_RETRIES, default= 1): cv.int_range(1, 10),
        cv.Optional(NASA_SEND_TIMEOUT, default=4000): cv.int_range(1000, 10000)                    
    }
)


CONFIG_SCHEMA = cv.Schema(
        {
            cv.GenerateID(NASA_CONTROLLER_ID): cv.declare_id(NASA_Controller),
            cv.Required(NASA_CLIENT): client_schema,
            cv.Optional(NASA_DEBUG_LOG_MESSAGES, default=False): cv.boolean,
            cv.Optional(NASA_DEBUG_LOG_MESSAGES_RAW, default=False): cv.boolean,
            cv.Optional(NASA_DEBUG_LOG_UNDEFINED_MESSAGES, default=False): cv.boolean,
            cv.Required(NASA_DEVICES): cv.ensure_list(device_schema)
        }
    ).extend(uart.UART_DEVICE_SCHEMA).extend(cv.polling_component_schema("30s"))


nasa_item_base_schema = cv.Schema( 
    {
        cv.GenerateID(NASA_CONTROLLER_ID): cv.use_id(NASA_Controller),
        cv.Required(NASA_DEVICE_ID): cv.use_id(NASA_Device),
        cv.Required(NASA_LABEL): cv.string_strict,
        cv.Optional(NASA_MODE, default=CONTROLLER_MODE_STATUS): controller_mode
    }    
)

@automation.register_action(
    "samsung_nasa.request_read",
    NASA_Request_Read_Action,
    cv.All(
        cv.Schema(
            {
                cv.GenerateID(NASA_CONTROLLER_ID): cv.use_id(NASA_Controller),
                cv.Required(CONF_ID): cv.ensure_list(cv.use_id(NASA_Base))
            }
        )
    )
)
async def request_read_to_code(config, action_id, template_arg, args):
    parent = await cg.get_variable(config[NASA_CONTROLLER_ID])
    comps = []
    for ID in config[CONF_ID]:
        comp = await cg.get_variable(ID)
        comps.append(comp)
    var = cg.new_Pvariable(action_id, template_arg, parent)
    cg.add(var.request_read(comps))
    return var

async def to_code(config):
    conf_client = config[NASA_CLIENT]
    client_var = cg.new_Pvariable(conf_client[NASA_CLIENT_ID])
    if (conf_pin:= conf_client.get(CONF_FLOW_CONTROL_PIN)) is not None:
        pin = await gpio_pin_expression(conf_pin)
        cg.add(client_var.set_flow_control_pin(pin))
    if (silence_interval := conf_client.get(NASA_SILENCE_INTERVAL)) is not None:
        cg.add(client_var.set_silence_interval(silence_interval))
    if (retry_interval := conf_client.get(NASA_RETRY_INTERVAL)) is not None:
        cg.add(client_var.set_retry_interval(retry_interval))
    if (min_retries := conf_client.get(NASA_MIN_RETRIES)) is not None:
        cg.add(client_var.set_min_retries(min_retries))
    if (send_timeout := conf_client.get(NASA_SEND_TIMEOUT)) is not None:
        cg.add(client_var.set_send_timeout(send_timeout))    
    controller = cg.new_Pvariable(config[NASA_CONTROLLER_ID], client_var)
    cg.add(controller.set_debug_log_messages(config[NASA_DEBUG_LOG_MESSAGES]))
    cg.add(controller.set_debug_log_messages_raw(config[NASA_DEBUG_LOG_MESSAGES_RAW]))
    cg.add(controller.set_debug_log_undefined_messages(config[NASA_DEBUG_LOG_UNDEFINED_MESSAGES]))
    for device in config[NASA_DEVICES]:
        var_device = cg.new_Pvariable(
            device[CONF_ID], 
            device[NASA_DEVICE_ADDRESS],
            device[NASA_DEVICE_CLASS]
        )
        cg.add(controller.register_device(var_device))
    await cg.register_component(controller, config)
    await cg.register_component(client_var, conf_client)
    await uart.register_uart_device(client_var, config)