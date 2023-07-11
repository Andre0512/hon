# Haier hOn
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Andre0512/hon?color=green)](https://github.com/Andre0512/hon/releases/latest)
[![GitHub](https://img.shields.io/github/license/Andre0512/hon?color=red)](https://github.com/Andre0512/hon/blob/main/LICENSE)
[![GitHub all releases](https://img.shields.io/github/downloads/Andre0512/hon/total?color=blue)](https://tooomm.github.io/github-release-stats/?username=Andre0512&repository=hon)  
Support for home appliances of [Haier's mobile app hOn](https://hon-smarthome.com/) based on [pyhOn](https://github.com/Andre0512/pyhon).

## Supported Appliances
- [Washing Machine](https://github.com/Andre0512/hon#washing-machine)
- [Tumble Dryer](https://github.com/Andre0512/hon#tumble-dryer)
- [Washer Dryer](https://github.com/Andre0512/hon#washer-dryer)
- [Oven](https://github.com/Andre0512/hon#oven)
- [Dish Washer](https://github.com/Andre0512/hon#dish-washer)
- [Air Conditioner](https://github.com/Andre0512/hon#air-conditioner)
- [Fridge](https://github.com/Andre0512/hon#fridge)
- [Induction Hob](https://github.com/Andre0512/hon#induction-hob) [BETA]
- [Hood](https://github.com/Andre0512/hon#hood) [BETA]
- [Wine Cellar](https://github.com/Andre0512/hon#wine-cellar) [BETA]
- [Air Purifier](https://github.com/Andre0512/hon#air-purifier) [BETA]

## Configuration

**Method 1**: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=hon)

**Method 2**: Settings > Devices & Services > Add Integration > **Haier hOn**  
_If the integration is not in the list, you need to clear the browser cache._

## Supported Models
Support has been confirmed for these models, but many more will work. Please add already supported devices [with this form to complete the list](https://forms.gle/bTSD8qFotdZFytbf8).

|                     | **Haier**                                                                                                                                                                                                  | **Hoover**                                                                                                                                  | **Candy**                                                                                           |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| **Washing Machine** | HW80-B14959TU1DE <br/> HW90-B14TEAM5 <br/> HW100-B14959U1                                                                                                                                                  | H-WASH 500 <br/> H7W4 48MBC-S <br/> HW 410AMBCB/1-80                                                                                        | CO4 107T1/2-07 <br/> CBWO49TWME-S <br/> RO44 1286DWMC4-07 <br/> HW 68AMC/1-80 <br/> HWPD 69AMBC/1-S |
| **Tumble Dryer**    | HD80-A3959                                                                                                                                                                                                 | H-DRY 500 <br/> H9A3TCBEXS-S <br/> HLE C10DCE-80 <br/> H5WPB447AMBC/1-S <br/> NDE H10A2TCE-80 <br/> NDE H9A2TSBEXS-S <br/> NDPHY10A2TCBEXSS | BCTDH7A1TE <br/> CSOE C10DE-80 <br/> ROE H9A3TCEX-S                                                 |
| **Washer Dryer**    | HWD100-B14979                                                                                                                                                                                              | HDQ 496AMBS/1-S <br/> HWPS4954DAMR-11                                                                                                       | RPW41066BWMR/1-S                                                                                    |
| **Oven**            | HWO60SM2F3XH                                                                                                                                                                                               | HSOT3161WG                                                                                                                                  |                                                                                                     |
| **Dish Washer**     | XIB 3B2SFS-80 <br/> XIB 6B2D3FB                                                                                                                                                                            | HFB 6B2S3FX                                                                                                                                 |                                                                                                     |
| **Air Conditioner** | AD105S2SM3FA <br/> AS09TS4HRA-M <br/> AS20HPL1HRA <br/> AS25PBAHRA <br/> AS25S2SF1FA-WH <br/> AS25TADHRA-2 <br/> AS35PBAHRA <br/> AS35S2SF1FA-WH <br/> AS35S2SF2FA-3 <br/> AS35TADHRA-2 <br/> AS35TAMHRA-C |                                                                                                                                             | CY-12TAIN                                                                                           |
| **Fridge**          | HFW7720ENMB                                                                                                                                                                                                |                                                                                                                                             | CCE4T620EWU                                                                                         |
| **Hob**             | HA2MTSJ68MC                                                                                                                                                                                                |                                                                                                                                             | CIS633SCTTWIFI                                                                                      |
| **Hood**            | HADG6DS46BWIFI                                                                                                                                                                                             |                                                                                                                                             |                                                                                                     |
| **Wine Cellar**     | HWS247FDU1                                                                                                                                                                                                 |                                                                                                                                             |                                                                                                     |
| **Air Purifier**    |                                                                                                                                                                                                            | HHP50CA001                                                                                                                                  |                                                                                                     |

| Please add your appliances data to our [hon-test-data collection](https://github.com/Andre0512/hon-test-data). <br/>This helps us to develop new features and not to break compatibility in newer versions. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

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

## Contribute


Want to help us to support more appliances? Or add more sensors? Or help with translating? Or beautify some icons or captions? 
Check out the [project on GitHub](https://github.com/Andre0512/hon), every contribution is welcome!

## Useful Links
* [GitHub repository](https://github.com/Andre0512/hon) (please add a star if you like this integration!)
* [pyhOn library](https://github.com/Andre0512/pyhOn)
* [Release notes](https://github.com/Andre0512/hon/releases)
* [Discussion and help](https://github.com/Andre0512/hon/discussions)
* [Issues](https://github.com/Andre0512/hon/issues)
