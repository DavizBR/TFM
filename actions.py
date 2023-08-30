# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import datetime
from matplotlib import image
import pytz
import re
import sqlite3
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

class ActionCheckMuseumOpeningHours(Action):
    def name(self) -> Text:
        return "action_abierto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tz = pytz.timezone('Europe/Madrid')
        current_time = datetime.datetime.now(tz)
        opening_time = datetime.time(10, 0)
        closing_time = datetime.time(20, 0)

        if current_time.time() >= opening_time and current_time.time() <= closing_time:
            message = "El museo está abierto ahora."
        else:
            message = "El museo está cerrado ahora."

        dispatcher.utter_message(text=message)

        return []
    

class ActionInformacionCuadro(Action):
    def name(self) -> Text:
        return "action_informacion_cuadro"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cuadro_goya = next(tracker.get_latest_entity_values("cuadro_goya"), None)

        if cuadro_goya and isinstance(cuadro_goya, str):
            cuadros_info = [
                {
                    "nombre": ["la maja vestida", "maja"],
                    "descripcion": "Este lienzo, posiblemente creado después de La Maja Desnuda, presenta a la maja recostada en un sofá verde, vestida con transparencias y detalles como un fajín rosa y chaquetilla amarilla. El cuadro muestra su destreza artística en las texturas y colores, permitiéndose una mayor libertad pictórica en comparación con su obra anterior. Los detalles del vestuario, el encarnado del rostro y el cabello negro son capturados con destreza. Su conexión con las majas como gitanas se menciona en inventarios de bienes.",
                    "enlace": "https://fundaciongoyaenaragon.es/obra/la-maja-vestida/581",
                    "imagen": "https://fundaciongoyaenaragon.es/files/resize/800x600/files/images/581_7.9.14.jpg"
                },
                {
                    "nombre": ["los fusilamientos del tres de mayo", "fusilamientos", "tres de mayo"],
                    "descripcion": "Los Fusilamientos representan la brutalidad de la represión durante la guerra de la Independencia española. La pintura muestra condenados esperando su ejecución, rodeados de víctimas previas y soldados implacables. Las expresiones de miedo, rabia y desesperación en los condenados revelan la crueldad y la irracionalidad de la violencia en un momento oscuro de la historia.",
                    "enlace": "https://fundaciongoyaenaragon.es/obra/el-tres-de-mayo-de-1808/181",
                    "imagen": "https://fundaciongoyaenaragon.es/files/resize/800x600/files/images/181_6.2.8.jpg"
                },
                {
                    "nombre": ["saturno devorando a sus hijos", "saturno"],
                    "descripcion": "Cuadro tétrico del titán Saturno devorando a su descendencia.",
                    "enlace": "https://fundaciongoyaenaragon.es/obra/saturno-devorando-a-un-hijo/660",
                    "imagen": "https://fundaciongoyaenaragon.es/files/resize/800x600/files/images/saturno79327.jpg"
                },
                {
                    "nombre": ["el quitasol", "quitasol"],
                    "descripcion": "Cuadro costumbrista en la que un majo protege de la luz solar a una maja.",
                    "enlace": "https://fundaciongoyaenaragon.es/obra/el-quitasol/17",
                    "imagen": "https://fundaciongoyaenaragon.es/files/resize/800x600/files/images/17_4.2.6.jpg"
                },
                {
                    "nombre": ["el coloso", "coloso"],
                    "descripcion": "Cuadro fantástico de un coloso amenazante en la lejanía.",
                    "enlace": "https://fundaciongoyaenaragon.es/obra/el-coloso/589",
                    "imagen": "https://fundaciongoyaenaragon.es/files/resize/800x600/files/images/589_7.3.39.jpg"
                },
            ]
            
            cuadro_info = next((cuadro for cuadro in cuadros_info if any(nombre.lower() == cuadro_goya.lower() for nombre in cuadro["nombre"])), None)

            if cuadro_info:
                nombre = cuadro_info["nombre"]
                descripcion = cuadro_info["descripcion"]
                enlace = cuadro_info["enlace"]

                respuesta = f"Autor: Francisco de Goya.\n\n{descripcion}\n\nÓleo sobre lienzo\n\n{image}"
                dispatcher.utter_message(text=respuesta)
            else:
                dispatcher.utter_message(text="Lo siento, no tengo información sobre ese cuadro de Goya.")
        else:
            dispatcher.utter_message(text="Por favor, indícame el nombre del cuadro sobre el que deseas obtener información.")

        return []
    

class ActionCalcularPrecio(Action):
    def name(self) -> Text:
        return "action_calcular_precio"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_user_message = tracker.latest_message.get("text")

        cantidad_pattern = r"\b(\d+)\b"
        cantidad_match = re.search(cantidad_pattern, last_user_message)

        if cantidad_match:
            cantidad_entradas = int(cantidad_match.group(1))
            precio_por_entrada = 8
            precio_total = cantidad_entradas * precio_por_entrada

            respuesta = f"El precio total por {cantidad_entradas} entradas es de {precio_total} euros."
            dispatcher.utter_message(text=respuesta)
        else:
            dispatcher.utter_message(text="Lo siento, no pude detectar la cantidad de entradas. Prueba a expresarlo con números.")

        return []

