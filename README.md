# Haier hOn
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Andre0512/hon?color=green)](https://github.com/Andre0512/hon/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/pyhon?label=pyhOn)](https://github.com/Andre0512/pyhOn)
[![GitHub](https://img.shields.io/github/license/Andre0512/hon?color=red)](https://github.com/Andre0512/hon/blob/main/LICENSE)
[![GitHub all releases](https://img.shields.io/github/downloads/Andre0512/hon/total?color=blue)](https://tooomm.github.io/github-release-stats/?username=Andre0512&repository=hon)  
Home Assistant integration for [Haier's mobile app hOn](https://hon-smarthome.com/).

## Supported Appliances
- [Washing Machine](https://github.com/Andre0512/hon#washing-machine)
- [Tumble Dryer](https://github.com/Andre0512/hon#tumble-dryer)
- [Washer Dryer](https://github.com/Andre0512/hon#washer-dryer)
- [Oven](https://github.com/Andre0512/hon#oven)
- [Dish Washer](https://github.com/Andre0512/hon#dish-washer)
- [Hob](https://github.com/Andre0512/hon#hob) [BETA]
- [Air conditioner](https://github.com/Andre0512/hon#air-conditioner) [BETA]
- [Fridge](https://github.com/Andre0512/hon#fridge) [BETA]

## Installation
**Method 1:** [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Andre0512&repository=hon&category=integration)

**Method 2:** [HACS](https://hacs.xyz/) > Integrations > Add Integration > **Haier hOn** > Install  

**Method 3:** Manually copy `hon` folder from [latest release](https://github.com/Andre0512/hon/releases/latest) to `config/custom_components` folder.

_Restart Home Assistant_

## Configuration

**Method 1**: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=hon)

**Method 2**: Settings > Devices & Services > Add Integration > **Haier hOn**  
_If the integration is not in the list, you need to clear the browser cache._

## Supported Languages
Translation of internal names like programs are available for all languages which are official supported by the hOn app:
* 🇨🇳 Chinese
* 🇭🇷 Croatian
* 🇨🇿 Czech
* 🇳🇱 Dutch
* 🇬🇧 English
* 🇫🇷 French
* 🇩🇪 German
* 🇬🇷 Greek
* 🇮🇱 Hebrew
* 🇮🇹 Italian
* 🇵🇱 Polish
* 🇵🇹 Portuguese
* 🇷🇴 Romanian
* 🇷🇺 Russian
* 🇷🇸 Serbian
* 🇸🇰 Slovak
* 🇸🇮 Slovenian
* 🇪🇸 Spanish
* 🇹🇷 Turkish

## Examples
### Washing Machine
![washing_machine.png](assets/washing_machine.png)

## Supported Models
Support has been confirmed for these models, but many more will work. Please add already supported devices [with this form to complete the list](https://forms.gle/bTSD8qFotdZFytbf8).
- Haier AS25PBAHRA
- Haier EG9012B19SU1JD
- Haier HD80-A3959
- Haier HW90-B14TEAM5
- Haier HW100-B14959U1
- Haier HWD100-B14979
- Haier HWO60SM2F3XH
- Haier XIB 3B2SFS-80
- Haier XIB 6B2D3FB
- Candy CIS633SCTTWIFI
- Candy CSOE C10DE-80
- Candy ROE H9A3TCEX-S
- Candy RPW41066BWMR/1-S
- Hoover H-WASH 500
- Hoover H-DRY 500
- Hoover H7W4 48MBC-S
- Hoover H9A3TCBEXS-S
- Hoover HFB 6B2S3FX
- Hoover HLE C10DCE-80
- Hoover HSOT3161WG
- Hoover HWPD 69AMBC/1-S
- Hoover HWPS4954DAMR-11
- Hoover NDE H10A2TCE-80
- Hoover NDE H9A2TSBEXS-S
- Hoover NDPHY10A2TCBEXSS

## Contribute
Any kind of contribution is welcome!
### Read out device data
If you want to make a request for adding new appliances or additional attributes and don't want to use the command line, here is how you can read out your device data.
For every device exists a hidden button which can be used to log all infos of your appliance.
1. Enable the "Show Device Info" button  
   _This button can be found in the diagnostic section of your device or in the entity overview if "show disabled entities" is enabled._
2. Press the button to create a notification
3. Open home assistant notifications and copy the message (Crtl+A, Ctrl+C)
### Add appliances or additional attributes
1. Install [pyhOn](https://github.com/Andre0512/pyhOn)
   ```commandline
    $ pip install pyhOn
    ```
2. Use the command line tool to read out all appliance data from your account
    ```commandline
    $ pyhOn
    User for hOn account: user.name@example.com
    Password for hOn account: ********
    ========== WM - Washing Machine ==========
    commands:
      pauseProgram: pauseProgram command
      resumeProgram: resumeProgram command
      startProgram: startProgram command
      stopProgram: stopProgram command
    data:
      actualWeight: 0
      airWashTempLevel: 0
      airWashTime: 0
      antiAllergyStatus: 0
      ...
    ```
3. Fork this repository and clone it to your local machine
4. Add the keys of the attributes you'd like to have as `EntityDescription` into this Repository  
   _Example: Add pause button_
    ```python
    BUTTONS: dict[str, tuple[ButtonEntityDescription, ...]] = {
        "WM": (                        # WM is the applianceTypeName
            ButtonEntityDescription(
                key="pauseProgram",    # key from pyhOn
                name="Pause Program",  # name in home assistant
                icon="mdi:pause",      # icon in home assistant
                ...
            ),
        ...
    ```
5. Create a [pull request](https://github.com/Andre0512/hon/pulls)

#### Tips and Tricks
- If you want to have some states humanreadable, have a look at the `translation_key` parameter of the `EntityDescription`.
- If you need to implement some more logic, create a pull request to the underlying library. There we collect special requirements in the `appliances` directory.
- Use [pyhOn's translate command](https://github.com/Andre0512/pyhOn#translation) to read out the official translations

## Special Thanks
- to [@alexandre-leites](https://github.com/alexandre-leites), [@MiguelAngelLV](https://github.com/MiguelAngelLV) and [@drudgebg](https://github.com/drudgebg) for contributing early to this project and adding new integrations.
- to [gvigroux/hon](https://github.com/gvigroux/hon), [signalize/hon-app-research](https://github.com/signalize/hon-app-research) and [slegars56/hon](https://github.com/slegars56/hon) for inspiring me to do this integration and for doing pioneer work on the hOn api.
- to everyone who contributed, created an issue, gave this repo a star, and used this integration.
- to the patience of my girlfriend as I work on this integration.

## Appliance Features

### Air conditioner
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| 10° Heating | `heat-wave` | `switch` | `settings.10degreeHeatingStatus` |
| Air Conditioner | `air-conditioner` | `climate` | `settings` |
| Echo | `account-voice` | `switch` | `settings.echoStatus` |
| Eco Mode |  | `switch` | `settings.ecoMode` |
| Health Mode | `medication-outline` | `switch` | `settings.healthMode` |
| Mute | `volume-off` | `switch` | `settings.muteStatus` |
| Rapid Mode | `run-fast` | `switch` | `settings.rapidMode` |
| Screen Display | `monitor-small` | `switch` | `settings.screenDisplayStatus` |
| Self Cleaning | `air-filter` | `switch` | `settings.selfCleaningStatus` |
| Self Cleaning 56 | `air-filter` | `switch` | `settings.selfCleaning56Status` |
| Silent Sleep | `bed` | `switch` | `settings.silentSleepStatus` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Program |  | `select` | `startProgram.program` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Eco Pilot | `run` | `select` | `settings.humanSensingStatus` |
| Target Temperature | `thermometer` | `number` | `settings.tempSel` |

### Dish washer
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Buzzer Disabled | `volume-off` | `switch` | `settings.buzzerDisabled` |
| Dish Washer | `dishwasher` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Add Dish | `silverware-fork-knife` | `switch` | `startProgram.addDish` |
| Delay time | `timer-plus` | `number` | `startProgram.delayTime` |
| Eco Express | `sprout` | `switch` | `startProgram.ecoExpress` |
| Eco Index | `sprout` | `sensor` | `startProgram.ecoIndex` |
| Energy Label | `lightning-bolt-circle` | `sensor` | `startProgram.energyLabel` |
| Extra Dry | `hair-dryer` | `switch` | `startProgram.extraDry` |
| Half Load | `fraction-one-half` | `switch` | `startProgram.halfLoad` |
| Open Door | `door-open` | `switch` | `startProgram.openDoor` |
| Program |  | `select` | `startProgram.program` |
| Remaining Time | `timer` | `select` | `startProgram.remainingTime` |
| Temperature | `thermometer` | `select` | `startProgram.temp` |
| Temperature | `thermometer` | `sensor` | `startProgram.temp` |
| Three in One | `numeric-3-box-outline` | `switch` | `startProgram.threeInOne` |
| Time | `timer` | `sensor` | `startProgram.remainingTime` |
| Water Efficiency | `water` | `sensor` | `startProgram.waterEfficiency` |
| Water Saving | `water-percent` | `sensor` | `startProgram.waterSaving` |
| Water hard | `water` | `number` | `startProgram.waterHard` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Connection |  | `binary_sensor` | `attributes.lastConnEvent.category` |
| Door |  | `binary_sensor` | `doorStatus` |
| Error | `math-log` | `sensor` | `errors` |
| Machine Status | `information` | `sensor` | `machMode` |
| Program Phase | `washing-machine` | `sensor` | `prPhase` |
| Remaining Time | `timer` | `sensor` | `remainingTimeMM` |
| Rinse Aid | `spray-bottle` | `binary_sensor` | `rinseAidStatus` |
| Salt | `shaker-outline` | `binary_sensor` | `saltStatus` |

### Hob
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Start Program | `pot-steam` | `button` | `startProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Power Management | `timelapse` | `number` | `startProgram.powerManagement` |
| Program |  | `select` | `startProgram.program` |
| Temperature | `thermometer` | `number` | `startProgram.temp` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Connection | `wifi` | `binary_sensor` | `attributes.lastConnEvent.category` |
| Error | `math-log` | `sensor` | `errors` |
| Hob Lock |  | `binary_sensor` | `hobLockStatus` |
| Hot Status |  | `binary_sensor` | `hotStatus` |
| On | `power-cycle` | `binary_sensor` | `attributes.parameters.onOffStatus` |
| Pan Status | `pot-mix` | `binary_sensor` | `panStatus` |
| Power | `lightning-bolt` | `sensor` | `power` |
| Remaining Time | `timer` | `sensor` | `remainingTimeMM` |
| Temperature | `thermometer` | `sensor` | `temp` |

### Oven
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Oven | `toaster-oven` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Delay time | `timer-plus` | `number` | `startProgram.delayTime` |
| Preheat | `thermometer-chevron-up` | `switch` | `startProgram.preheatStatus` |
| Program |  | `select` | `startProgram.program` |
| Program Duration | `timelapse` | `number` | `startProgram.prTime` |
| Target Temperature | `thermometer` | `number` | `startProgram.tempSel` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Connection | `wifi` | `binary_sensor` | `attributes.lastConnEvent.category` |
| On | `power-cycle` | `binary_sensor` | `attributes.parameters.onOffStatus` |
| Remaining Time | `timer` | `sensor` | `remainingTimeMM` |
| Start Time | `clock-start` | `sensor` | `delayTime` |
| Temperature | `thermometer` | `sensor` | `temp` |
| Temperature Selected | `thermometer` | `sensor` | `tempSel` |

### Fridge
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Auto-Set Mode | `thermometer-auto` | `switch` | `settings.intelligenceMode` |
| Super Cool | `snowflake` | `switch` | `settings.quickModeZ2` |
| Super Freeze | `snowflake-variant` | `switch` | `settings.quickModeZ1` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Program |  | `select` | `startProgram.program` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Auto-Set Mode | `thermometer-auto` | `binary_sensor` | `intelligenceMode` |
| Door Status Freezer | `fridge-top` | `binary_sensor` | `doorStatusZ1` |
| Door Status Fridge | `fridge-bottom` | `binary_sensor` | `door2StatusZ1` |
| Freezer Temperature | `thermometer` | `number` | `settings.tempSelZ2` |
| Fridge Temperature | `thermometer` | `number` | `settings.tempSelZ1` |
| Holiday Mode | `palm-tree` | `binary_sensor` | `holidayMode` |
| Room Humidity | `water-percent` | `sensor` | `humidityEnv` |
| Room Temperature | `home-thermometer-outline` | `sensor` | `tempEnv` |
| Super Cool | `snowflake` | `binary_sensor` | `quickModeZ2` |
| Super Freeze | `snowflake-variant` | `binary_sensor` | `quickModeZ1` |
| Temperature Freezer | `snowflake-thermometer` | `sensor` | `tempZ2` |
| Temperature Fridge | `thermometer` | `sensor` | `tempZ1` |

### Tumble dryer
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Pause Tumble Dryer | `pause` | `switch` | `pauseProgram` / `resumeProgram` |
| Tumble Dryer | `tumble-dryer` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Anti-Crease | `timer` | `switch` | `startProgram.antiCreaseTime` |
| Anti-Crease | `timer` | `switch` | `startProgram.anticrease` |
| Delay time | `timer-plus` | `number` | `startProgram.delayTime` |
| Dry Time |  | `number` | `startProgram.dryTime` |
| Dry Time | `timer` | `select` | `startProgram.dryTimeMM` |
| Dry level | `hair-dryer` | `select` | `startProgram.dryLevel` |
| Energy Label | `lightning-bolt-circle` | `sensor` | `startProgram.energyLabel` |
| Program |  | `select` | `startProgram.program` |
| Steam Type | `weather-dust` | `sensor` | `steamType` |
| Steam level | `smoke` | `sensor` | `startProgram.steamLevel` |
| Sterilization | `clock-start` | `switch` | `startProgram.sterilizationStatus` |
| Suggested Load | `weight-kilogram` | `sensor` | `startProgram.suggestedLoadD` |
| Temperature level | `thermometer` | `number` | `startProgram.tempLevel` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Anti-Crease |  | `binary_sensor` | `anticrease` |
| Connection |  | `binary_sensor` | `attributes.lastConnEvent.category` |
| Door |  | `binary_sensor` | `doorStatus` |
| Dry level | `hair-dryer` | `sensor` | `dryLevel` |
| Error | `math-log` | `sensor` | `errors` |
| Machine Status | `information` | `sensor` | `machMode` |
| Program | `tumble-dryer` | `sensor` | `programName` |
| Program Phase | `washing-machine` | `sensor` | `prPhase` |
| Remaining Time | `timer` | `sensor` | `remainingTimeMM` |
| Start Time | `clock-start` | `sensor` | `delayTime` |
| Steam level | `smoke` | `sensor` | `steamLevel` |
| Temperature level | `thermometer` | `sensor` | `tempLevel` |

### Washer dryer
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Pause Washer Dryer | `pause` | `switch` | `pauseProgram` / `resumeProgram` |
| Washer Dryer | `washing-machine` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Acqua Plus | `water-plus` | `switch` | `startProgram.acquaplus` |
| Anti-Crease | `timer` | `switch` | `startProgram.antiCreaseTime` |
| Anti-Crease | `timer` | `switch` | `startProgram.anticrease` |
| Auto Dose Detergent | `cup` | `switch` | `startProgram.autoDetergentStatus` |
| Auto Dose Softener | `teddy-bear` | `switch` | `startProgram.autoSoftenerStatus` |
| Delay Status | `timer-check` | `switch` | `startProgram.delayStatus` |
| Delay Time | `timer-plus` | `number` | `startProgram.delayTime` |
| Dry Time |  | `number` | `startProgram.dryTime` |
| Dry Time | `timer` | `select` | `startProgram.dryTimeMM` |
| Dry level | `hair-dryer` | `select` | `startProgram.dryLevel` |
| Energy Label | `lightning-bolt-circle` | `sensor` | `startProgram.energyLabel` |
| Extra Rinse 1 | `numeric-1-box-multiple-outline` | `switch` | `startProgram.extraRinse1` |
| Extra Rinse 2 | `numeric-2-box-multiple-outline` | `switch` | `startProgram.extraRinse2` |
| Extra Rinse 3 | `numeric-3-box-multiple-outline` | `switch` | `startProgram.extraRinse3` |
| Good Night | `weather-night` | `switch` | `startProgram.goodNight` |
| Keep Fresh | `refresh-circle` | `switch` | `startProgram.permanentPressStatus` |
| Liquid Detergent Dose | `cup-water` | `sensor` | `startProgram.liquidDetergentDose` |
| Main Wash Time | `clock-start` | `number` | `startProgram.mainWashTime` |
| Powder Detergent Dose | `cup` | `sensor` | `startProgram.powderDetergentDose` |
| Program |  | `select` | `startProgram.program` |
| Remaining Time | `timer` | `sensor` | `startProgram.remainingTime` |
| Rinse Iterations | `rotate-right` | `number` | `startProgram.rinseIterations` |
| Soak Prewash Selection | `tshirt-crew` | `switch` | `startProgram.haier_SoakPrewashSelection` |
| Spin speed | `numeric` | `select` | `startProgram.spinSpeed` |
| Steam Level | `weather-dust` | `number` | `startProgram.steamLevel` |
| Steam Type | `weather-dust` | `sensor` | `steamType` |
| Steam level | `smoke` | `sensor` | `startProgram.steamLevel` |
| Sterilization | `clock-start` | `switch` | `startProgram.sterilizationStatus` |
| Suggested Load | `weight-kilogram` | `sensor` | `startProgram.suggestedLoadW` |
| Suggested Load | `weight-kilogram` | `sensor` | `startProgram.suggestedLoadD` |
| Suggested weight | `weight-kilogram` | `sensor` | `startProgram.weight` |
| Temperature | `thermometer` | `select` | `startProgram.temp` |
| Temperature level | `thermometer` | `number` | `startProgram.tempLevel` |
| Water hard | `water` | `number` | `startProgram.waterHard` |
| lang |  | `number` | `startProgram.lang` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Acqua Plus |  | `binary_sensor` | `acquaplus` |
| Anti-Crease |  | `binary_sensor` | `anticrease` |
| Current Electricity Used | `lightning-bolt` | `sensor` | `currentElectricityUsed` |
| Current Temperature | `thermometer` | `sensor` | `temp` |
| Current Water Used | `water` | `sensor` | `currentWaterUsed` |
| Dirt level | `liquid-spot` | `sensor` | `dirtyLevel` |
| Door |  | `binary_sensor` | `doorStatus` |
| Door Lock |  | `binary_sensor` | `doorLockStatus` |
| Dry level | `hair-dryer` | `sensor` | `dryLevel` |
| Error | `math-log` | `sensor` | `errors` |
| Extra Rinse 1 |  | `binary_sensor` | `extraRinse1` |
| Extra Rinse 2 |  | `binary_sensor` | `extraRinse2` |
| Extra Rinse 3 |  | `binary_sensor` | `extraRinse3` |
| Good Night Mode |  | `binary_sensor` | `goodNight` |
| Machine Status | `information` | `sensor` | `machMode` |
| Pre Wash |  | `binary_sensor` | `startProgram.prewash` |
| Program | `tumble-dryer` | `sensor` | `programName` |
| Program Phase | `washing-machine` | `sensor` | `prPhase` |
| Remaining Time | `timer` | `sensor` | `remainingTimeMM` |
| Remote Control | `remote` | `binary_sensor` | `attributes.lastConnEvent.category` |
| Spin Speed | `speedometer` | `sensor` | `spinSpeed` |
| Start Time | `clock-start` | `sensor` | `delayTime` |
| Steam level | `smoke` | `sensor` | `steamLevel` |
| Temperature level | `thermometer` | `sensor` | `tempLevel` |
| Total Power |  | `sensor` | `totalElectricityUsed` |
| Total Wash Cycle | `counter` | `sensor` | `totalWashCycle` |
| Total Water |  | `sensor` | `totalWaterUsed` |

### Washing machine
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Pause Washing Machine | `pause` | `switch` | `pauseProgram` / `resumeProgram` |
| Washing Machine | `washing-machine` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Acqua Plus | `water-plus` | `switch` | `startProgram.acquaplus` |
| Auto Dose Detergent | `cup` | `switch` | `startProgram.autoDetergentStatus` |
| Auto Dose Softener | `teddy-bear` | `switch` | `startProgram.autoSoftenerStatus` |
| Delay Status | `timer-check` | `switch` | `startProgram.delayStatus` |
| Delay Time | `timer-plus` | `number` | `startProgram.delayTime` |
| Energy Label | `lightning-bolt-circle` | `sensor` | `startProgram.energyLabel` |
| Extra Rinse 1 | `numeric-1-box-multiple-outline` | `switch` | `startProgram.extraRinse1` |
| Extra Rinse 2 | `numeric-2-box-multiple-outline` | `switch` | `startProgram.extraRinse2` |
| Extra Rinse 3 | `numeric-3-box-multiple-outline` | `switch` | `startProgram.extraRinse3` |
| Good Night | `weather-night` | `switch` | `startProgram.goodNight` |
| Keep Fresh | `refresh-circle` | `switch` | `startProgram.permanentPressStatus` |
| Liquid Detergent Dose | `cup-water` | `sensor` | `startProgram.liquidDetergentDose` |
| Main Wash Time | `clock-start` | `number` | `startProgram.mainWashTime` |
| Powder Detergent Dose | `cup` | `sensor` | `startProgram.powderDetergentDose` |
| Program |  | `select` | `startProgram.program` |
| Remaining Time | `timer` | `sensor` | `startProgram.remainingTime` |
| Rinse Iterations | `rotate-right` | `number` | `startProgram.rinseIterations` |
| Soak Prewash Selection | `tshirt-crew` | `switch` | `startProgram.haier_SoakPrewashSelection` |
| Spin speed | `numeric` | `select` | `startProgram.spinSpeed` |
| Steam Level | `weather-dust` | `number` | `startProgram.steamLevel` |
| Suggested Load | `weight-kilogram` | `sensor` | `startProgram.suggestedLoadW` |
| Suggested weight | `weight-kilogram` | `sensor` | `startProgram.weight` |
| Temperature | `thermometer` | `select` | `startProgram.temp` |
| Water hard | `water` | `number` | `startProgram.waterHard` |
| lang |  | `number` | `startProgram.lang` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Acqua Plus |  | `binary_sensor` | `acquaplus` |
| Current Electricity Used | `lightning-bolt` | `sensor` | `currentElectricityUsed` |
| Current Temperature | `thermometer` | `sensor` | `temp` |
| Current Water Used | `water` | `sensor` | `currentWaterUsed` |
| Dirt level | `liquid-spot` | `sensor` | `dirtyLevel` |
| Door |  | `binary_sensor` | `doorStatus` |
| Door Lock |  | `binary_sensor` | `doorLockStatus` |
| Error | `math-log` | `sensor` | `errors` |
| Extra Rinse 1 |  | `binary_sensor` | `extraRinse1` |
| Extra Rinse 2 |  | `binary_sensor` | `extraRinse2` |
| Extra Rinse 3 |  | `binary_sensor` | `extraRinse3` |
| Good Night Mode |  | `binary_sensor` | `goodNight` |
| Machine Status | `information` | `sensor` | `machMode` |
| Pre Wash |  | `binary_sensor` | `startProgram.prewash` |
| Program Phase | `washing-machine` | `sensor` | `prPhase` |
| Remaining Time | `timer` | `sensor` | `remainingTimeMM` |
| Remote Control | `remote` | `binary_sensor` | `attributes.lastConnEvent.category` |
| Spin Speed | `speedometer` | `sensor` | `spinSpeed` |
| Total Power |  | `sensor` | `totalElectricityUsed` |
| Total Wash Cycle | `counter` | `sensor` | `totalWashCycle` |
| Total Water |  | `sensor` | `totalWaterUsed` |
