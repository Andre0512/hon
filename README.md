# Haier hOn
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Andre0512/hon?color=green)](https://github.com/Andre0512/hon/releases/latest)
![GitHub](https://img.shields.io/github/license/Andre0512/hon?color=red)
[![Home Assistant installs](https://img.shields.io/badge/dynamic/json?color=blue&label=usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.hon.total)](https://analytics.home-assistant.io/)  
Home Assistant integration for Haier hOn: support for Haier/Candy/Hoover home appliances like washing machines.
## Supported Appliances
- Tumble Dryer
- Washer Dryer
- Washing Machine
- Oven

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
#### Add appliances or additional attributes
1. Install [pyhOn](https://github.com/Andre0512/pyhOn)
   ```commandline
    $ pip install pyhOn
    ```
2. Use the commandline tool to read out all appliance data from your account
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
- Use [pyhOn](https://github.com/Andre0512/pyhOn)s translate command to read out the official translations 

## Tested Devices
- Haier WD90-B14TEAM5
- Haier HD80-A3959
- Haier HWO60SM2F3XH
- Hoover H-WASH 500

## About this Repo
The existing integrations missed some features from the app I liked to have in HomeAssistant.
I tried to create a pull request, but in the structures of these existing repos, I find it hard to fit in my needs, so I basically rewrote everything. 
I moved the api related stuff into the package [pyhOn](https://github.com/Andre0512/pyhOn).
