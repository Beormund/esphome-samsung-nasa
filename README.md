# ESPHome / Home Assistant Samsung Heat Pump Integration

If you find this useful please consider supporting me by buying me a coffee. Thank you!

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/jvn5gy8fdy)

This component enables Samsung Heat Pumps to be integrated into ESPHome and Home Assistant. It supports NASA heat pumps that utilize the MIM-E03CN / MIM-E03DN & MIM-E03EN control boards (e.g., Samsung Gen 6 heat pump etc). Older non-NASA systems are not supported. 

The project requires a suitable RS485 Modbus enabled board such as the M5Stack Atomic RS485 Base (https://shop.m5stack.com/products/atomic-rs485-base) with the Atom Lite (https://shop.m5stack.com/products/atom-lite-esp32-development-kit). But any ESPHome supported board with a TTL-RS485 converter should theoretically work. Modbus A connects to F1 and Modubs B connects to F2 on the MIM control board. F1 & F2 are the connectors used for communication betweeen the internal unit/MIM board and the external heat pump unit. F3 & F4 are the connectors used by the wired LCD touch controllers. You can take the 12V V+ from V1 and Ground from V2 on the control board. These pins are normally grouped together on the top right hand side of the control board.

| RS485         | MIM Board Pin |
|---------------|---------------|
|   A  (Yellow) |      F1       |
|   B  (Green)  |      F2       |
|   V+ (Red)    |      V1       |
|   G  (Black)  |      V2       |

This project borrows from the excellent work done by the team supporting the ESPHome Samsung HVAC Integration (https://github.com/omerfaruk-aran/esphome_samsung_hvac_bus/). The project includes detailed [hardware installation instructions](https://github.com/omerfaruk-aran/esphome_samsung_hvac_bus/wiki/Hardware-Installation) on the installation process so I won't repeat them here.

Most of the useful controls for DHW (domestic hot water), and heating (single and 2-zone) are supported by this component - along with the ability to read and write FSVs (Field Setting Values). The project has been re-engineered to abstract away the NASA message codes from the C++ code so it should be much easier to add missing controls to the Python lists of ESPHome components (numbers, selects, switches, sensors etc). This should make it much easier to submit PRs for missing NASA messages.

All commands, and FSVs are implemented as standard ESPHome components (e.g., numbers, selects, switches...). Check out the [example.yaml](example.yaml).

**NB**: When assigning a nasa device to a samsung_nasa platform component make sure you assign the correct indoor/outdoor unit. The easiest way to check is by looking at the NASA Label information in the tables below. If the label says VAR_IN_... or ENUM_IN_... then the status is reported from the indoor unit. If the label says VAR_OUT_..., LVAR_OUT_... or ENUM_OUT..., then the status is reported from the outdoor unit.

## Compilation Using Arduino or ESP-IDF

Using the Arduino framework will result in faster compilation time but less efficient RAM usage and larger firmware size.

```yaml
esp32:
  board: m5stack-atom
  framework:
    type: arduino
```

Using the ESP-IDF framework will result in slower compilation time but smaller firmware size and more efficient RAM usage. From ESPHome 2026.1 onwards the default framework will be esp-idf (unless arduino is specified).

```yaml
esp32:
  board: m5stack-atom
  framework:
    type: esp-idf
```

## Basic Controller, NASA Client & Device Configuration  

```yaml
samsung_nasa:
  debug_log_messages: false
  debug_log_undefined_messages: false
  nasa_client: {}
  devices:
   - address: 20.00.00
     id: nasa_device_1
   - address: 10.00.00
     id: nasa_device_2
```

20.00.00 would normally be the address of the indoor unit; 10.00.00 would be the address of the outdoor unit (heat pump). It's best to leave the nasa_client options empty (at their defaults) as the client has been tested with these default values. You will need to provide an id for each device so you can associate each device with an ESPHome component.

## Advanced Controller, NASA Client & Device Configuration  

```yaml
samsung_nasa:
  debug_log_messages: false
  debug_log_undefined_messages: false
  nasa_client:
    silence_interval: 100
    retry_interval: 500
    min_retries: 1
    send_timeout: 1000
    flow_control_pin: GPIOXX
  devices:
   - address: 20.00.00
     id: nasa_device_1
   - address: 10.00.00
     id: nasa_device_2
```

The nasa_client configuration options are to do with ensuring NASA message delivery via a retry mechansim. Thanks and acknowledgment go to atanasenko for the [retry mechanism.](https://github.com/omerfaruk-aran/esphome_samsung_hvac_bus/commit/1030af3bcc4f3dc688be643e0c2ae65b6401fcc5)

 - **silence_interval**: (Optional) The time to wait since the last wire activity before sending. 
 - **retry_interval**: (Optional) The minimum time before a retry attempt.  
 - **min_retries**: (Optional) The minimum number of retries, even beyond timeout. 
 - **send_timeout**: (Optional) The maximum time to wait before discarding commands.  
 - **flow_control_pin**: (Optional) The pin used to switch flow control. This is useful for RS485 transceivers that do not have automatic flow control switching, like the common MAX485.

## Number  

Commands and FSVs are implemented as number components when they represent a range of values such as temperature, duration etc. For commands use the message option with the NASA hex code; for FSVs use the fsv field:

```yaml
number:
  - platform: samsung_nasa
    message: 0x4201
    name: "Zone 1 Target Temp"
    nasa_device_id: nasa_device_1
    id: zone_target_temp

  - platform: samsung_nasa
    fsv: 2011
    nasa_device_id: nasa_device_1
    name: "Water Law (Outdoor Temp) High"
    id: fsv_2011
```

These are the only fields you need to provide. All other fields such as unit of measure, decimal accuracy etc are automatically configured based on the message or fsv value. Number components are read/write so in the examples above the target temperature can be read and modified; likewise the FSV (Water Law (Outdoor Temp) High) can be modified and the new value sent to the heat pump. Caution needs to be exercised with FSVs. While care has been taken to limit the values to those that are appropriate for the given FSV, there can be minor differences between control boards and permitted min/max values.

### Supported Commands  

| NASA Code | NASA Label                              | Description                            |
|-----------|-----------------------------------------|--------------------------------------- |
| 0x4201    | VAR_IN_TEMP_TARGET_F                    | Zone 1 Target Temperature              |
| 0x4206    | VAR_IN_TEMP_TARGET_ZONE2_F              | Zone 2 Target Temperature              |
| 0x4235    | VAR_IN_TEMP_WATER_HEATER_TARGET_F       | DHW Target Temperature                 |
| 0x4247    | VAR_IN_TEMP_WATER_OUTLET_TARGET_F       | Zone 1 Water Outlet Target Temperature |
| 0x4248    | VAR_IN_TEMP_WATER_LAW_TARGET_F          | Water Law Target Temperature           |
| 0x42D7    | VAR_IN_TEMP_WATER_OUTLET_TARGET_ZONE2_F | Zone 2 Water Outlet Target Temperature |

### Supported FSVs  

Refer to p.24 onwards of the [MIM-E03EN user manual PDF](MIM-E03EN.pdf).

1011, 1012, 1021, 1022, 1031, 1032, 1041, 1042, 1051, 1052, 2011, 2012, 2021, 2022, 2031, 
2032, 2051, 2052, 2061, 2062, 2071, 2072, 3021, 3022, 3023, 3024, 3025, 3026, 3032, 3033,
3043, 3044, 3045, 3052, 3046, 3081, 3082, 3083, 4012, 4013, 4024, 4025, 4033, 4042, 4043, 
4044, 4045, 4046, 4052, 4053, 5011, 5013, 5014, 5015, 5016, 5017, 5018, 5019, 5021, 5023,
5082, 5083, 5092, 5093


You can find a list of supported commands and FSVs in the [python configuration file for number components.](/components/samsung_nasa/nasa/numbers.py)

For example here are the python entries for the above number components:

```python
numbers = {
    0x4201: {
        NASA_LABEL: "VAR_IN_TEMP_TARGET_F",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: cmd_numeric_data(16, 30),
        CONF_DEFAULTS: temperature_defaults()
    },
    0x4254: {
        NASA_LABEL: "VAR_IN_FSV_2011",
        NASA_MODE: CONTROLLER_MODE_FSV,
        CONF_DATA: fsv_numeric_data(2011, -20, 5),
        CONF_DEFAULTS: temperature_defaults()
    }
}

```

## Select  

```yaml
select:
  - platform: samsung_nasa
    message: 0x4066
    nasa_device_id: nasa_device_1
    name: Hot Water Mode
    id: hotwater_mode
```

The correct options for select components are automatically configured. You can find a list of supported select components and FSVs in the [python configuration file](/components/samsung_nasa/nasa/selects.py) that is used to auto generate the select component.

So for example message 0x4066 (hot water mode):

```python
0x4066: {
    NASA_LABEL: "ENUM_IN_WATER_HEATER_MODE",
    NASA_MODE: CONTROLLER_MODE_CONTROL,
    CONF_DATA: cmd_select_data(
        [
            "Economy", 
            "Standard", 
            "Power", 
            "Force"
        ]
    ),
    CONF_DEFAULTS: select_defaults()
}
```

### Supported Commands  

| NASA Code | NASA Label                  | Description                                     |
|-----------|-----------------------------|-------------------------------------------------|
| 0x4001    | ENUM_IN_OPERATION_MODE      | Operation mode (eg. Auto, Heat, Cool)           |
| 0x4066    | ENUM_IN_WATER_HEATER_MODE   | DHW mode (eco, standard, power, force)          |
| 0x406F    | ENUM_IN_REFERENCE_EHS_TEMP  | Temperature Reference (Room, Water Out)         |
| 0x8003    | ENUM_OUT_OPERATION_HEATCOOL | Cool/heat mode (Cool, Heat, CoolMain, HeatMain) |

### Supported FSVs  

Refer to p.24 onwards of the [MIM-E03EN user manual PDF](MIM-E03EN.pdf).

2041, 2081, 2091, 2092, 2093, 3011, 3042, 3061, 3071, 4011, 4021, 4022, 4041, 4051, 4052, 4053



## Switch  

Binary type NASA commands and FSV values (such as ON/OFF, YES/NO, ENABLED/DISABLED) are represented as switches. Like Number and Select componentes, they are read/write.

```yaml
switch:
  - platform: samsung_nasa
    message: 0x4065
    nasa_device_id: nasa_device_1
    name: "DHW Power"
    id: dhw_power_switch
  - platform: samsung_nasa
    message: 0x4000
    nasa_device_id: nasa_device_1
    name: "Zone 1 Power"
    id: zone_power
```
 
 A list of available switches can be found in [switches.py](/components/samsung_nasa/nasa/switches.py) which is used to auto configure the switch components.

```python
switches = {
    0x4065: {
        NASA_LABEL: "ENUM_IN_WATER_HEATER_POWER",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },    
    0x4000: {
        NASA_LABEL: "ENUM_IN_OPERATION_POWER",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        CONF_DATA: empty_data(),
        CONF_DEFAULTS: bool_defaults()
    },
}
```

### Supported Commands  

| NASA Code | NASA Label                           | Description                            |
|-----------|--------------------------------------|----------------------------------------|
| 0x4000    | ENUM_IN_OPERATION_POWER              | Zone 1 heating On/Off control          |
| 0x4046    | ENUM_IN_SILENCE                      | Silence mode  On/Off control           |
| 0x4065    | ENUM_IN_WATER_HEATER_POWER           | DHW On/Off control                     |
| 0x406D    | ENUM_IN_OUTING_MODE                  | Outing On/Off control                  |
| 0x411E    | ENUM_IN_OPERATION_POWER_ZONE2.       | Zone 2 heating On/Off control          |
| 0x4111    | ENUM_IN_OPERATION_AUTOMATIC_CLEANING | Turn on/off automatic cleaning         |

### Supported FSVs  

Refer to p.24 onwards of the [MIM-E03EN user manual PDF](MIM-E03EN.pdf).

3031, 3041, 3051, 4023, 4031, 4032, 4061, 5022, 5041, 5051, 5081, 5091, 5094  


## Sensor   

Sensor components are read-only. They report real-time data such as room temperature, energy consumption/production and valve/pump status.

```yaml
sensor:
  - platform: samsung_nasa
    message: 0x4237
    nasa_device_id: nasa_device_1
    name: "DHW Temperature"
    id: hot_water_current_temp
```

In addition to a large selection of available sensors, it is also possible to specify your own NASA code should it not be listed in [sensors.py](/components/samsung_nasa/nasa/sensors.py). You will need to provide the appropriate unit of measure, device class, decimal accuracy and filters to transform the raw NASA value to something meaningful. Consult the [ESPHome documentation](https://esphome.io/components/sensor/) for how to configure a sensor component. As part of the samsung_nasa platform you will need to specify message, nasa_device_id, and platform fields. If you do find a NASA code that is not available as a pre-configured component please pop it in the discussion area along with your yaml configuration for the component so that I can add it for other users.

Here's an example of a user configured sensor:

```yaml
sensor:
   - platform: samsung_nasa
     message: 0x8238
     nasa_device_id: nasa_device_2
     device_class: frequency
     state_class: measurement
     unit_of_measurement: Hz
     accuracy_decimals: 1
     name: Compressor Frequency
     id: compressor_frequency
```

Here is the python entry that configures the above DHW Temperature sensor:

```python
0x4237: {
    NASA_LABEL: "VAR_IN_TEMP_WATER_TANK_F",
    NASA_MODE: CONTROLLER_MODE_STATUS,
    CONF_DEFAULTS: temp_sensor_defaults()
},
```

| NASA Code | NASA Label                                | Description                             |
|-----------|-------------------------------------------|-----------------------------------------|
| 0x24FC    | LVAR_NM_OUT_SENSOR_VOLTAGE                | Heat pump voltage                       |
| 0x4002    | ENUM_IN_OPERATION_MODE_REAL               | Current operation mode                  |
| 0x4038    | ENUM_IN_STATE_HUMIDITY_PERCENT            | Only available with A/C units           |
| 0x4067    | ENUM_IN_3WAY_VALVE                        | DHW valve (0=heat, 1=tank)              |
| 0x4069    | ENUM_IN_THERMOSTAT1                       | Zone 1 input signal from external stat  |
| 0x406A    | ENUM_IN_THERMOSTAT2                       | Zone 2 input signal from external stat  |
| 0x4089    | ENUM_IN_STATE_WATER_PUMP                  | Primary water pump status               |
| 0x408A    | ENUM_IN_2WAY_VALVE                        | Zone control valve status               |
| 0x40C4    | ENUM_IN_WATERPUMP_PWM_VALUE               | PWM Water Pump Status (%)               |
| 0x4202    | VAR_IN_DHW_HEAT_UNTIL                     | Heat DHW until this temperature         |
| 0x4204    | VAR_IN_WATER_OUT_TW2                      | Similar to 0x4238 but 2 degrees lower   |
| 0x4205    | VAR_IN_TEMP_EVA_IN_F                      | EVA return temperature                  |
| 0x4206    | VAR_IN_TEMP_EVA_OUT_F                     | EVA flow temperature                    |
| 0x4236    | VAR_IN_TEMP_WATER_IN_F                    | Flow return temperature                 |
| 0x4237    | VAR_IN_TEMP_WATER_TANK_F                  | DHW tank temperature                    |
| 0x4238    | VAR_IN_TEMP_WATER_OUT_F                   | Flow temperature                        |
| 0x4203    | VAR_IN_TEMP_ROOM_F                        | Zone 1 room temperature                 |
| 0x427F    | VAR_IN_TEMP_WATER_LAW_F                   | Water law target flow temperature       |
| 0x42D4    | VAR_IN_TEMP_ZONE2_F                       | Zone 2 room temperature                 |
| 0x42E8    | VAR_IN_FLOW_SENSOR_VOLTAGE                | Flow sensor voltage                     |
| 0x42E9    | VAR_IN_FLOW_SENSOR_CALC                   | Flow rate sensor (l/min)                |
| 0x4284    | NASA_INDOOR_POWER_CONSUMPTION             | Indoor unit power consumption           |
| 0x4423    | LVAR_IN_MINS_SINCE_INST                   | Mins since installation (unit: days)    |
| 0x4424    | LVAR_IN_MINS_ACTIVE_SINCE_INST            | Mins active since inst. (unit: hours)   |
| 0x4426    | LVAR_IN_4426                              | Heat pump produced energy (last minute) |
| 0x4427    | LVAR_IN_4427                              | Heat pump produced energy (total)       |
| 0x8000    | ENUM_OUT_OPERATION_SERVICE_OP             | Outdoor unit service modes              |
| 0x8001    | ENUM_OUT_OPERATION_ODU_MODE               | Outdoor unit driving Modes              |
| 0x8061    | ENUM_OUT_DEICE_STEP_INDOOR                | Defrost operation steps                 |
| 0x8204    | VAR_OUT_SENSOR_AIROUT                     | Outdoor temperature                     |
| 0x8206    | VAR_OUT_SENSOR_HIGHPRESS                  | High pressure (kgf/cm²)                 |
| 0x8208    | VAR_OUT_SENSOR_LOWPRESS                   | Low pressure (kgf/cm²)                  |
| 0x820A    | VAR_OUT_SENSOR_DISCHARGE1                 | Compresor discharge temperature         |
| 0x8217    | VAR_OUT_SENSOR_CT1                        | Outdoor current (Amps)                  |
| 0x8218    | VAR_OUT_SENSOR_CONDOUT                    | Heat exchanger outlet temperature       |
| 0x821A    | VAR_OUT_SENSOR_SUCTION                    | Compresor suction temperature           |
| 0x821C    | VAR_OUT_SENSOR_DOUBLETUBE                 | Double tube temperature                 |
| 0x821E    | VAR_OUT_SENSOR_EVIIN                      | EVI return temperature                  |
| 0x8220    | VAR_OUT_SENSOR_EVIOUT                     | EVI flow temperature                    |
| 0x8235    | VAR_OUT_ERROR_CODE                        | Error code (0 = OK)                     |
| 0x8236    | VAR_OUT_CONTROL_ORDER_CFREQ_COMP1         | Compressor instruction frequency        |
| 0x8237    | VAR_OUT_CONTROL_TARGET_CFREQ_COMP1        | Compressor target frequency             |
| 0x8238    | VAR_OUT_CONTROL_CFREQ_COMP1               | Compressor current frequency            |
| 0x823B    | VAR_OUT_SENSOR_DCLINK_VOLTAGE             | Inverter DC voltage input               |
| 0x823D    | VAR_OUT_LOAD_FANRPM1                      | Outdoor fan speed (rpm)                 |
| 0x8240    | NASA_OUTDOOR_ODU_CAPA1                    | Electric capacity of outdoor unit in %  |
| 0x8254    | VAR_OUT_SENSOR_IPM1                       | IPM1 sensor reading (°C)                |
| 0x827A    | VAR_OUT_CONTROL_DSH1                      | DSH1 sensor reading (°C)                |
| 0x8280    | VAR_OUT_SENSOR_TOP1                       | TOP1 sensor reading (°C)                |
| 0x829F    | VAR_OUT_SENSOR_SAT_TEMP_HIGH_PRESSURE     | High pressure saturation temperature    |
| 0x82A0    | VAR_OUT_SENSOR_SAT_TEMP_LOW_PRESSURE      | Low pressure saturation temperature     |
| 0x82DF    | VAR_OUT_SENSOR_TW1                        | TW1 sensor reading (°C)(same as 0x4238) |
| 0x82E0    | VAR_OUT_SENSOR_TW2                        | TW2 sensor reading (°C)(same as 0x4236) |
| 0x8411    | NASA_OUTDOOR_CONTROL_WATTMETER_1UNIT      | Outdoor unit inst. power consumed (w)   |
| 0x8413    | LVAR_OUT_CONTROL_WATTMETER_1W_1MIN_SUM    | Heat pump consumed energy (last minute) |
| 0x8414    | LVAR_OUT_CONTROL_WATTMETER_ALL_UNIT_ACCUM | Heat pump consumed energy (total)       |

Bear in mind that VAR_OUT type NASA Labels mean that you will need to assign the outdoor device to the component as it is the external heat pump unit that reports this data.

## Binary Sensor

Binary sensors are read-only. They report boolean type data such as Yes/No, On/Off, Open/Closed.

| NASA Code | NASA Label                        | Description                            |
|-----------|-----------------------------------|--------------------------------------- |
| 0x4067    | ENUM_IN_3WAY_VALVE                | 3-Way Valve: 0 = Heating; 1 = Tank     |
| 0x4087    | ENUM_IN_BOOSTER_HEATER            | Booster Heater: 0 = Off; 1 = On        |
| 0x406C    | ENUM_IN_BACKUP_HEATER             | Backup Heater: 0 = Off; 1 = On         |
| 0x8010    | ENUM_OUT_LOAD_COMP1               | Compressor Running: 0 = Off; 1 = On    |
| 0x8017    | ENUM_OUT_LOAD_HOTGAS              | Hot Gas 1 Status: 0 = Off; 1 = On      |
| 0x8019    | ENUM_OUT_LOAD_LIQUID              | Liquid Valve Status: 0 = Off; 1 = On   |
| 0x8021    | ENUM_OUT_LOAD_EVI_BYPASS          | EVI Bypass: 0 = Off; 1 = On            |
| 0x801A    | ENUM_OUT_LOAD_4WAY                | 4-Way Valve Status: 0 = Off; 1 = On    |
| 0x80AF    | ENUM_OUT_LOAD_BASEHEATER          | Base Heater Status: 0 = Off; 1 = On    |
| 0x80D7    | ENUM_OUT_LOAD_PHEHEATER           | PHE Heater Status: 0 = Off; 1 = On     |

```yaml
binary_sensor:
  - platform: samsung_nasa
    message: 0x4087
    nasa_device_id: nasa_device_1
    name: Booster Heater
    id: booster_heater
  - platform: samsung_nasa
    message: 0x8010
    nasa_device_id: nasa_device_2
    name: Compressor Status
    id: compressor_status 
```

Bear in mind that ENUM_OUT type NASA Labels mean that you will need to assign the outdoor device to the component. It is the outdoor (heat pump) unit that reports this data. Like sensors, binary sensors can also be user configured for NASA codes not listed above. See the Sensors section above on how to do this.

## Automation and FSVs

Unlike NASA sensors which regularly report data without being requested, FSV values need to be requested. The samsung_nasa.request_read action enables you to request FSV values using ESPHome's powerful automation triggers and conditions. For example you can periodically request readings using ESPHome's interval component:

```yaml
interval:
  - interval: 30min
    startup_delay: 30s
    then:
      - samsung_nasa.request_read:
          id: [fsv_2011, fsv_2012, fsv_2021, fsv_2022]
```

In the above automation FSV values are read 30 seconds after startup and then every 30 minutes (or for example once a day).

Alternatively you can implement a configuration button component that when pressed will perform a read request:

```yaml
button:
  - platform: template
    name: Request
    entity_category: config
    on_press:
      - samsung_nasa.request_read:
          id: [fsv_2011, fsv_2012, fsv_2021, fsv_2022]
```

## Climate Component

The samsung_nasa platform extends to the climate component which can report current DHW (domestic hot water) temperature and room temperature if you use the Samsung wired controller as a thermostat. For DHW and heating you can control the target temperature and even bind select components to auto generate presets.

```yaml
climate:
  - platform: samsung_nasa
    name: Hot Water
    id: climate_hot_water
    power_switch_id: dhw_power_switch
    current_temp_sensor_id: hot_water_current_temp
    target_temp_number_id: hot_water_target_temp
    custom_preset_select_id: hotwater_mode
    action_mode_sensor:
      id: three_way_valve
      mappings:
        0: CLIMATE_ACTION_IDLE
        1: CLIMATE_ACTION_HEATING
    visual:
      min_temperature: 30
      max_temperature: 60
      temperature_step:
        target_temperature: 0.5
        current_temperature: 0.1
```

In the above example the climate control can report/control heat/off mode by binding the power_switch_id field to the appropriate switch component:

```yaml
switch:
  - platform: samsung_nasa
    message: 0x4065
    nasa_device_id: nasa_device_1
    name: "DHW Power"
    id: dhw_power_switch
```

The climate component reports hot water temperature by binding the current_temp_sensor_id to the appropriate sensor component:

```yaml
sensor:
  - platform: samsung_nasa
    message: 0x4237
    nasa_device_id: nasa_device_1
    name: "DHW Temperature"
    internal: true
    id: hot_water_current_temp
```

Likewise, target temperature can be bound to a number component for reading/modifying the desired temperature:

```yaml
number:
  - platform: samsung_nasa
    message: 0x4235
    name: DHW Target Temperature
    nasa_device_id: nasa_device_1
    id: hot_water_target_temp
```
If you are feeling adventurous you can even have the climate component report current action of the heat pump (idle, heating, off etc) by binding the action_mode_sensor field to the appropriate pump or valve. In the above example NASA code 0x4067 is the code for reporting the DHW valve status (0 = room; 1 = hot water tank). When this sensor reports a value of 1 the heat pump is actively heating the hot water tank.

```yaml
sensor:
    # 0x4067
    # 0 = room; 1 = tank
  - platform: samsung_nasa
    message: 0x4067
    nasa_device_id: nasa_device_1
    name: "3-Way Valve"
    id: three_way_valve 

climate:
  - platform: samsung_nasa
    name: Hot Water
    id: climate_hot_water
    power_switch_id: dhw_power_switch
    current_temp_sensor_id: hot_water_current_temp
    target_temp_number_id: hot_water_target_temp
    custom_preset_select_id: hotwater_mode
    action_mode_sensor:
      id: three_way_valve
      mappings:
        0: CLIMATE_ACTION_IDLE
        1: CLIMATE_ACTION_HEATING
```

Use the mappings field to map sensor values to climate action modes. Available climate action modes are:

* CLIMATE_ACTION_OFF  
* CLIMATE_ACTION_COOLING  
* CLIMATE_ACTION_HEATING  
* CLIMATE_ACTION_IDLE  

Finally you populate the climate component's presets from a select component. In this example the NASA code 0x4066, which is implemented as a select component, is bound to the climate's custom_preset_select_id field.

```yaml
select:
  - platform: samsung_nasa
    message: 0x4066
    nasa_device_id: nasa_device_1
    name: Hot Water Mode
    id: hotwater_mode
```
## What if My System Uses 3rd Party Thermostats?

Whilst you won't be able to use the samsung_nasa platform climate control you can still turn the heating zone on/off and report whether or not 3rd party thermostats are calling for heat. Note that when your heat pump is configured to use 3rd party thermostats to control heating zone valves (rather than the Samsung wired controller acting as thermostat with zone control enabled) the MIM control board will not use pins B9/B10, B13/B14 (switched live output for zone valve control). Instead try something like this:

```yaml
switch:
  # Turn Heating Zone On/Off
  - platform: samsung_nasa
    message: 0x4000
    nasa_device_id: nasa_device_1
    name: "Zone Power"
binary_sensor:
  - platform: template
    name: "Zone Running"
    id: heating_running
text_sensor:
  - platform: template
    name: "Zone Action"
    id: heating_action
sensor:
    # 0x4069: ENUM_IN_THERMOSTAT1
    # On MIM control board 3rd party thermostats 
    # are connected to Pin B22 which is a command 
    # signal input (Command Signal Zone 1 Heating)
    # 0 = Off, 1 = Cool, 2 = Heat
    # If Off then Action = Idle
    # If Heat then Action = Heating
  - platform: samsung_nasa
    id: zone_heating
    message: 0x4069
    nasa_device_id: nasa_device_1
    state_class: measurement
    on_value:
        then:
            - if:
                condition:
                    lambda: "return x == 0;"
                then:
                    - binary_sensor.template.publish:
                        id: heating_running
                        state: OFF
                    - text_sensor.template.publish:
                        id: heating_action
                        state: "Idle"
                else:
                    - binary_sensor.template.publish:
                        id: heating_running
                        state: ON
                    - text_sensor.template.publish:
                        id: heating_action
                        state: "Heating"
```

## COP (Coefficient of Performance)

The COP of a heat pump is a measure of its efficiency, specifically how much heat it can produce for a given amount of electricial energy input. A higher COP indicates a more efficient heat pump. For example, if a heat pump has a COP of 3, it means that for every 1 unit of electrical energy it consumes, it delivers 3 units of heat.

Using sensors 0x8414 (total consumed energy) and 0x4427 (total produced energy) it is possible to do a crude calculation of the overall COP of your heat pump:

```yaml
# Assuming the 0x8414 sensor has an id of heat_pump_cumulative_energy
# Assuming the 0x4427 sensor has an id of heat_pump_produced_energy
sensor:
  - platform: template
    name: COP - Total
    icon: mdi:chart-bar
    lambda: |-
      return id(heat_pump_produced_energy).state /
             id(heat_pump_cumulative_energy).state;
    update_interval: 300s
    accuracy_decimals: 2
```

To calculate the COP minute by minute (bear in mind this will only be meaningful when the heat pump is running):

```yaml
# Assuming the 0x4426 sensor has an id of heat_generated_last_min
# Assuming the 0x8413 sensor has an id of heat_consumed_last_min
sensor:
  - platform: template
    name: COP - Instant
    icon: mdi:chart-bar
    state_class: measurement
    lambda: |-
      float x = (id(heat_generated_last_min).state /
           id(heat_consumed_last_min).state);
      if (x > 8) { x = 8; }
      if (x < 0) { x = 0; }
      return x;
    update_interval: 10s
    accuracy_decimals: 2
```

Calculating daily COP takes a little more work. First, create two sensors using ESPHome's total_daily_energy platform. For the power_id fields use the heat_consumed_last_min (sensor 0x8413) and head_generated_last_min (sensor 0x4426) sensors from the example above.

```yaml
sensor:
  - platform: total_daily_energy
    id: daily_energy_consumed
    name: Daily Energy Consumed
    power_id: heat_consumed_last_min
    unit_of_measurement: 'kWh'
    state_class: total_increasing
    device_class: energy
    accuracy_decimals: 3
    filters:
      # Multiplication factor from W to kW is 0.001
      - multiply: 0.001
  - platform: total_daily_energy
    id: daily_heat_generated
    name: Daily Heat Generated
    power_id: heat_generated_last_min
    unit_of_measurement: 'kWh'
    state_class: total_increasing
    device_class: energy
    accuracy_decimals: 3
    filters:
      # Multiplication factor from W to kW is 0.001
      - multiply: 0.001
```
Finally, use these two total_daily_energy sensors in a template sensor:

```yaml
  - platform: template
    name: COP - Daily
    icon: mdi:chart-bar
    state_class: measurement
    lambda: |-
      float x = (id(daily_heat_generated).state /
           id(daily_energy_consumed).state);
      if (x > 8) { x = 8; }
      if (x < 0) { x = 0; }
      return x;
```
To have the daily COP sensor reset each day you will need a time component (sntp, home assistant etc). Dont' forget to set your [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) (Region/City). 

```yaml
# Enable time component to reset energy at midnight
time:
  - platform: homeassistant
    id: homeassistant_time
    timezone: "Europe/London"
```

Thanks to [@mergwyn](https://github.com/mergwyn) for providing these examples.

## Home Assistant

An example heat pump dashboard in Home Assistant using this component and the example.yaml.

<img src="samsung_nasa.png" width="100%"/>

## Implementation Details

On startup the NASA Controller issues a read request for all configured samsung_nasa platform components. These are batched into groups of up to 10 messages and dispatched with a small time delay between each read request. The heat pump responds with a value for each NASA message so all samsung_nasa components should have an initial up-to-date value (including FSVs).

When a command is issued and successfully actioned by the heat pump, the heat pump responds with an ACK message. A read request is then issued to confirm the new value and this is reported back to the samsung_nasa platform components. Components therefore do not require optimistic: true to be set as feedback from the NASA Controller component updates the state of the component soon after the command has been issued.

A batched dispatcher is used for outgoing read requests - this automatically combines up to 10 read requests into a single payload and these batches are issued with a small delay betweeen each dispatch as a means of congestion control. There is also an outgoing queue which writes to the bus when the bus is "quiet" i.e. not currently receiving data. These two approaches combined together should hopefully minimise traffic and help reduce collisions.

## NASA Protocol & List of Codes

The protocol and list of codes are available [here](samsung_nasa_protocol.md) courtesy of [@larrykluger](https://github.com/larrykluger).

## Acknowledgments

@Ianwin for founding the samsung HVAC Bus project; 
@omerfaruk-aran for maintaining the samsung HVAC project; @north3221, @matthias882, @hnykda, @Foxhill67 for technical contributions to understanding the NASA protocol. Thanks goes to @atanasenko for the much improved retry-mechanism.
