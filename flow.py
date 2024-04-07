import streamlit as st
from data import *  # Importing DataController and other necessary components
from bot_responses import BotResponse  # Handling predefined bot responses
from display_message import display_messages  # For displaying messages in the UI
from input_button import *  # For rendering input buttons in the UI
from predict import DiseaseDetector  # The model for disease prediction
from symptoms import model_symptoms  # Predefined list of symptoms
import json  # For loading disease advice from a JSON file
import os

class RunFlow:
    def __init__(self):
        # Initialize the chatbot interface with a welcome message using Streamlit.
        st.markdown("<h1>Welcome to Symptom Chatbot</h1>", unsafe_allow_html=True)
        
        # Instantiate the DiseaseDetector, which will be used for predicting diseases based on user inputs.
        self.predictor = DiseaseDetector()
        
        # Load advice and recommendations for handling various diseases from a JSON file.
        self.disease_advice = self.load_disease_advice()

    def load_disease_advice(self):
        # Try to load disease advice data from a JSON file; if unsuccessful, return an empty dictionary.
        try:
            with open('advice.json') as file:
                return json.load(file)
        except Exception as e:
            print(f"Failed to load disease advice data: {e}")
            return {}

    def predict_disease(self):
        # Fetch the user's symptoms from the DataController and use the disease detector to predict the disease.
        symptoms = DataController.get_patient_symptoms()
        return self.predictor.predict(symptoms)
    
    # Define callback functions for various user interactions throughout the chatbot conversation.
    
    def patient_who_callback(self, value):
        # Update the conversation based on who the patient is (self or other) and advance the state.
        msg = "I am the patient." if value.lower() == "self" else "I am searching for someone else."
        DataController.add_messages(encodeMessage(msg, isBot=False))
        DataController.change_state(ProgramState.GENDER)
        DataController.set_bot_replied_status(False)

    def ask_gender_callback(self, value):
        # Record the patient's gender, update the conversation, and move to the next state.
        msg = "I am Male." if value == Gender.MALE else "I am Female."
        DataController.add_messages(encodeMessage(msg, isBot=False))
        DataController.change_state(ProgramState.NAME)
        DataController.set_bot_replied_status(False)

    def ask_name_callback(self, value):
        # Save the patient's name, update the conversation, and progress to collecting the patient's age.
        DataController.add_messages(encodeMessage(f"My name is {value}", isBot=False))
        DataController.set_patient_name(value)
        DataController.change_state(ProgramState.AGE)
        DataController.set_bot_replied_status(False)

    def ask_age_callback(self, value):
        # Validate and record the patient's age, then move on to symptom collection.
        if value is None:
            return
        try:
            age = int(value)
            if age < 1 or age > 100:
                raise ValueError("Invalid age")
            DataController.add_messages(encodeMessage(f"I am {age} years old", isBot=False))
            DataController.set_patient_age(age)
            DataController.set_bot_replied_status(False)
            DataController.change_state(ProgramState.SYMPTOM)
        except ValueError:
            DataController.add_messages(encodeMessage(BotResponse.invalid_age()))

    def add_symptom_callback(self, value):
        # Add a symptom to the patient's record; notify if already exists or if added, then check if ready to predict.
        DataController.add_messages(encodeMessage(f"Add {value} symptom.", isBot=False))
        if DataController.add_patient_symptom(value):
            BotResponse.symptom_added(value)
        else:
            BotResponse.symptom_exists(value)
        DataController.set_bot_replied_status(False)
        # Move to disease prediction if enough symptoms have been collected.
        if len(DataController.get_patient_symptoms()) > 4:
            DataController.change_state(ProgramState.DISEASE)
        time.sleep(0.1)
        st.rerun()

    def remove_symptom_callback(self, value):
        # Remove a symptom from the patient's record and update accordingly.
        DataController.add_messages(encodeMessage(f"Remove {value} symptom.", isBot=False))
        DataController.remove_patient_symptom(value)
        BotResponse.symptom_removed(value)
        DataController.set_bot_replied_status(False)
        time.sleep(0.1)
        st.rerun()

    def detect_symptom_callback(self):
        # Directly proceed to the disease prediction stage.
        DataController.set_bot_replied_status(False)
        DataController.change_state(ProgramState.DISEASE)
        time.sleep(0.1)



    # UI Methods: These methods define the UI flow of the application, guiding the user through
    # each step of the interaction from identifying the patient to providing disease advice.

    def welcome(self):
        """
        Handles the welcome state of the application.
        Sets the program state to initiate the patient identification process.
        """
        DataController.change_state(ProgramState.PATIENT_WHO)
        BotResponse.welcome(rerun=True)

    def patient_who(self):
        """
        Displays options to identify whether the user is entering symptoms for themselves or someone else.
        """
        opts = ['Self', 'Other']
        if not DataController.bot_replied_status():
            DataController.set_bot_replied_status(True)
            BotResponse.patient_who(rerun=False)
        display_messages()
        display_2_options(opts, [lambda: self.patient_who_callback(opts[0]), lambda: self.patient_who_callback(opts[1])])

    def ask_gender(self):
        """
        Prompts the user for the patient's gender.
        Advances the conversation based on the user's selection.
        """
        if not DataController.bot_replied_status():
            DataController.set_bot_replied_status(True)
            BotResponse.patient_who(rerun=False)
        display_messages()
        display_2_options(['Male', 'Female'], [lambda: self.ask_gender_callback(Gender.MALE), lambda: self.ask_gender_callback(Gender.FEMALE)])

    def ask_name(self):
        """
        Requests the patient's name from the user.
        Updates the conversation and progresses to the next step.
        """
        if not DataController.bot_replied_status():
            DataController.set_bot_replied_status(True)
            BotResponse.ask_name(rerun=False)
        display_messages()
        display_input_field("Enter patient's name", on_submit=self.ask_name_callback)
        
    def ask_age(self):
        """
        Asks for the patient's age, ensuring valid input before moving forward.
        """
        if not DataController.bot_replied_status():
            DataController.set_bot_replied_status(True)
            BotResponse.ask_age(rerun=False)
        display_messages()
        display_input_field("Enter patient's age", on_submit=self.ask_age_callback)
        
    def ask_symptom(self):
        """
        Guides the user through symptom entry, providing options to add or remove symptoms.
        Automatically proceeds to disease prediction if sufficient symptoms are collected.
        """
        symptoms = DataController.get_patient_symptoms()
        if not DataController.bot_replied_status():
            DataController.set_bot_replied_status(True)
            BotResponse.ask_symptom(rerun=False) if len(symptoms) > 0 else BotResponse.ask_more_symptoms(rerun=False)
        display_messages()
        # Adjust UI based on the number of symptoms entered.
        if len(symptoms) < 1:
            symptom_popup("Add Symptom", model_symptoms, on_submit=self.add_symptom_callback)
        elif len(symptoms) < 3:
            add_remove_symptom_popup(symptoms, DataController.get_patient_symptoms(), on_add=self.add_symptom_callback, on_remove=self.remove_symptom_callback)
        elif len(symptoms) < 4:
            add_remove_detect_symptom_popup(symptoms, DataController.get_patient_symptoms(), on_add=self.add_symptom_callback, on_remove=self.remove_symptom_callback, on_detect=self.detect_symptom_callback)
        else:
            self.detect_symptom_callback()

    def detect_disease(self):
        """
        Predicts the disease based on collected symptoms and displays the result along with advice.
        """
        if not DataController.bot_replied_status():
            DataController.set_bot_replied_status(True)
            disease = self.predict_disease()
            # Fetch and display advice and medications for the diagnosed disease.
            disease_info = self.disease_advice.get(disease, {})
            advice = disease_info.get('advice', 'Please consult a healthcare provider for more information.')
            medications = ', '.join(disease_info.get('medications', ['Consult a healthcare provider for medication options.']))
            full_message = f"{disease}\n\nAdvice: {advice}\nOTC Medications: {medications}"
            BotResponse.disease_detected(full_message)
        display_messages()

    def bye(self):
        """
        Concludes the chat session, offering the user an option to restart with a new patient.
        """
        DataController.add_messages(encodeMessage("Bye", isBot=False))
        if not DataController.bot_replied_status():
            DataController.set_bot_replied_status(True)
            BotResponse.bye()
        display_messages()
        if st.button("Try New Patient"):
            self.new_patient()

    def run(self):
        """
        The main loop of the application. Determines the current state and executes the corresponding method.
        """
        state = DataController.get_program_state()
        # Execute the method associated with the current state of the chatbot.
        if state == ProgramState.WELCOME:
            self.welcome()
        elif state == ProgramState.PATIENT_WHO:
            self.patient_who()
        elif state == ProgramState.GENDER:
            self.ask_gender()
        elif state == ProgramState.NAME:
            self.ask_name()
        elif state == ProgramState.AGE:
            self.ask_age()
        elif state == ProgramState.SYMPTOM:
            self.ask_symptom()
        elif state == ProgramState.DISEASE:
            self.detect_disease()
        elif state == ProgramState.BYE:
            self.bye()