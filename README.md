# <img src='https://www.openhab.org/openhab-logo-square.png' card_color='#40DBB0' width='50' height='50' style='vertical-align:bottom'/> openHAB
This skill adds openHAB support to Mycroft.

## About 
This skill adds [openHAB](http://www.openhab.org/) support to [Mycroft](https://mycroft.ai).
The skill takes advantage of the openHAB REST API, so it works both with the v1.x and v2.x of openHAB.

In order to make openHAB Items accessible to Mycroft, they need to be [tagged](https://www.openhab.org/addons/integrations/homekit/).
Device names recognized by Mycroft are matched against openHAB Item Labels.

The above examples would all work with the following set of openHAB Item definitons:

```java
Color DiningroomLight "Diningroom Light" <light> (gKitchen) [ "Lighting" ] {channel="hue:0200:1:bloom1:color"}
Color KitchenLight "Kitchen Light" <light> (gKitchen) [ "Lighting" ] {channel="hue:0200:1:bloom1:color"}
Switch GoodNight "Good Night"	[ "Switchable" ]

Number MqttID1Temperature "Bedroom Temperature" <temperature> [ "CurrentTemperature" ] {mqtt="<[mosquitto:mysensors/SI/1/1/1/0/0:state:default]"}
Number MqttID1Humidity "Bedroom Humidity" [ "CurrentHumidity" ] {mqtt="<[mosquitto:mysensors/SI/1/0/1/0/1:state:default]"}

Group gThermostat "Main Thermostat" [ "gMainThermostat" ]
Number MainThermostatCurrentTemp "Main Thermostat Current Temperature" (gMainThermostat) [ "CurrentTemperature" ]
Number MainThermostatTargetTemperature "Main Thermostat Target Temperature" (gMainThermostat) [ "TargetTemperature" ]
String MainThermostatHeatingCoolingMode "Main Thermostat Heating/Cooling Mode" (gMainThermostat) [ "homekit:HeatingCoolingMode" ]
```

If items are modified in openHAB, a refresh in Mycroft is needed by the command:

- *"Hey Mycroft, refresh openhab items"*

If you've forgotten what items have been identified, you can ask Mycroft:
- *"Hey Mycroft, list openhab items"*

## Versions Change Log
* 1.4 added spanish translation
* 1.3 added german translation
* 1.2 addedd python 3 support
* 1.1 added status request to Switchable items
* 1.0 added support to item tagged as Thermostat, CurrentTemperature, CurrentHumidity
* 0.9 added dimming command to item tagged as Lighting
* 0.8 supports only Lighting and Switchable tags, commands ON and OFF

## Installation

From 18.2.5b mycroft-core release it is possible to install the skill using the voice command:
- *"Hey Mycroft, install openhab"*

or via the [msm](https://mycroft.ai/documentation/msm/) command:
```shell
msm install openhab
```

To manually install the skill:
Clone this repository into your `~/.mycroft/skills` directory.
Then install the dependencies inside your mycroft virtual environment:

If on picroft just skip the workon part and the directory will be `/opt/mycroft/skills`

```shell
cd ~/.mycroft/skills
git clone https://github.com/openhab/openhab-mycroft.git skill-openhab
workon mycroft
cd skill-openhab
pip install -r requirements.txt
```

## Examples 
* " Hey Mycroft, turn on Diningroom Light"
* "Hey Mycroft, switch off Kitchen Light"
* "Hey Mycroft, put on Good Night"
* "Hey Mycroft, what is Good Night status?"
* "Hey Mycroft, set Diningroom to 50 percent"
* "Hey Mycroft, dim Kitchen"
* "Hey Mycroft, brighten Kitchen"
* "Hey Mycroft, dim Kitchen by 20 percent"
* "Hey Mycroft, what's Bedroom temperature?"
* "Hey Mycroft, what's Bedroom humidity?"
* "Hey Mycroft, adjust Main Thermostat to 21 degrees"
* "Hey Mycroft, regulate Main Thermostat to 20 degrees"
* "Hey Mycroft, decrease Main Thermostat by 2 degrees"
* "Hey Mycroft, increase Main Thermostat by 1 degrees"
* "Hey Mycroft, what is Main Thermostat regulated to?"
* "Hey Mycroft, what is Main Thermostat tuned to?"

## Credits 
@mortommy

## Category
**IoT**

## Tags
#openHAB
#smarthome
#IoT
#Automation
#opensource
