# Haier hOn
Home Assistant component supporting hOn cloud.

## Installation
#### Installing via HACS
1. You need to have installed [HACS](https://hacs.xyz/)
2. Go to HACS->Integrations
3. Add this repo (`https://github.com/Andre0512/haier.git`) into your HACS custom repositories
4. Search for Haier hOn and Download it
5. Restart your HomeAssistant
6. Go to Settings->Devices & Services
7. Shift reload your browser
8. Click Add Integration
9. Search for Haier hOn 
10. Type your username used in the hOn App and hit submit

## Supported Appliances
- Washing Machine

## Tested Devices
- Haier WD90

## About this Repo
The existing integrations missed some features from the app I liked to have in HomeAssistant.
I tried to create a pull request, but in the structures of these existing repos, I find it hard to fit in my needs, so I basically rewrote everything. 
I moved the api related stuff into the package [pyhOn](https://github.com/Andre0512/pyhOn).

