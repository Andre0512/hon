WASHING_PR_PHASE = {
    "ready": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "spin": "WASHING_CMD&CTRL.PHASE_SPIN.TITLE",
    "rinse": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "drying": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    "steam": "WASHING_CMD&CTRL.PHASE_STEAM.TITLE",
    "weighting": "WASHING_CMD&CTRL.PHASE_WEIGHTING.TITLE",
    "scheduled": "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",
    "tumbling": "WASHING_CMD&CTRL.PHASE_TUMBLING.TITLE",
    "refresh": "WASHING_CMD&CTRL.PHASE_REFRESH.TITLE",
    "heating": "WASHING_CMD&CTRL.PHASE_HEATING.TITLE",
    "washing": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
}

MACH_MODE = {
    "ready": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "running": "WASHING_CMD&CTRL.PHASE_RUNNING.TITLE",
    "pause": "WASHING_CMD&CTRL.PHASE_PAUSE.TITLE",
    "scheduled": "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",
    "error": "WASHING_CMD&CTRL.PHASE_ERROR.TITLE",
    "test": "Test",
    "ending": "GLOBALS.APPLIANCE_STATUS.ENDING_PROGRAM",
}

TUMBLE_DRYER_PR_PHASE = {
    "ready": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "heat_stroke": "TD_CMD&CTRL.STATUS_PHASE.PHASE_HEAT_STROKE",
    "drying": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    "cooldown": "TD_CMD&CTRL.STATUS_PHASE.PHASE_COOLDOWN",
    "unknown": "unknown",
    "tumbling": "WASHING_CMD&CTRL.PHASE_TUMBLING.DASHBOARD_TITLE",
}

DIRTY_LEVEL = {
    "little": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.LITTLE",
    "normal": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.NORMAL",
    "very": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.VERY",
    "unknown": "unknown",
}

STEAM_LEVEL = {
    "no_steam": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.NO_STEAM",
    "cotton": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_FABRICS.COTTON_TITLE",
    "delicate": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_FABRICS.DELICATE_TITLE",
    "synthetic": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_FABRICS.SYNTHETIC_TITLE",
}

DISHWASHER_PR_PHASE = {
    "ready": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "prewash": "WASHING_CMD&CTRL.PHASE_PREWASH.TITLE",
    "washing": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "rinse": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "drying": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    "hot_rinse": "WASHING_CMD&CTRL.PHASE_HOT_RINSE.TITLE",
}

TUMBLE_DRYER_DRY_LEVEL = {
    "no_dry": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.NO_DRY",
    "iron_dry": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.IRON_DRY",
    "no_dry_iron": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.NO_DRY_IRON_TITLE",
    "cupboard_dry": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.CUPBOARD_DRY_TITLE",
    "extra_dry": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.EXTRA_DRY_TITLE",
    "ready_to_wear": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.READY_TO_WEAR_TITLE",
}

AC_MACH_MODE = {
    "auto": "PROGRAMS.AC.IOT_AUTO",
    "cool": "PROGRAMS.AC.IOT_COOL",
    "dry": "PROGRAMS.AC.IOT_DRY",
    "heat": "PROGRAMS.AC.IOT_HEAT",
    "fan": "PROGRAMS.AC.IOT_FAN",
}

AC_FAN_MODE = {
    "high": "AC.PROGRAM_CARD.WIND_SPEED_HIGH",
    "mid": "AC.PROGRAM_CARD.WIND_SPEED_MID",
    "low": "AC.PROGRAM_CARD.WIND_SPEED_LOW",
    "auto": "AC.PROGRAM_CARD.WIND_SPEED_AUTO",
}

AC_HUMAN_SENSE = {
    "touch_off": "AC.PROGRAM_DETAIL.TOUCH_OFF",
    "avoid_touch": "AC.PROGRAM_DETAIL.AVOID_TOUCH",
    "follow_touch": "AC.PROGRAM_DETAIL.FOLLOW_TOUCH",
    "unknown": "unknown",
}

