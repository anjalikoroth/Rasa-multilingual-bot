# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import os

class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "Language %s belongs to the Family %s\n with Genus as %s\n and has ISO code %s" % (out_row["Name"], out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Sorry! We don't have records for the language %s" % query_lang)

        return []


Tasks to do
Procedure for each task (What we are trying to do)
    We are answering questions based on the wals dataset. 
    That is done by first identifying the intent and then the associated entity in a particular query.
    So for each task the required dataset has to be downloaded and then queries for 
    different entities(basically languages) should be written in hindi, for the specified intent(is specified down below)

Task 1 (need at least 15 questions)
    Questions based on family, genus and macroarea of a particular language need to be answered
    dataset - languages.csv (already downloaded, can be found in data->cldf folder)
    Sample Question - मुझे स्पेनिश के परिवार के बारे में बताएं (Tell me about the family of spanish)
    English translation also given for the slow ones

Task 2 (need at least 15 questions)
    Questions based on features(the number and the list of features) of a particular language need to be answered
    dataset - languages.csv (already downloaded, can be found in data->cldf folder)
    Sample Question - मुझे स्पेनिश के परिवार के बारे में बताएं (Tell me about the family of spanish)
    English translation also given for the slow ones
