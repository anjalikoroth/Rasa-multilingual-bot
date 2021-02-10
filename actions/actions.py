# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from googletrans import Translator
import pandas as pd
import os

translator = Translator(service_urls=['translate.googleapis.com'])

class ActionLanguageSearch(Action):    
    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        lang_entities = list(tracker.get_latest_entity_values("language"))

        if len(lang_entities) > 0:
            query_lang = lang_entities.pop()
            query_lang = translator.translate(query_lang, dest='en').text
            query_lang = query_lang.lower().capitalize()
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                name_hindi = translator.translate(out_row["Name"], dest='hi').text
                family_hindi = translator.translate(out_row["Family"], dest='hi').text
                genus_hindi = translator.translate(out_row["Genus"], dest='hi').text
                out_text = "भाषा का नाम, परिवार, उपपरिवार और आईएसओ कोड %s, %s, %s और %s क्रमशः" % (name_hindi, family_hindi, genus_hindi, out_row["ISO_codes"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "माफ़ करना! हमारे पास भाषा %s के रिकॉर्ड नहीं हैं" % query_lang)

        return []



class ActionFamilySearch(Action):    
    def name(self) -> Text:
        return "action_family_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        lang_entities = list(tracker.get_latest_entity_values("language"))

        if len(lang_entities) > 0:
            query_lang = lang_entities.pop()
            query_lang = translator.translate(query_lang, dest='en').text
            query_lang = query_lang.lower().capitalize()
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                name_hindi = translator.translate(out_row["Name"], dest='hi').text
                family_hindi = translator.translate(out_row["Family"], dest='hi').text
                out_text = "भाषा का नाम और परिवार, %s %s हैं" % (name_hindi, family_hindi)
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "माफ़ करना! हमारे पास भाषा %s के रिकॉर्ड नहीं हैं" % query_lang)

        return []