REF_ZONES = {
    "fridge": "REF.ZONES.FRIDGE",
    "freezer": "REF.ZONES.FREEZER",
    "vtroom1": "REF.ZONES.MY_ZONE_1",
    "fridge_freezer": ["REF.ZONES.FRIDGE", " & ", "REF.ZONES.FREEZER"],
}


SENSOR = {
    "washing_modes": MACH_MODE,
    "mach_modes_ac": AC_MACH_MODE,
    "program_phases_wm": WASHING_PR_PHASE,
    "program_phases_td": TUMBLE_DRYER_PR_PHASE,
    "program_phases_dw": DISHWASHER_PR_PHASE,
    "dry_levels": TUMBLE_DRYER_DRY_LEVEL,
}

SELECT = {
    "dry_levels": TUMBLE_DRYER_DRY_LEVEL,
    "eco_pilot": AC_HUMAN_SENSE,
    "fan_mode": AC_FAN_MODE,
    "ref_zones": REF_ZONES,
}

PROGRAMS = {
    "select": {
        "programs_ac": "PROGRAMS.AC",
        "programs_dw": "PROGRAMS.DW",
        "programs_ih": "PROGRAMS.IH",
        "programs_ov": "PROGRAMS.OV",
        "programs_td": "PROGRAMS.TD",
        "programs_wm": "PROGRAMS.WM_WD",
        "programs_ref": "PROGRAMS.REF",
    },
    "sensor": {
        "programs_ac": "PROGRAMS.AC",
        "programs_dw": "PROGRAMS.DW",
        "programs_ih": "PROGRAMS.IH",
        "programs_ov": "PROGRAMS.OV",
        "programs_td": "PROGRAMS.TD",
        "programs_wm": "PROGRAMS.WM_WD",
        "programs_ref": "PROGRAMS.REF",
        "programs_wc": "PROGRAMS.WC",
    },
}

CLIMATE = {
    "fridge": {
        "preset_mode": {
            "name": "REF_CMD&CTRL.MODE_SELECTION_DRAWER_FRIDGE.FRIDGE_MODE_TITLE",
            "state": {
                "auto_set": "REF_CMD&CTRL.MODALITIES.ECO",
                "super_cool": "REF_CMD&CTRL.MODALITIES.SUPER_COOL",
                "holiday": "REF_CMD&CTRL.MODALITIES.BACK_FROM_HOLIDAY",
                "no_mode": "REF_CMD&CTRL.MODALITIES.NO_MODE_SELECTED",
            },
        }
    },
    "freezer": {
        "preset_mode": {
            "name": "REF_CMD&CTRL.MODE_SELECTION_DRAWER_FREEZER.FREEZER_MODE_TITLE",
            "state": {
                "auto_set": "REF_CMD&CTRL.MODALITIES.ECO",
                "super_freeze": "REF_CMD&CTRL.MODALITIES.SHOCK_FREEZE",
                "no_mode": "REF_CMD&CTRL.MODALITIES.NO_MODE_SELECTED",
            },
        }
    },
    "oven": {
        "preset_mode": {
            "name": "OV.TABS.PROGRAMS_TITLE",
            "state": "PROGRAMS.OV",
        }
    },
    "air_conditioner": {
        "preset_mode": {
            "name": "OV.TABS.PROGRAMS_TITLE",
            "state": "PROGRAMS.AC",
        }
    },
    "wine": {
        "preset_mode": {
            "name": "WC.NAME",
            "state": "PROGRAMS.WC",
        }
    },
}

