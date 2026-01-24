from esphome.const import (
    CONF_DEFAULTS,
    CONF_ICON,
    CONF_ENTITY_CATEGORY,
    CONF_NAME,
    ENTITY_CATEGORY_DIAGNOSTIC,
    ENTITY_CATEGORY_NONE,
)
from .const import *

# Simple helper for Text Sensor defaults
def text_defaults(
        icon="mdi:text", 
        category=ENTITY_CATEGORY_NONE
    ):
    return {
        CONF_ICON: icon,
        CONF_ENTITY_CATEGORY: category,
    }

text_sensors = {
    0x4002: {
        NASA_LABEL: "ENUM_IN_OPERATION_MODE_REAL",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_NAME: "Current Operation Mode",
        NASA_MAPPING: {
            0: "Auto", 
            1: "Cool", 
            2: "Dry", 
            3: "Fan", 
            4: "Heat",
            11: "Auto-Cool", 
            12: "Auto-Dry", 
            13: "Auto-Fan", 
            14: "Auto-Heat",
            21: "Cool Storage", 
            24: "Hot Water", 
            255: "Unknown/Idle"
        },
        CONF_DEFAULTS: text_defaults("mdi:sync")
    },
    0x4067: {
        NASA_LABEL: "ENUM_IN_3WAY_VALVE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_NAME: "3-Way Valve Position",
        NASA_MAPPING: {
            0: "Room (Heating)",
            1: "Tank (DHW)"
        },
        CONF_DEFAULTS: text_defaults("mdi:valve")
    },
    0x4066: {
        NASA_LABEL: "ENUM_IN_WATER_HEATER_MODE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_NAME: "DHW Mode",
        NASA_MAPPING: {
            0: "Economic", 
            1: "Standard", 
            2: "Power", 
            3: "Force"
        },
        CONF_DEFAULTS: text_defaults("mdi:water-boiler")
    },
    0x8000: {
        NASA_LABEL: "ENUM_OUT_OPERATION_SERVICE_OP",
        NASA_MODE: CONTROLLER_MODE_CONTROL,
        NASA_MAPPING: {
            2: "Heating Test Run",
            3: "Pump Out",
            13: "Cooling Test Run",
            14: "Pump Down"
        },
        CONF_DEFAULTS: text_defaults("mdi:engine")
    },
    0x8001: {
        NASA_LABEL: "ENUM_OUT_OPERATION_ODU_MODE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_NAME: "Outdoor Driving Mode",
        NASA_MAPPING: {
            0: "Stop", 
            1: "Safety", 
            2: "Normal", 
            3: "Balance", 
            4: "Recovery",
            5: "Deice", 
            6: "Comp Down", 
            7: "Prohibit", 
            8: "Line Jig", 
            9: "PCB Jig",
            10: "Test Mode", 
            11: "Recharge", 
            12: "Pump Down", 
            13: "Pump Out",
            14: "Vacuum", 
            15: "Calory Jig", 
            16: "Pump Down Stop", 
            17: "Sub Stop",
            18: "Check Pipe", 
            19: "Check Ref", 
            20: "FPT Jig", 
            21: "Nonstop Heat/Cool Change", 
            22: "Auto Inspect", 
            23: "Electric Discharge",
            24: "Split Deice", 
            25: "Inverter Check", 
            26: "Nonstop Deice",
            27: "Remote Test", 
            28: "Rating", 
            29: "PC Test", 
            30: "Pump Down Thermo-off",
            31: "3-Phase Test", 
            32: "Smart Install", 
            33: "Deice Perf Test",
            34: "Inverter Fan PBA Check", 
            35: "Auto Pipe Pairing", 
            36: "Auto Charge"
        },
        CONF_DEFAULTS: text_defaults("mdi:engine")
    },
    0x8061: {
        NASA_LABEL: "ENUM_OUT_DEICE_STEP_INDOOR",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_NAME: "Defrost Stage",
        NASA_MAPPING: {
            1: "Stage 1", 
            2: "Stage 2", 
            3: "Stage 3", 
            7: "Finished", 
            255: "No Defrost"
        },
        CONF_DEFAULTS: text_defaults("mdi:ice-pop")
    },
    0x8235: {
        NASA_LABEL: "VAR_OUT_ERROR_CODE",
        NASA_MODE: CONTROLLER_MODE_STATUS,
        CONF_NAME: "System Error Status",
        NASA_MAPPING: {
            0: "No Error",
            # --- Communication & System ---
            101: "Wire Connection Error (Control Kit/ODU)",
            162: "Control Kit EEPROM Error",
            163: "EEPROM Option Setting Error",
            201: "Communication Matching Error",
            202: "Communication Error (ODU Time-out 3m)",
            203: "Comm Error: Inverter to Main Micom",
            205: "Comm Error: Inv Micom to Fan Micom",
            601: "Comm Error: Control Kit to Remote",
            602: "Remote Controller Main/Sub Setting Error",
            604: "Tracking Error: Control Kit to Remote",
            607: "Comm Error: Main to Sub Remote",
            670: "Controller Combination Error",

            # --- Indoor / Control Kit Sensors ---
            120: "Zone 2 Room Sensor Error (Open/Short)",
            121: "Zone 1 Room Sensor Error (Open/Short)",
            122: "Indoor EVA-IN Sensor Error",
            123: "Indoor EVA-OUT Sensor Error",
            177: "Emergency Signal Error (Hydro Box)",
            198: "Terminal Block Thermal Fuse Open",
            897: "DHW Tank Inlet Sensor Error",
            899: "Zone 1 Water-Out Sensor Error",
            900: "Zone 2 Water-Out Sensor Error",
            901: "Inlet Water (PHE) Sensor Error",
            902: "Outlet Water (PHE) Sensor Error",
            903: "Backup Heater Outlet Sensor Error",
            904: "DHW Tank Sensor Error",
            910: "Water Outlet Pipe Sensor Detached",
            916: "Mixing Valve Sensor Error",
            973: "Water Pressure Sensor Error",

            # --- Outdoor Unit Sensors & Operation ---
            221: "ODU Ambient Temp Sensor Error",
            231: "Condenser Temp Sensor Error",
            241: "ODU Cond-Out Sensor Breakaway",
            251: "Discharge Temp Sensor Error",
            262: "Discharge Sensor Breakaway",
            266: "Compressor Top Sensor Breakaway",
            269: "Suction Sensor Breakaway",
            276: "Comp Top Temp Sensor Error",
            291: "High Pressure Sensor Error",
            296: "Low Pressure Sensor Error",
            308: "Suction Sensor Error",
            320: "OLP Sensor Error",
            321: "EVI Inlet Sensor Error",
            322: "EVI Outlet Sensor Error",
            381: "Inverter 1 PCB Overheat",
            403: "PHE Freeze Detection (Cooling)",
            436: "PHE Freeze Detection (Heating)",
            906: "ODU Evap-In Sensor Error",

            # --- Protection & Mechanical ---
            404: "Outdoor Unit Overload Protection",
            407: "High Pressure Protection (Comp Down)",
            410: "Low Pressure Protection (Comp Down)",
            416: "Compressor Discharge Overheat",
            425: "Power Line Missing (3-Phase Model)",
            428: "Compression Ratio Control Error",
            438: "EVI EEV Opening Error",
            439: "Refrigerant Leakage (Standby)",
            440: "Heating Blocked (Outdoor >35°C)",
            441: "Cooling Blocked (Outdoor <9°C)",
            443: "No Startup: Low Pressure",
            450: "High Condenser Temp Error",
            458: "ODU Fan 1 Error",
            475: "ODU Fan 2 Error",
            500: "IPM Overheat Error",
            507: "High Pressure Switch Trip",
            536: "PHE Refrigerant Leak Error",
            554: "Gas Leak Error",
            907: "Pipe Rupture Protection Error",
            908: "Freeze Prevention (Auto-Restart)",
            909: "Freeze Prevention (Manual Reset)",
            911: "Low Water Flow Rate Error",
            913: "Flow Switch Error (6x Detection)",
            914: "Incorrect Thermostat Connection",
            915: "DC Fan Error (Non-operating)",
            919: "DHW Disinfection Temp Not Reached",
            920: "FSV SD Card Read Error",

            # --- Inverter & Power ---
            461: "Inverter: Comp Startup Error",
            462: "Inverter: Total/PFC Overcurrent",
            463: "OLP Overheated",
            464: "Inverter: IPM Overcurrent",
            465: "Compressor V Limit Error",
            466: "DC-Link Under/Over Voltage",
            467: "Inverter: Comp Rotation Error",
            468: "Inverter: Current Sensor Error",
            469: "Inverter: DC-Link Voltage Sensor Error",
            470: "ODU EEPROM Read/Write Error",
            471: "ODU EEPROM OTP Error",
            474: "IPM or PFCM Temp Sensor Error",
            483: "H/W DC-Link Over Voltage",
            484: "PFC Overload Error",
            485: "Input Current Sensor Error",
            488: "AC Input Voltage Sensor Error",
            590: "Inverter: Data Flash Error",
        },
        CONF_DEFAULTS: text_defaults("mdi:alert-octagon", ENTITY_CATEGORY_DIAGNOSTIC)
    }
}
