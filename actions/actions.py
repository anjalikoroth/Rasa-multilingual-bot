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
import time
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
            query_lang_hin = query_lang
            query_lang = translator.translate(query_lang, dest='en').text
            query_lang = query_lang.lower().capitalize()
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                name_hindi = translator.translate(out_row["Name"], dest='hi').text
                family_hindi = translator.translate(out_row["Family"], dest='hi').text
                genus_hindi = translator.translate(out_row["Genus"], dest='hi').text
                out_text = "भाषा का नाम, परिवार, उपपरिवार और आईएसओ कोड %s, %s और %s क्रमशः" % (name_hindi, family_hindi, genus_hindi)
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "माफ़ करना! हमारे पास भाषा %s के रिकॉर्ड नहीं हैं" % query_lang_hin)

        return []



class ActionFamilySearch(Action):    
    def name(self) -> Text:
        return "action_family_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        lang_entities = list(tracker.get_latest_entity_values("family"))

        if len(lang_entities) > 0:
            query_lang = query_lang_hi = lang_entities.pop()
            query_lang = translator.translate(query_lang, dest='en').text
            query_lang = '-'.join([i.lower().capitalize() for i in query_lang.split('-')])
            query_lang = query_lang.strip()

            out_row = wals_data[wals_data["Family"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                name_hindi = translator.translate(out_row["Name"], dest='hi').text
                family_hindi = translator.translate(out_row["Family"], dest='hi').text
                out_text = "भाषा का नाम और परिवार, %s और %s हैं" % (name_hindi, family_hindi)
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "माफ़ करना! हमारे पास भाषा %s के रिकॉर्ड नहीं हैं" % query_lang_hi)

        return []



class ActionMacroAreaSearch(Action):    
    def name(self) -> Text:
        return "action_macro_area_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # change the data path according to where you are fetching the data from 
        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "Languages_New.csv") 
        wals_data = pd.read_csv(data_path)
        lang_entities = list(tracker.get_latest_entity_values("macroarea")) # assuming that the entity name is country

        if len(lang_entities) > 0:
            macro_name = macro_name_hi = lang_entities.pop()
            macro_name = translator.translate(macro_name, dest='en').text
            macro_name = ' '.join([i.strip().lower().capitalize() for i in macro_name.split(' ')])
            
            out_row = wals_data[wals_data["macroarea"] == macro_name]

            if len(out_row) > 0:
                out_row = out_row['name'].values[0]
                language_name = translator.translate(out_row, dest='hi').text
                
                out_text = "%s उपमहाद्वीप में एक भाषा %s है" % (macro_name_hi, language_name)
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "माफ़ करना! हमारे पास भाषा %s के रिकॉर्ड नहीं हैं" % macro_name_hi)

        return []


class ActionFeedback(Action):
    def name(self) -> Text:
        return "feedback_loop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text = "क्या इससे आपको मदद मिली?")
        return []

class UtterGreetings(Action):
    def name(self) -> Text:
        return "action_greetings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        curr_time = time.localtime().tm_hour
        if curr_time < 12: 
            dispatcher.utter_message(text = "शुभ प्रभात!")
        elif curr_time >= 12 and curr_time < 17:
            dispatcher.utter_message(text = "नमस्कार!")
        elif curr_time >= 17 and curr_time < 20:
            dispatcher.utter_message(text = "गुड इवनिंग!")
        else:
            dispatcher.utter_message(text = "शुभ रात्रि!")
        return []


class UtterPartings(Action):
    def name(self) -> Text:
        return "action_partings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        curr_time = time.localtime().tm_hour
        if curr_time > 21: 
            dispatcher.utter_message(text = "शुभ रात्रि!")
        else:
            dispatcher.utter_message(text = "फिर मिलेंगे!")
        return []