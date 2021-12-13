# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!!!")

        return []

class ActionInfoExamOption(Action):

    def name(self) -> Text:
        return "action_info_appointment_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        option2action = {
            1: "action_view_prepare",
            2: "action_confirm_procedure",
            3: "action_reschedule",
            4: "action_cancel_appointment",
            0: "action_back_to_main"

        }
        
        try:
            user_choice = int(tracker.get_slot("appointment_info_menu_option"))         
        except ValueError:
            dispatcher.utter_message(text=f"Por favor entre com um número")
            return [SlotSet('appointment_info_menu_option', None)]

        dispatcher.utter_message(text=f"Você escolheu a opção {user_choice}!")

        try:
            next_action = option2action[user_choice]
        except KeyError:
            dispatcher.utter_message(text=f"Essa opção não está disponível")
            return [SlotSet('appointment_info_menu_option', None)]


        return [SlotSet('appointment_info_menu_option', None), FollowupAction(name=next_action)]

class ActionViewPrepare(Action):

    def name(self) -> Text:
        return "action_view_prepare"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = "Você escolheu a opção de visualizar preparo. "
        dispatcher.utter_message(text=message)

        return []

class actionConfirmProcedure(Action):

    def name(self) -> Text:
        return "action_confirm_procedure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = "Você escolheu a opção de confirmar o Procedimento"
        dispatcher.utter_message(text=message)

        return []

class ActionUnitsInfo(Action):

    def name(self) -> Text:
        return "action_units_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_choice = tracker.get_slot("unit_choice")

        if user_choice == "mato grosso":
           info_msg = "Essa unidade fica aberta de segunda a sexta das 07h as 18hs. Temos as especialidades: Ortopedia, Geriatria, Pediatria e Otorrino. Estamos localizados na av. Matro Grosso, 1444 - bairro Carandá"
        elif user_choice == "afonso pena":
           info_msg = "Essa unidade fica aberta de segunda a sexta das 08h as 17hs. Temos as especialidades: Endocrinologia, Psiquiatria e Pneumologia. Estamos localizados na av. Afonso Pena, 2222 - bairro Amambaí"
        elif user_choice == "centro":
            info_msg = "Essa unidade fica aberta de segunda a sexta das 08h as 22hs. Temos as especialidades: Clínico Geral, Neurologia, Pediatria e Obstetra. Estamos localizados na rua 13 de maio, 5155 - bairro Centro"
        else:
            info_msg = "Não temos informaçòes sobre a unidade informada"
        
        dispatcher.utter_message(text=info_msg)
        return []

class ActionGetPacientInformation(Action):

    def name(self) -> Text:
        return "action_get_pacient_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        text = tracker.slots['cpf']

        if text == "73725072191":
            name = "Nathalia"
        else:
            name = "Outro Paciente"
        return [SlotSet("user_name", name)]
