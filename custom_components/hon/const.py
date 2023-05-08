from homeassistant.components.climate import (
    HVACMode,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_AUTO,
)

DOMAIN = "hon"

PLATFORMS = [
    "sensor",
    "select",
    "number",
    "switch",
    "button",
    "binary_sensor",
    "climate",
]

HON_HVAC_MODE = {
    "0": HVACMode.AUTO,
    "1": HVACMode.COOL,
    "2": HVACMode.COOL,
    "3": HVACMode.DRY,
    "4": HVACMode.HEAT,
    "5": HVACMode.FAN_ONLY,
    "6": HVACMode.FAN_ONLY,
}

HON_HVAC_PROGRAM = {
    HVACMode.AUTO: "iot_auto",
    HVACMode.COOL: "iot_cool",
    HVACMode.DRY: "iot_dry",
    HVACMode.HEAT: "iot_heat",
    HVACMode.FAN_ONLY: "iot_fan",
}

HON_FAN = {
    "1": FAN_HIGH,
    "2": FAN_MEDIUM,
    "3": FAN_LOW,
    "4": FAN_AUTO,
    "5": FAN_AUTO,
}

# These languages are official supported by hOn
LANGUAGES = [
    "cs",  # Czech
    "de",  # German
    "el",  # Greek
    "en",  # English
    "es",  # Spanish
    "fr",  # French
    "he",  # Hebrew
    "hr",  # Croatian
    "it",  # Italian
    "nl",  # Dutch
    "pl",  # Polish
    "pt",  # Portuguese
    "ro",  # Romanian
    "ru",  # Russian
    "sk",  # Slovak
    "sl",  # Slovenian
    "sr",  # Serbian
    "tr",  # Turkish
    "zh",  # Chinese
]

WASHING_PR_PHASE = {
    "0": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "1": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "2": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "3": "WASHING_CMD&CTRL.PHASE_SPIN.TITLE",
    "4": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "5": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "6": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "7": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    "9": "WASHING_CMD&CTRL.PHASE_STEAM.TITLE",
    "10": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "11": "WASHING_CMD&CTRL.PHASE_SPIN.TITLE",
    "12": "WASHING_CMD&CTRL.PHASE_WEIGHTING.TITLE",
    "13": "WASHING_CMD&CTRL.PHASE_WEIGHTING.TITLE",
    "14": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "15": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "16": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "17": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "18": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "19": "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",
    "20": "WASHING_CMD&CTRL.PHASE_TUMBLING.TITLE",
    "24": "WASHING_CMD&CTRL.PHASE_REFRESH.TITLE",
    "25": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "26": "WASHING_CMD&CTRL.PHASE_HEATING.TITLE",
    "27": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
}
MACH_MODE = {
    "0": "WASHING_CMD&CTRL.PHASE_READY.TITLE",  # NO_STATE
    "1": "WASHING_CMD&CTRL.PHASE_READY.TITLE",  # SELECTION_MODE
    "2": "WASHING_CMD&CTRL.PHASE_RUNNING.TITLE",  # EXECUTION_MODE
    "3": "WASHING_CMD&CTRL.PHASE_PAUSE.TITLE",  # PAUSE_MODE
    "4": "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",  # DELAY_START_SELECTION_MODE
    "5": "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",  # DELAY_START_EXECUTION_MODE
    "6": "WASHING_CMD&CTRL.PHASE_ERROR.TITLE",  # ERROR_MODE
    "7": "WASHING_CMD&CTRL.PHASE_READY.TITLE",  # END_MODE
    "8": "Test",  # TEST_MODE
    "9": "GLOBALS.APPLIANCE_STATUS.ENDING_PROGRAM",  # STOP_MODE
}
TUMBLE_DRYER_PR_PHASE = {
    "0": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "1": "TD_CMD&CTRL.STATUS_PHASE.PHASE_HEAT_STROKE",
    "2": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    "3": "TD_CMD&CTRL.STATUS_PHASE.PHASE_COOLDOWN",
    "11": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "13": "TD_CMD&CTRL.STATUS_PHASE.PHASE_COOLDOWN",
    "14": "TD_CMD&CTRL.STATUS_PHASE.PHASE_HEAT_STROKE",
    "15": "TD_CMD&CTRL.STATUS_PHASE.PHASE_HEAT_STROKE",
    "16": "TD_CMD&CTRL.STATUS_PHASE.PHASE_COOLDOWN",
    "17": "unknown",
    "18": "WASHING_CMD&CTRL.PHASE_TUMBLING.DASHBOARD_TITLE",
    "19": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    "20": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
}
DIRTY_LEVEL = {
    "1": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.LITTLE",
    "2": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.NORMAL",
    "3": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.VERY",
}

