from bot_message import *  # Import bot messaging utilities and response types
from data import DataController  # Access the DataController for managing app state and messages
from utility import encodeMessage  # Utility for encoding messages for display

class BotResponse:
    @staticmethod
    def welcome(rerun=False):
        """
        Sends a welcome message to the user.
        
        Args:
            rerun (bool): Indicates whether to trigger a Streamlit rerun after adding the message.
        """
        msg = BotMessage.get_message(BotResponseType.WELCOME)  # Fetch the welcome message
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)  # Add to messages with bot flag True

    @staticmethod
    def patient_who(rerun=False):
        """
        Asks the user if they are entering symptoms for themselves or someone else.
        """
        msg = BotMessage.get_message(BotResponseType.PATIENT_WHO)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def new_patient(rerun=False):
        """
        Sends a message to initiate the process for a new patient query.
        """
        msg = BotMessage.get_message(BotResponseType.NEW_PATIENT)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def ask_name(rerun=False):
        """
        Prompts the user to enter the patient's name.
        """
        msg = BotMessage.get_message(BotResponseType.NAME)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def ask_age(rerun=False):
        """
        Requests the patient's age from the user.
        """
        msg = BotMessage.get_message(BotResponseType.AGE)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def ask_gender(rerun=False):
        """
        Inquires about the gender of the patient.
        """
        msg = BotMessage.get_message(BotResponseType.GENDER)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def invalid_age(rerun=False):
        """
        Notifies the user that the entered age is invalid.
        """
        msg = BotMessage.get_message(BotResponseType.INVALID_AGE)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def ask_symptom(rerun=False):
        """
        Asks the user to enter symptoms experienced by the patient.
        """
        msg = BotMessage.get_message(BotResponseType.SYMPTOM)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def ask_more_symptoms(rerun=False):
        """
        Encourages the user to provide additional symptoms if available.
        """
        msg = BotMessage.get_message(BotResponseType.MORE_SYMPTOM)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def symptom_added(symptom, rerun=False):
        """
        Confirms that a symptom has been successfully added.
        """
        msg = BotMessage.get_message(BotResponseType.SYMPTOM_ADDED).format(symptom=symptom)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def symptom_exists(symptom, rerun=False):
        """
        Alerts the user that the symptom they tried to add already exists.
        """
        msg = BotMessage.get_message(BotResponseType.SYMPTOM_EXISTS).format(symptom=symptom)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def symptom_removed(symptom, rerun=False):
        """
        Confirms the removal of a specified symptom.
        """
        msg = BotMessage.get_message(BotResponseType.SYMPTOM_REMOVED).format(symptom=symptom)  # Corrected the type to SYMPTOM_REMOVED for consistency
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def disease_detected(disease, rerun=False):
        """
        Displays the disease prediction and optionally additional advice to the user.
        """
        msg = BotMessage.get_message(BotResponseType.DISEASE).format(disease=disease)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)

    @staticmethod
    def bye(rerun=False):
        """
        Sends a goodbye message, concluding the interaction or allowing for a new patient query.
        """
        msg = BotMessage.get_message(BotResponseType.BYE)
        DataController.add_messages(encodeMessage(msg, True), rerun=rerun)
