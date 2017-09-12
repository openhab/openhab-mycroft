# openHAB skill for Mycroft

[Mycroft](https://mycroft.ai/) is the world’s first open source assistant. The skill allows you to connect a running Mycroft 
instance (Mark 1, picroft, etc.) to your openHab. The skill takes advantage of the openHAB REST API, so it works both with the 
v1.x and v2.x, and no openHab upgrade is required. 

The skill is supported for English (U.S.), English (U.K.) languages. 

## General Configuration Instructions

### Requirements

* [A running instance of Mycroft](https://mycroft.ai/get-mycroft/)
* A running instance of openHAB
* openHAB must be reacheable from the Mycroft instance 

### Skill Installation

The openHAB skill has to be installed on you Mycroft instance, please refer to the [official documentation](https://docs.mycroft.ai/skills.and.features/adding.skills) 
about how to install a skill. 

Clone the [repository](https://github.com/openhab/openhab-mycroft.git) into your `~/.mycroft/skills` directory.
Then install the dependencies inside your mycroft virtual environment:

If on picroft just skip the workon part and the directory will be `/opt/mycroft/skills`

```shell
cd ~/.mycroft/skills
git clone https://github.com/mortommy/mycroft-skill-openhab skill-openhab
workon mycroft
cd skill-openhab
pip install -r requirements.txt
```

### Skill Configuration

Add the block below to your `mycoft.conf` file:

```json
 "openHABSkill": {
        "host": "openHAB server ip",
        "port": "openHAB server port"
      }
```

Restart mycroft for the changes to take effect.

### openHAB Item Configuration

Items are exposed to openHAB skill for Mycroft through the use of tags which follow the [HomeKit](http://docs.openhab.org/addons/io/homekit/readme.html) binding tagging syntax.
Pleas see the [HomeKit item configuration](http://docs.openhab.org/addons/io/homekit/readme.html#item-configuration) page for information on how to tag items.

* **Items via .items - File**

  See [Item Definition and Syntax](http://docs.openhab.org/configuration/items.html#item-definition-and-syntax)
     
  Some examples of tagged items are:
  
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
  
### Example Voice Commands

Each item tag supports different command, here is the summary:


 | Tag					| Key word   	|  Commands				|
 |----------------------|---------------|-----------------------|
 | Switchable			| turn		 	| 	on, off				|
 |						| switch	 	|	on, off				|
 |						| put		 	|	on, off				|
 |						|				|						|
 | Lighting				| turn		 	| 	on, off				|
 |						| switch	 	|	on, off				|
 |						| put		 	|	on, off				|
 |						| dim		 	|						|
 |						| dim by	 	|	value in percentage	|
 |						| brighten 		|						|
 |						| brighten by	|	value in percentage	|
 |						|				|						|
 | Thermostat			| adjust to		|	values in degrees	|
 |						| regulate to	|	values in degrees	|
 |						| tune to		|	values in degrees	|
 |						| decrease by	|	values in degrees	|
 |						| increase by	|	values in degrees	|
 |						| what's		|	adjusted to			|
 |						| what's		|	regulated to		|
 |						| what's		|	tuned to			|
 |						|				|						|
 | CurrentHumidity		| what's		|	humidity			|
 |						|				|						|
 | CurrentTemperature	| what's		|	temperature			|

With references to the above item definitions, here are an examples of working commands:

- *"Hey Mycroft, turn on Diningroom Light"*
- *"Hey Mycroft, switch off Kitchen Light"*
- *"Hey Mycroft, put on Good Night"*
- *"Hey Mycroft, set Diningroom to 50 percent"*
- *"Hey Mycroft, dim Kitchen"*
- *"Hey Mycroft, brighten Kitchen"*
- *"Hey Mycroft, dim Kitchen by 20 percent"*
- *"Hey Mycroft, what's Bedroom temperature?"*
- *"Hey Mycroft, what's Bedroom humidity?"*
- *"Hey Mycroft, adjust Main Thermostat to 21 degrees"*
- *"Hey Mycroft, regulate Main Thermostat to 20 degrees"*
- *"Hey Mycroft, decrease Main Thermostat by 2 degrees"*
- *"Hey Mycroft, increase Main Thermostat by 1 degrees"*
- *"Hey Mycroft, what is Main Thermostat regulated to?"*
- *"Hey Mycroft, what is Main Thermostat tuned to?"*

### Additional Comments

* By default all temperatures are in Celsius, no test so far about the tag Fahrenheit to the thermostat group item (which should also be tagged with `Thermostat`).