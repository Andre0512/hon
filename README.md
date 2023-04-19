# Haier hOn
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Andre0512/hon?color=green)](https://github.com/Andre0512/hon/releases/latest)
[![GitHub](https://img.shields.io/github/license/Andre0512/hon?color=red)](https://github.com/Andre0512/hon/blob/main/LICENSE)
[![GitHub all releases](https://img.shields.io/github/downloads/Andre0512/hon/total?color=blue)](https://tooomm.github.io/github-release-stats/?username=Andre0512&repository=hon)  
Home Assistant integration for Haier hOn: support for Haier/Candy/Hoover home appliances like washing machines.

## Supported Appliances
- [Washing Machine](https://github.com/Andre0512/hon#washing-machine)
- [Tumble Dryer](https://github.com/Andre0512/hon#tumble-dryer)
- [Washer Dryer](https://github.com/Andre0512/hon#washer-dryer)
- [Oven](https://github.com/Andre0512/hon#oven)
- [Hob](https://github.com/Andre0512/hon#hob)
- [Dish Washer](https://github.com/Andre0512/hon#dish-washer)

## Installation
**Method 1:** [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Andre0512&repository=hon&category=integration)

**Method 2:** [HACS](https://hacs.xyz/) > Integrations > Add Integration > **Haier hOn** > Install  

**Method 3:** Manually copy `hon` folder from [latest release](https://github.com/Andre0512/hon/releases/latest) to `config/custom_components` folder.

_Restart Home Assistant_

## Configuration

**Method 1**: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=hon)

**Method 2**: Settings > Devices & Services > Add Integration > **Haier hOn**  
_If the integration is not in the list, you need to clear the browser cache._

## Contribute
Any kind of contribution is welcome!
### Read out device data
If you want to make a request for adding new appliances or additional attributes and don't want to use the command line, here is how you can read out your device data.
For every device exists a hidden button which can be used to log all info of your appliance.
1. Enable the "Log Device Info" button  
   _This button can be found in the diagnostic section of your device or in the entity overview if "show disabled entities" is enabled._
2. Press the button
3. Go to Settings > System > Logs, click _load full logs_ and scroll down  
   _The formatting is messy if you not load full logs_
4. Here you can find all data which can be read out via the api
   ```yaml
   data:
     appliance:
       applianceId: 12-34-56-78-90-ab#2022-10-25T19:47:11Z
       applianceModelId: 1569 
       ...
   ```
5. Copy this data and create a [new issue](https://github.com/Andre0512/hon/issues/new) with your request

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

## Tested Devices
- Haier WD90-B14TEAM5
- Haier HD80-A3959
- Haier HWO60SM2F3XH
- Hoover H-WASH 500
- Candy CIS633SCTTWIFI
- Haier XIB 3B2SFS-80
- Haier XIB 6B2D3FB

## About this Repo
The existing integrations missed some features from the app I liked to have in HomeAssistant.
I tried to create a pull request, but in the structures of these existing repos, I find it hard to fit in my needs, so I basically rewrote everything. 
I moved the api related stuff into the package [pyhOn](https://github.com/Andre0512/pyhOn).

## Appliance Features

### Dish washer
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Dish Washer | `mdi:dishwasher` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Add Dish | `mdi:silverware-fork-knife` | `switch` | `startProgram.addDish` |
| Delay time | `mdi:timer-plus` | `number` | `startProgram.delayTime` |
| Eco Express | `mdi:sprout` | `switch` | `startProgram.ecoExpress` |
| Eco Index | `mdi:sprout` | `sensor` | `startProgram.ecoIndex` |
| Energy Label | `mdi:lightning-bolt-circle` | `sensor` | `startProgram.energyLabel` |
| Extra Dry | `mdi:hair-dryer` | `switch` | `startProgram.extraDry` |
| Half Load | `mdi:fraction-one-half` | `switch` | `startProgram.halfLoad` |
| Open Door | `mdi:door-open` | `switch` | `startProgram.openDoor` |
| Program |  | `select` | `startProgram.program` |
| Temperature | `mdi:thermometer` | `sensor` | `startProgram.temp` |
| Three in One | `mdi:numeric-3-box-outline` | `switch` | `startProgram.threeInOne` |
| Time | `mdi:timer` | `sensor` | `startProgram.remainingTime` |
| Water Efficiency | `mdi:water` | `sensor` | `startProgram.waterEfficiency` |
| Water Saving | `mdi:water-percent` | `sensor` | `startProgram.waterSaving` |
| Water hard | `mdi:water` | `number` | `startProgram.waterHard` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Connection |  | `binary_sensor` | `attributes.lastConnEvent.category` |
| Door |  | `binary_sensor` | `doorStatus` |
| Error | `mdi:math-log` | `sensor` | `errors` |
| Machine Status | `mdi:information` | `sensor` | `machMode` |
| Remaining Time | `mdi:timer` | `sensor` | `remainingTimeMM` |
| Rinse Aid | `mdi:spray-bottle` | `binary_sensor` | `rinseAidStatus` |
| Salt | `mdi:shaker-outline` | `binary_sensor` | `saltStatus` |

### Hob
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Start Program | `mdi:pot-steam` | `button` | `startProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Power Management | `mdi:timelapse` | `number` | `startProgram.powerManagement` |
| Program |  | `select` | `startProgram.program` |
| Temperature | `mdi:thermometer` | `number` | `startProgram.temp` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Connection | `mdi:wifi` | `binary_sensor` | `attributes.lastConnEvent.category` |
| Error | `mdi:math-log` | `sensor` | `errors` |
| Hob Lock |  | `binary_sensor` | `hobLockStatus` |
| Hot Status |  | `binary_sensor` | `hotStatus` |
| On | `mdi:power-cycle` | `binary_sensor` | `attributes.parameters.onOffStatus` |
| Pan Status | `mdi:pot-mix` | `binary_sensor` | `panStatus` |
| Power | `mdi:lightning-bolt` | `sensor` | `power` |
| Remaining Time | `mdi:timer` | `sensor` | `remainingTimeMM` |
| Remote Control | `mdi:remote` | `binary_sensor` | `attributes.parameters.remoteCtrValid` |
| Temperature | `mdi:thermometer` | `sensor` | `temp` |

### Oven
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Start Program | `mdi:power-cycle` | `button` | `startProgram` |
| Stop Program | `mdi:power-off` | `button` | `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Delay time | `mdi:timer-plus` | `number` | `startProgram.delayTime` |
| Preheat |  | `select` | `startProgram.preheatStatus` |
| Program |  | `select` | `startProgram.program` |
| Program Duration | `mdi:timelapse` | `number` | `startProgram.prTime` |
| Target Temperature | `mdi:thermometer` | `number` | `startProgram.tempSel` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Connection | `mdi:wifi` | `binary_sensor` | `attributes.lastConnEvent.category` |
| On | `mdi:power-cycle` | `binary_sensor` | `attributes.parameters.onOffStatus` |
| Remaining Time | `mdi:timer` | `sensor` | `remainingTimeMM` |
| Remote Control | `mdi:remote` | `binary_sensor` | `attributes.parameters.remoteCtrValid` |
| Start Time | `mdi:clock-start` | `sensor` | `delayTime` |
| Temperature | `mdi:thermometer` | `sensor` | `temp` |
| Temperature Selected | `mdi:thermometer` | `sensor` | `tempSel` |

### Tumble dryer
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Pause Tumble Dryer | `mdi:pause` | `switch` | `pauseProgram` / `resumeProgram` |
| Tumble Dryer | `mdi:tumble-dryer` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Anti-Crease time | `mdi:timer` | `number` | `startProgram.antiCreaseTime` |
| Delay time | `mdi:timer-plus` | `number` | `startProgram.delayTime` |
| Dry level | `mdi:hair-dryer` | `number` | `startProgram.dryLevel` |
| Program |  | `select` | `startProgram.program` |
| Sterilization status | `mdi:clock-start` | `number` | `startProgram.sterilizationStatus` |
| Temperature level | `mdi:thermometer` | `number` | `startProgram.tempLevel` |
| Time | `mdi:timer` | `select` | `startProgram.dryTimeMM` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Connection |  | `binary_sensor` | `attributes.lastConnEvent.category` |
| Door |  | `binary_sensor` | `doorStatus` |
| Dry level | `mdi:hair-dryer` | `sensor` | `dryLevel` |
| Error | `mdi:math-log` | `sensor` | `errors` |
| Machine Status | `mdi:information` | `sensor` | `machMode` |
| Program | `mdi:tumble-dryer` | `sensor` | `prCode` |
| Program Phase | `mdi:tumble-dryer` | `sensor` | `prPhase` |
| Remaining Time | `mdi:timer` | `sensor` | `remainingTimeMM` |
| Start Time | `mdi:clock-start` | `sensor` | `delayTime` |
| Temperature level | `mdi:thermometer` | `sensor` | `tempLevel` |

### Washer dryer
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Pause Washing Machine | `mdi:pause` | `switch` | `pauseProgram` / `resumeProgram` |
| Washing Machine | `mdi:washing-machine` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Delay Time | `mdi:timer-plus` | `number` | `startProgram.delayTime` |
| Program |  | `select` | `startProgram.program` |
| Suggested weight | `mdi:weight-kilogram` | `sensor` | `startProgram.weight` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Acqua Plus |  | `binary_sensor` | `acquaplus` |
| Anti-Crease |  | `binary_sensor` | `anticrease` |
| Current Electricity Used | `mdi:lightning-bolt` | `sensor` | `currentElectricityUsed` |
| Current Program | `mdi:tumble-dryer` | `sensor` | `prCode` |
| Current Temperature | `mdi:thermometer` | `sensor` | `temp` |
| Current Water Used | `mdi:water` | `sensor` | `currentWaterUsed` |
| Dirt level | `mdi:liquid-spot` | `sensor` | `dirtyLevel` |
| Dry level | `mdi:hair-dryer` | `sensor` | `dryLevel` |
| Extra Rinse 1 |  | `binary_sensor` | `extraRinse1` |
| Extra Rinse 2 |  | `binary_sensor` | `extraRinse2` |
| Extra Rinse 3 |  | `binary_sensor` | `extraRinse3` |
| Good Night Mode |  | `binary_sensor` | `goodNight` |
| Machine Status | `mdi:information` | `sensor` | `machMode` |
| Pre Wash |  | `binary_sensor` | `startProgram.prewash` |
| Program Phase | `mdi:tumble-dryer` | `sensor` | `prPhase` |
| Remaining Time | `mdi:timer` | `sensor` | `remainingTimeMM` |
| Remote Control | `mdi:remote` | `binary_sensor` | `attributes.lastConnEvent.category` |
| Spin Speed | `mdi:fast-forward-outline` | `sensor` | `spinSpeed` |
| Steam level | `mdi:smoke` | `sensor` | `steamLevel` |
| Total Power |  | `sensor` | `totalElectricityUsed` |
| Total Wash Cycle | `mdi:counter` | `sensor` | `totalWashCycle` |
| Total Water |  | `sensor` | `totalWaterUsed` |

### Washing machine
#### Controls
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Pause Washing Machine | `mdi:pause` | `switch` | `pauseProgram` / `resumeProgram` |
| Washing Machine | `mdi:washing-machine` | `switch` | `startProgram` / `stopProgram` |
#### Configs
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Delay Status | `mdi:timer-check` | `switch` | `startProgram.delayStatus` |
| Delay Time | `mdi:timer-plus` | `number` | `startProgram.delayTime` |
| Main Wash Time | `mdi:clock-start` | `number` | `startProgram.mainWashTime` |
| Program |  | `select` | `startProgram.program` |
| Rinse Iterations | `mdi:rotate-right` | `number` | `startProgram.rinseIterations` |
| Soak Prewash Selection | `mdi:tshirt-crew` | `switch` | `startProgram.haier_SoakPrewashSelection` |
| Spin speed | `mdi:numeric` | `select` | `startProgram.spinSpeed` |
| Suggested weight | `mdi:weight-kilogram` | `sensor` | `startProgram.weight` |
| Temperature | `mdi:thermometer` | `select` | `startProgram.temp` |
#### Sensors
| Name | Icon | Entity | Key |
| --- | --- | --- | --- |
| Current Electricity Used | `mdi:lightning-bolt` | `sensor` | `currentElectricityUsed` |
| Current Water Used | `mdi:water` | `sensor` | `currentWaterUsed` |
| Door |  | `binary_sensor` | `doorStatus` |
| Door Lock |  | `binary_sensor` | `doorLockStatus` |
| Error | `mdi:math-log` | `sensor` | `errors` |
| Machine Status | `mdi:information` | `sensor` | `machMode` |
| Remaining Time | `mdi:timer` | `sensor` | `remainingTimeMM` |
| Remote Control | `mdi:remote` | `binary_sensor` | `attributes.lastConnEvent.category` |
| Spin Speed | `mdi:speedometer` | `sensor` | `spinSpeed` |
| Total Power |  | `sensor` | `totalElectricityUsed` |
| Total Wash Cycle | `mdi:counter` | `sensor` | `totalWashCycle` |
| Total Water |  | `sensor` | `totalWaterUsed` |