STEAM_LEVEL = {
    "0": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.NO_STEAM",
    "1": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_FABRICS.COTTON_TITLE",
    "2": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_FABRICS.DELICATE_TITLE",
    "3": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_FABRICS.SYNTHETIC_TITLE",
}

DISHWASHER_PR_PHASE = {
    "0": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "1": "WASHING_CMD&CTRL.PHASE_PREWASH.TITLE",
    "2": "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    "3": "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    "4": "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    "5": "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    "6": "WASHING_CMD&CTRL.PHASE_HOT_RINSE.TITLE",
}

TUMBLE_DRYER_DRY_LEVEL = {
    "0": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.NO_DRY",
    "1": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.IRON_DRY",
    "2": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.NO_DRY_IRON_TITLE",
    "3": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.CUPBOARD_DRY_TITLE",
    "4": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.EXTRA_DRY_TITLE",
    "11": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.NO_DRY",
    "12": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.IRON_DRY",
    "13": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.CUPBOARD_DRY_TITLE",
    "14": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.READY_TO_WEAR_TITLE",
    "15": "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.EXTRA_DRY_TITLE",
}

AC_MACH_MODE = {
    "0": "PROGRAMS.AC.IOT_AUTO",
    "1": "PROGRAMS.AC.IOT_COOL",
    "2": "PROGRAMS.AC.IOT_COOL",
    "3": "PROGRAMS.AC.IOT_DRY",
    "4": "PROGRAMS.AC.IOT_HEAT",
    "5": "PROGRAMS.AC.IOT_FAN",
    "6": "PROGRAMS.AC.IOT_FAN",
}

AC_FAN_MODE = {
    "1": "AC.PROGRAM_CARD.WIND_SPEED_HIGH",
    "2": "AC.PROGRAM_CARD.WIND_SPEED_MID",
    "3": "AC.PROGRAM_CARD.WIND_SPEED_LOW",
    "4": "AC.PROGRAM_CARD.WIND_SPEED_AUTO",
    "5": "AC.PROGRAM_CARD.WIND_SPEED_AUTO",
}

AC_HUMAN_SENSE = {
    "0": "AC.PROGRAM_DETAIL.TOUCH_OFF",
    "1": "AC.PROGRAM_DETAIL.AVOID_TOUCH",
    "2": "AC.PROGRAM_DETAIL.FOLLOW_TOUCH",
}

TUMBLE_DRYER_PROGRAMS = [
    "hqd_baby_care"
    "hqd_bath_towel"
    "hqd_bed_sheets"
    "hqd_bulky"
    "hqd_casual"
    "hqd_cold_wind_30"
    "hqd_cold_wind_timing"
    "hqd_cotton"
    "hqd_curtain"
    "hqd_delicate"
    "hqd_diaper"
    "hqd_duvet"
    "hqd_feather"
    "hqd_hot_wind_timing"
    "hqd_hygienic"
    "hqd_i_refresh"
    "hqd_i_refresh_pro"
    "hqd_jacket"
    "hqd_jeans"
    "hqd_luxury"
    "hqd_mix"
    "hqd_night_dry"
    "hqd_outdoor"
    "hqd_precious_cure"
    "hqd_quick_20"
    "hqd_quick_30"
    "hqd_quick_dry"
    "hqd_quilt"
    "hqd_refresh"
    "hqd_school_uniform"
    "hqd_shirt"
    "hqd_shoes"
    "hqd_silk"
    "hqd_sports"
    "hqd_synthetics"
    "hqd_timer"
    "hqd_towel"
    "hqd_underwear"
    "hqd_warm_up"
    "hqd_wool"
    "hqd_working_suit"
]

