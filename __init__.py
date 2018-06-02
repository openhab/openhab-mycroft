# Copyright (c) 2010-2017 by the respective copyright holders.
# -*- coding: iso-8859-15 -*-

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html

from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from fuzzywuzzy import fuzz

import requests
import json

__author__ = 'mortommy'

LOGGER = getLogger(__name__)

class openHABSkill(MycroftSkill):
    def __init__(self):
        super(openHABSkill, self).__init__(name="openHABSkill")

        self.url = "http://%s:%s/rest" % (self.config.get('host'), self.config.get('port'))

        self.command_headers = {"Content-type": "text/plain"}
        self.polling_headers = {"Accept": "application/json"}

        self._clearItems()
        self._getTaggedItems()

    def initialize(self):

        supported_languages = ["en-us"]

        if self.lang not in supported_languages:
            self.log.warning("Unsupported language for " + self.name + ", shutting down skill.")
            self.shutdown()

        intent = IntentBuilder("RefreshTaggedItemsIntent").require("RefreshTaggedItemsKeyword").build()
        self.register_intent(intent, self.intent_refresh_items)

        intent = IntentBuilder("OnOff_StatusIntent").require("OnOffStatusKeyword").require("Command").require("Item").build()
        self.register_intent(intent, self.intent_onoff)

        intent = IntentBuilder("Dimmer_StatusIntent").require("DimmerStatusKeyword").require("Item").require("DimmerPercentage").build()
        self.register_intent(intent, self.intent_dimmer)

        intent = IntentBuilder("What_StatusIntent").require("WhatStatusKeyword").require("Item").require("RequestType").build()
        self.register_intent(intent, self.handle_what_status_intent)

        intent = IntentBuilder("SetTemp_StatusIntent").require("ThermostatStatusKeyword").require("Item").require("TempValue").build()
        self.register_intent(intent, self.handle_setTemp_status_intent)

        intent = IntentBuilder("ListItemsIntent").require("ListItemsKeyword").build()
        self.register_intent(intent, self.intent_list_items)

    def intent_list_items(self, message):
        self.speak_dialog("ListItems", {
            "type": "Lighting",
            "items": self._getItemsFromDict(self.items["Lighting"])
        })

        self.speak_dialog("ListItems", {
            "type": "Switchable",
            "items": self._getItemsFromDict(self.items["Switchable"])
        })

        self.speak_dialog("ListItems", {
            "type": "CurrentTemperature",
            "items": self._getItemsFromDict(self.items["CurrentTemperature"])
        })

        self.speak_dialog("ListItems", {
            "type": "CurrentHumidity",
            "items": self._getItemsFromDict(self.items["CurrentHumidity"])
        })

        self.speak_dialog("ListItems", {
            "type": "Thermostat",
            "items": self._getItemsFromDict(self.items["Thermostat"])
        })

    def intent_refresh_items(self, message):
        self._getTaggedItems()

        self.speak_dialog('RefreshItems', {
            'light_count': str(len(self.items["Lighting"])),
            'switch_count': str(len(self.items["Switchable"])),
            'temp_count': str(len(self.items["CurrentTemperature"])),
            'hum_count': str(len(self.items["CurrentHumidity"])),
            'therm_count': str(len(self.items["Thermostat"]))
        })

    def intent_onoff(self, message):
        command = message.data.get('Command')
        messageItem = message.data.get('Item')

        # On/off needs switchable or lighting items only
        items = dict()
        items.update(self.items["Lighting"])
        items.update(self.items["Switchable"])

        item = self._findItemName(items, messageItem)

        if item != None:
            if (command != "on") and (command != "off"):
                self.speak_dialog('ErrorDialog')
            else:
                statusCode = self._sendCommandToItem(item, command.upper())

                if statusCode == 200:
                    self.speak_dialog('SetItem')
                elif statusCode == 400:
                    self.speak_dialog('ItemCommandNullError')
                elif statusCode == 404:
                    self.speak_dialog('ItemNotFoundError')
                else:
                    self.speak_dialog('CommunicationError')
        else:
            self.speak_dialog('ItemNotFoundError')

    def intent_dimmer(self, message):
        command = message.data.get('DimmerStatusKeyword')
        messageItem = message.data.get('Item')
        value = message.data.get('DimmerPercentage', None)

        # Dimmer needs lighting items only
        items = dict()
        items.update(self.items["Lighting"])

        item = self._findItemName(items, messageItem)

        if item != None:
            if (value == None):
                LOGGER.debug("Didn't pick up the value")
            elif ((int(value) < 0) or (int(value) > 100)):
                self.speak_dialog('ErrorDialog')
            else:
                statusCode = self._sendCommandToItem(item, value)

                if statusCode == 200:
                    self.speak_dialog('SetItem')
                elif statusCode == 400:
                    self.speak_dialog('ItemCommandNullError')
                elif statusCode == 404:
                    self.speak_dialog('ItemNotFoundError')
                else:
                    self.speak_dialog('CommunicationError')
        else:
            self.speak_dialog('ItemNotFoundError')

    def handle_what_status_intent(self, message):
        messageItem = message.data.get('Item')
        requestType = message.data.get('RequestType')

        # Status needs switchable, lighting, and thermostat items only
        # items = dict()
        # items.update(self.items["Lighting"])
        # items.update(self.items["Switchable"])
        # items.update(self.items["CurrentTemperature"])
        # items.update(self.items["CurrentHumidity"])

        # item = self._findItemName(items, messageItem)

        # state = self.getCurrentItemStatus(item)

        if (requestType == "status"):
            items = dict()
            items.update(self.items["Lighting"])
            items.update(self.items["Switchable"])

            item = self._findItemName(items, messageItem)
            state = self.getCurrentItemStatus(item)

            self.speak_dialog('StatusOnOff', {'item': messageItem, 'state': state})
        elif (requestType == "set to"):
            items = dict()
            items.update(self.items["Lighting"])

            item = self._findItemName(items, messageItem)
            state = self.getCurrentItemStatus(item)

            self.speak_dialog('StatusDimmer', {'item': messageItem, 'state': state})
        elif (requestType == "temp"):
            items = dict()
            items.update(self.items["CurrentTemperature"])

            item = self._findItemName(items, messageItem)
            state = self.getCurrentItemStatus(item)

            self.speak_dialog('StatusTemperature', {'item': messageItem, 'state': state})
        elif (requestType == "humidity"):
            items = dict()
            items.update(self.items["CurrentHumidity"])

            item = self._findItemName(items, messageItem)
            state = self.getCurrentItemStatus(item)

            self.speak_dialog('StatusHumidity', {'item': messageItem, 'state': state})

    def handle_setTemp_status_intent(self, message):
        command = message.data.get('ThermostatStatusKeyword')
        messageItem = message.data.get('Item')
        tempVal = message.data.get('TempValue')

        statusCode = 0
        newTempValue = 0

        ohItem = self._findItemName(self.targetTemperatureItemsDic, messageItem)

        if ohItem != None:
            if((command == "regulate") or (command == "adjust") or (command == "tune") or (command == "regola") or (command == "aggiusta") or (command == "metti")):
                statusCode = self._sendCommandToItem(ohItem, tempVal)
                newTempValue = tempVal
            else:
                state = self.getCurrentItemStatus(ohItem)
                if ((state != None) and (state.isdigit())):
                    if ((command == "increase") or (command == "incrementa")):
                        newTempValue = int(state)+(int(tempVal))
                    else:
                        newTempValue = int(state)-(int(tempVal))

                    statusCode = self._sendCommandToItem(
                        ohItem, str(newTempValue))
                else:
                    pass

            if statusCode == 200:
                self.speak_dialog('ThermostatStatus', {
                                  'item': messageItem, 'temp_val': str(newTempValue)})
            elif statusCode == 404:
                LOGGER.error(
                    "Some issues with the command execution!. Item not found")
                self.speak_dialog('ItemNotFoundError')
            else:
                LOGGER.error("Some issues with the command execution!")
                self.speak_dialog('CommunicationError')

        else:
            LOGGER.error("Item not found!")
            self.speak_dialog('ItemNotFoundError')

    def getCurrentItemStatus(self, ohItem):
        requestUrl = self.url+"/items/%s/state" % (ohItem)
        state = None

        try:
            req = requests.get(requestUrl, headers=self.command_headers)

            if req.status_code == 200:
                state = req.text
            else:
                LOGGER.error("Some issues with the command execution!")
                self.speak_dialog('CommunicationError')

        except KeyError:
            pass

        return state

    def stop(self):
        pass
	
    def _clearItems(self):
        self.items = {
            "Lighting": {},
            "Switchable": {},
            "CurrentTemperature": {},
            "CurrentHumidity": {},
            "Thermostat": {}
        }
    
    def _getTaggedItems(self):
        self._clearItems()

        requestUrl = self.url+"/items?recursive=false"

        req = requests.get(requestUrl, headers=self.polling_headers)

        if req.status_code == 200:
            json_response = req.json()

            for x in range(0, len(json_response)):
                if ("Lighting" in json_response[x]['tags']):
                    self.items["Lighting"].update(
                        {json_response[x]['name']: json_response[x]['label']})
                elif ("Switchable" in json_response[x]['tags']):
                    self.items["Switchable"].update(
                        {json_response[x]['name']: json_response[x]['label']})
                elif ("CurrentTemperature" in json_response[x]['tags']):
                    self.items["CurrentTemperature"].update(
                        {json_response[x]['name']: json_response[x]['label']})
                elif ("CurrentHumidity" in json_response[x]['tags']):
                    self.items["CurrentHumidity"].update(
                        {json_response[x]['name']: json_response[x]['label']})
                elif ("Thermostat" in json_response[x]['tags']):
                    self.items["Thermostat"].update(
                        {json_response[x]['name']: json_response[x]['label']})
                else:
                    pass
        else:
            self.speak_dialog('GetItemsListError')

    def _findItemName(self, itemDictionary, messageItem):

        bestScore = 0
        score = 0
        bestItem = None

        try:
            for itemName, itemLabel in list(itemDictionary.items()):
                score = fuzz.ratio(messageItem, itemLabel)
                if score > bestScore:
                    bestScore = score
                    bestItem = itemName
        except KeyError:
            pass

        return bestItem

    def _getItemsFromDict(self, itemsDict):
        if len(itemsDict) == 0:
            return "nothing"
        else:
            return "%s" % (', '.join(list(itemsDict.values())))

    def _sendCommandToItem(self, ohItem, command):
        requestUrl = self.url+"/items/%s" % (ohItem)
        req = requests.post(requestUrl, data=command, headers=self.command_headers)

        return req.status_code

def create_skill():
    return openHABSkill()