NAMES = {
    "switch": {
        "anti_crease": "HDRY_CMD&CTRL.PROGRAM_CYCLE_DETAIL.ANTICREASE_TITLE",
        "add_dish": "DW.ADD_DISH",
        "eco_express": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.ECO",
        "extra_dry": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRA_DRY",
        "half_load": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.HALF_LOAD",
        "open_door": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.OPEN_DOOR",
        "three_in_one": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.THREE_IN_ONE",
        "preheat": "OV.PROGRAM_DETAIL.PREHEAT",
        "dish_washer": "GLOBALS.APPLIANCES_NAME.DW",
        "tumble_dryer": "GLOBALS.APPLIANCES_NAME.TD",
        "washing_machine": "GLOBALS.APPLIANCES_NAME.WM",
        "washer_dryer": "GLOBALS.APPLIANCES_NAME.WD",
        "oven": "GLOBALS.APPLIANCES_NAME.OV",
        "prewash": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.PREWASH",
        "pause": "GENERAL.PAUSE_PROGRAM",
        "keep_fresh": "GLOBALS.APPLIANCE_STATUS.TUMBLING",
        "delay_time": "HINTS.TIPS_TIME_ENERGY_SAVING.TIPS_USE_AT_NIGHT_TITLE",
        "rapid_mode": "AC.PROGRAM_CARD.RAPID",
        "eco_mode": "AC.PROGRAM_CARD.ECO_MODE",
        "10_degree_heating": "PROGRAMS.AC.IOT_10_HEATING",
        "self_clean": "PROGRAMS.AC.IOT_SELF_CLEAN",
        "self_clean_56": "PROGRAMS.AC.IOT_SELF_CLEAN_56",
        "silent_mode": "AC.PROGRAM_DETAIL.SILENT_MODE",
        "mute_mode": "AC.PROGRAM_DETAIL.MUTE_MODE",
        "extra_rinse_1": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE1",
        "extra_rinse_2": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE2",
        "extra_rinse_3": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE3",
        "acqua_plus": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.ACQUAPLUS",
        "auto_dose_softener": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.AUTODOSE",
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.SOFTENER",
        ],
        "auto_dose_detergent": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.AUTODOSE",
            "WASHING_CMD&CTRL.DASHBOARD_MENU_MORE_SETTINGS_WATER.DETERGENT",
        ],
        "good_night": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.GOODNIGHT",
        "auto_set": "REF_CMD&CTRL.MODALITIES.ECO",
        "super_cool": "REF_CMD&CTRL.MODALITIES.SUPER_COOL",
        "super_freeze": "REF_CMD&CTRL.MODALITIES.SUPER_FREEZE",
        "refrigerator": "REF.NAME",
    },
    "binary_sensor": {
        "door_lock": "WASHING_CMD&CTRL.CHECK_UP_RESULTS.DOOR_LOCK",
        "extra_rinse_1": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE1",
        "extra_rinse_2": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE2",
        "extra_rinse_3": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE3",
        "good_night": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.GOODNIGHT",
        "anti_crease": "HDRY_CMD&CTRL.PROGRAM_CYCLE_DETAIL.ANTICREASE_TITLE",
        "acqua_plus": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.ACQUAPLUS",
        "spin_speed": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.SPINSPEED",
        "still_hot": "IH.COILS_STATUS.STILL_HOT",
        "pan_status": "IH.COILS_STATUS.PAN",
        "remote_control": "OV.SUPPORT.REMOTE_CONTROL",
        "rinse_aid": "DW_CMD&CTRL.MAINTENANCE.CONSUMABLE_LEVELS_ICON_RINSE_AID",
        "salt_level": "DW_CMD&CTRL.MAINTENANCE.CONSUMABLE_LEVELS_ICON_SALT",
        "door_open": "GLOBALS.APPLIANCE_STATUS.DOOR_OPEN",
        "connection": "ENROLLMENT_COMMON.HEADER_NAME.STEP_APPLIANCE_CONNECTION",
        "child_lock": "AP.FOOTER_MENU_MORE.SECURITY_LOCK_TITLE",
        "on": "GLOBALS.GENERAL.ON",
        "prewash": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.PREWASH",
        "buzzer": "DW_CMD&CTRL.SETTINGS.END_CYCLE_BUZZER",
        "holiday_mode": "REF.DASHBOARD_MENU_MORE_NOTIFICATIONS.HOLIDAY_MODE",
        "auto_set": "REF_CMD&CTRL.MODALITIES.ECO",
        "super_cool": "REF_CMD&CTRL.MODALITIES.SUPER_COOL",
        "super_freeze": "REF_CMD&CTRL.MODALITIES.SUPER_FREEZE",
        "freezer_door": ["GLOBALS.APPLIANCE_STATUS.DOOR_OPEN", "REF.ZONES.FREEZER"],
        "fridge_door": ["GLOBALS.APPLIANCE_STATUS.DOOR_OPEN", "REF.ZONES.FRIDGE"],
        "filter_replacement": "AP.MAINTENANCE.FILTER_REPLACEMENT",
    },
    "button": {
        "induction_hob": "GLOBALS.APPLIANCES_NAME.IH",
        "start_program": ["WC.SET_PROGRAM.PROGRAM", "GLOBALS.GENERAL.START_ON"],
        "stop_program": ["WC.SET_PROGRAM.PROGRAM", "GLOBALS.GENERAL.STOP"],
    },
    "select": {
        "dry_levels": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_LEVEL",
        "dry_time": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_TIME",
        "spin_speed": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.SPINSPEED",
        "temperature": "IH.COMMON.TEMPERATURE",
        "programs_dw": "WC.SET_PROGRAM.PROGRAM",
        "programs_ih": "WC.SET_PROGRAM.PROGRAM",
        "programs_ov": "WC.SET_PROGRAM.PROGRAM",
        "programs_td": "WC.SET_PROGRAM.PROGRAM",
        "programs_wm": "WC.SET_PROGRAM.PROGRAM",
        "programs_ac": "WC.SET_PROGRAM.PROGRAM",
        "programs_ref": "WC.SET_PROGRAM.PROGRAM",
        "eco_pilot": "AC.PROGRAM_DETAIL.ECO_PILOT",
        "remaining_time": "ENROLLMENT_COMMON.GENERAL.REMAINING_TIME",
        "ref_zones": "IH.COMMON.COIL",
    },
    "sensor": {
        "dry_levels": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_LEVEL",
        "dry_time": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_TIME",
        "power": "OV.RECIPE_DETAIL.POWER_LEVEL",
        "remaining_time": "ENROLLMENT_COMMON.GENERAL.REMAINING_TIME",
        "temperature": "IH.COMMON.TEMPERATURE",
        "water_efficiency": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_RESULT.WATER_EFFICIENCY",
        "water_saving": "STATISTICS.SMART_AI_CYCLE.WATER_SAVING",
        "duration": "WASHING_CMD&CTRL.DRAWER_PROGRAM_FILTERS.DURATION",
        "target_temperature": "IH.COOKING_DETAIL.TEMPERATURE_TARGETING",
        "spin_speed": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.SPINSPEED",
        "steam_leve": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.STEAM_LEVEL",
        "dirt_level": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.DIRTY_LEVEL",
        "program_phases_wm": "WASHING_CMD&CTRL.STATISTICS_GRAPHIC_INSTANT_CONSUMPTION.PHASE",
        "program_phases_td": "WASHING_CMD&CTRL.STATISTICS_GRAPHIC_INSTANT_CONSUMPTION.PHASE",
        "program_phases_dw": "WASHING_CMD&CTRL.STATISTICS_GRAPHIC_INSTANT_CONSUMPTION.PHASE",
        "delay_time": "HINTS.TIPS_TIME_ENERGY_SAVING.TIPS_USE_AT_NIGHT_TITLE",
        "suggested_load": "WASHING_CMD&CTRL.DRAWER_PROGRAM_FILTERS.LOAD_CAPACITY",
        "energy_label": "WASHING_CMD&CTRL.DRAWER_PROGRAM_FILTERS.ENERGY_EFFICIENCY",
        "det_dust": "HUBS.WIDGET.STAINS_WIDGET.STAINS.SUGGESTED_DET_DUST",
        "det_liquid": "HUBS.WIDGET.STAINS_WIDGET.STAINS.SUGGESTED_DET_LIQUID",
        "errors": "ROBOT_CMD&CTRL.PHASE_ERROR.TITLE",
        "programs": "OV.TABS.CURRENT_PROGRAM",
        "room_temperature": "REF.SMART_DRINK_ASSISTANT.AMBIENT",
        "humidity": "AP.TITLES.HUMIDITY",
        "cycles_total": [
            "WASHING_CMD&CTRL.GENERAL.CYCLES",
            "WC.VIRTUAL_WINE_STATS_COUNTRY.TOTAL",
        ],
        "energy_total": [
            "MISE.ENERGY_CONSUMPTION.TITLE",
            "WC.VIRTUAL_WINE_STATS_COUNTRY.TOTAL",
        ],
        "water_total": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_RESULT.WATER_EFFICIENCY",
            "WC.VIRTUAL_WINE_STATS_COUNTRY.TOTAL",
        ],
        "energy_current": [
            "MISE.ENERGY_CONSUMPTION.TITLE",
            "CUBE90_GLOBAL.GENERAL.CURRENT",
        ],
        "water_current": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_RESULT.WATER_EFFICIENCY",
            "CUBE90_GLOBAL.GENERAL.CURRENT",
        ],
        "freezer_temp": "REF_CMD&CTRL.TEMPERATURE_DRAWER_FREEZER.FREEZER_TEMPERATURE_TITLE",
        "fridge_temp": "REF_CMD&CTRL.TEMPERATURE_DRAWER_FRIDGE.FRIDGE_TEMPERATURE_TITLE",
        "programs_dw": "WC.SET_PROGRAM.PROGRAM",
        "programs_ih": "WC.SET_PROGRAM.PROGRAM",
        "programs_ov": "WC.SET_PROGRAM.PROGRAM",
        "programs_td": "WC.SET_PROGRAM.PROGRAM",
        "programs_wm": "WC.SET_PROGRAM.PROGRAM",
        "programs_ac": "WC.SET_PROGRAM.PROGRAM",
        "programs_ref": "WC.SET_PROGRAM.PROGRAM",
    },
    "number": {
        "power_management": "HINTS.COOKING_WITH_INDUCTION.POWER_MANAGEMENT",
        "temperature": "IH.COMMON.TEMPERATURE",
        "delay_time": "HINTS.TIPS_TIME_ENERGY_SAVING.TIPS_USE_AT_NIGHT_TITLE",
        "water_hard": "WASHING_CMD&CTRL.DASHBOARD_MENU_MORE_SETTINGS_WATER.TITLE",
        "program_duration": "OV.PROGRAM_DETAIL.PROGRAM_DURATION",
        "target_temperature": "IH.COOKING_DETAIL.TEMPERATURE_TARGETING",
        "rinse_iterations": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL.DRAWER_HEADER_RINSE",
        "wash_time": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL.WASHING_TIME",
        "dry_time": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_TIME",
        "steam_level": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.STEAM_LEVEL",
        "freezer_temp_sel": ["OV.COMMON.GOAL_TEMPERATURE", "REF.ZONES.FREEZER"],
        "fridge_temp_sel": ["OV.COMMON.GOAL_TEMPERATURE", "REF.ZONES.FRIDGE"],
    },
    "climate": {
        "air_conditioner": "GLOBALS.APPLIANCES_NAME.AC",
        "fridge": "REF.ZONES.FRIDGE",
        "freezer": "REF.ZONES.FREEZER",
        "oven": "GLOBALS.APPLIANCES_NAME.OV",
    },
    "fan": {"air_extraction": "HO.DASHBOARD.AIR_EXTRACTION_TITLE"},
}