PROGRAMS_TD = [
    "active_dry",
    "allergy_care",
    "all_in_one",
    "antiallergy",
    "anti_odours",
    "auto_care",
    "baby",
    "bed_quilt",
    "care_30",
    "care_45",
    "care_59",
    "coloured",
    "daily_45_min",
    "daily_perfect_59_min",
    "darks_and_coloured",
    "delicates",
    "duvet",
    "eco",
    "ecospeed_cottons",
    "ecospeed_delicates",
    "ecospeed_mixed",
    "extra_hygiene",
    "fitness",
    "fresh_care",
    "genius",
    "hqd_baby_care",
    "hqd_bath_towel",
    "hqd_bed_sheets",
    "hqd_bulky",
    "hqd_casual",
    "hqd_cold_wind_30",
    "hqd_cold_wind_timing",
    "hqd_cotton",
    "hqd_curtain",
    "hqd_delicate",
    "hqd_diaper",
    "hqd_duvet",
    "hqd_feather",
    "hqd_hot_wind_timing",
    "hqd_hygienic",
    "hqd_i_refresh",
    "hqd_i_refresh_pro",
    "hqd_jacket",
    "hqd_jeans",
    "hqd_luxury",
    "hqd_mix",
    "hqd_night_dry",
    "hqd_outdoor",
    "hqd_precious_cure",
    "hqd_quick_20",
    "hqd_quick_30",
    "hqd_quick_dry",
    "hqd_quilt",
    "hqd_refresh",
    "hqd_school_uniform",
    "hqd_shirt",
    "hqd_shoes",
    "hqd_silk",
    "hqd_sports",
    "hqd_synthetics",
    "hqd_timer",
    "hqd_towel",
    "hqd_underwear",
    "hqd_warm_up",
    "hqd_wool",
    "hqd_working_suit",
    "hygiene",
    "iot_checkup",
    "iot_dry_anti_mites",
    "iot_dry_baby",
    "iot_dry_backpacks",
    "iot_dry_bathrobe",
    "iot_dry_bed_linen",
    "iot_dry_bed_quilt",
    "iot_dry_cotton",
    "iot_dry_cuddly_toys",
    "iot_dry_curtains",
    "iot_dry_dehumidifier",
    "iot_dry_delicates",
    "iot_dry_delicate_tablecloths",
    "iot_dry_denim_jeans",
    "iot_dry_down_jacket",
    "iot_dry_duvet",
    "iot_dry_easy_iron_cotton",
    "iot_dry_easy_iron_synthetics",
    "iot_dry_gym_fit",
    "iot_dry_lingerie",
    "iot_dry_mixed",
    "iot_dry_playsuits",
    "iot_dry_rapid_30",
    "iot_dry_rapid_59",
    "iot_dry_refresh",
    "iot_dry_regenerates_waterproof",
    "iot_dry_relax_creases",
    "iot_dry_shirts",
    "iot_dry_small_load",
    "iot_dry_swimsuits_and_bikinis",
    "iot_dry_synthetics",
    "iot_dry_synthetic_dry",
    "iot_dry_tablecloths",
    "iot_dry_technical_fabrics",
    "iot_dry_warm_embrace",
    "iot_dry_wool",
    "jeans",
    "mix_and_dry",
    "pets",
    "pre_iron",
    "rapid_30",
    "rapid_45",
    "rapid_59",
    "refresh",
    "relax_creases",
    "saving_30_min",
    "shirts",
    "shoes",
    "small_load",
    "soft_care",
    "sport_plus",
    "super_easy_iron_misti",
    "super_easy_iron_xxl",
    "super_fast_cottons",
    "super_fast_delicates",
    "synthetics",
    "total_care",
    "trainers",
    "ultra_care",
    "waterproof_revitalize",
    "whites",
    "wool",
    "woolmark",
    "xxl_load",
    "zoom_59",
]
