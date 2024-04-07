from enum import Enum
import time
import streamlit as st
from bot_message import BotMessage, BotResponseType
import constants
from utility import encodeMessage

# Define enumerations for application states and gender options
ProgramState = Enum("ProgramState", ['WELCOME', 'PATIENT_WHO', 'GENDER', 'NAME', 'AGE', 'SYMPTOM', 'DISEASE', 'BYE'])
Gender = Enum("Gender", ['MALE', 'FEMALE'])

class DataController:
    # Initialize class variables from the Streamlit session state or set default values
    __messages = st.session_state.get(constants.MESSAGE_KEY, [])
    __program_state = st.session_state.get(constants.PROGRAM_STATE_KEY, ProgramState.WELCOME)
    __bot_message_shown = st.session_state.get(constants.BOT_MESSAGE_SHOWN_KEY, False)

    # Patient information initialized from session state or default values
    __patient_name: str = st.session_state.get(constants.PATIENT_NAME_KEY, '')
    __patient_gender: Gender = st.session_state.get(constants.PATIENT_GENDER_KEY, Gender.MALE)
    __patient_age: int = st.session_state.get(constants.PATIENT_AGE_KEY, 0)
    __patient_symptoms: list = st.session_state.get(constants.PATIENT_SYMPTOMS_KEY, [])
    __patient_disease: str = st.session_state.get(constants.PATIENT_DISEASE_KEY, '')

    @staticmethod
    def bot_replied_status() -> bool:
        # Return True if the bot has already replied in the current context
        return DataController.__bot_message_shown

    @staticmethod
    def set_bot_replied_status(value: bool):
        # Update the bot reply status in both the class variable and session state
        DataController.__bot_message_shown = value
        st.session_state[constants.BOT_MESSAGE_SHOWN_KEY] = value

    # Getter methods for patient information
    @staticmethod
    def get_patient_name() -> str:
        return DataController.__patient_name

    @staticmethod
    def get_patient_age() -> int:
        return DataController.__patient_age

    @staticmethod
    def get_patient_disease() -> str:
        return DataController.__patient_disease

    @staticmethod
    def get_patient_symptoms() -> list:
        return DataController.__patient_symptoms

    @staticmethod
    def get_patient_gender() -> Gender:
        return DataController.__patient_gender

    # Setter methods to update patient information in the class and session state
    @staticmethod
    def set_patient_name(value):
        DataController.__patient_name = value
        st.session_state[constants.PATIENT_NAME_KEY] = value

    @staticmethod
    def set_patient_gender(value):
        DataController.__patient_gender = value
        st.session_state[constants.PATIENT_GENDER_KEY] = value

    @staticmethod
    def set_patient_age(value):
        DataController.__patient_age = value
        st.session_state[constants.PATIENT_AGE_KEY] = value

    @staticmethod
    def set_patient_disease(value):
        DataController.__patient_disease = value
        st.session_state[constants.PATIENT_DISEASE_KEY] = value

    # Methods to manage patient symptoms: adding and removing, and updating session state accordingly
    @staticmethod
    def add_patient_symptom(value) -> bool:
        # Avoid adding duplicate symptoms
        if value in DataController.__patient_symptoms:
            return False
        DataController.__patient_symptoms.append(value)
        st.session_state[constants.PATIENT_SYMPTOMS_KEY] = DataController.__patient_symptoms
        return True

    @staticmethod
    def remove_patient_symptom(value) -> bool:
        # Remove symptom if it exists
        if value not in DataController.__patient_symptoms:
            return False
        DataController.__patient_symptoms.remove(value)
        st.session_state[constants.PATIENT_SYMPTOMS_KEY] = DataController.__patient_symptoms
        return True

    # Methods for clearing data: reset patient data and/or all messages
    @staticmethod
    def clear_data():
        DataController.clear_patient_data()
        DataController.set_bot_replied_status(False)

    @staticmethod
    def clear_patient_data():
        # Reset patient info in both the class and session state
        st.session_state[constants.PATIENT_NAME_KEY] = ""
        st.session_state[constants.PATIENT_AGE_KEY] = 0
        st.session_state[constants.PATIENT_GENDER_KEY] = Gender.MALE
        st.session_state[constants.PATIENT_DISEASE_KEY] = ""
        st.session_state[constants.PATIENT_SYMPTOMS_KEY] = []
        DataController.__patient_name = ""
        DataController.__patient_age = 0
        DataController.__patient_gender = Gender.MALE
        DataController.__patient_disease = ""
        DataController.__patient_symptoms = []

    # Method to change the application's current state
    @staticmethod
    def change_state(state: ProgramState):
        DataController.__program_state = state
        st.session_state[constants.PROGRAM_STATE_KEY] = state

    # Getter for the application's current state
    @staticmethod
    def get_program_state() -> ProgramState:
        return DataController.__program_state

    # Methods to manage messages in the conversation, including adding new messages and clearing all messages
    @staticmethod
    def add_messages(message, rerun=False):
        DataController.__messages.append(message)
        st.session_state[constants.MESSAGE_KEY] = DataController.__messages
        if rerun:
            time.sleep(0.1)
            st.rerun()

    @staticmethod
    def get_messages():
        return DataController.__messages

    @staticmethod
    def clear_messages():
        st.session_state[constants.MESSAGE_KEY] = []

    # Method to ensure the welcome message is added at the start of a new session or conversation
    @staticmethod
    def welcome_message():
        if len(DataController.__messages) == 0:
            welcome = BotMessage.get_message(BotResponseType.WELCOME)
            DataController.add_messages(encodeMessage(msg=welcome, isBot=True))
