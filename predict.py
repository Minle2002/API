import pickle
from symptoms import model_symptoms  # Import the list of symptoms the model recognizes
import os

class DiseaseDetector:
    # Specify the path to the serialized decision tree model.

    __MODEL_PATH = "v2/decision_tree-v2.pkl"

    def __load_model(self, path):
        """
        Private method to load the decision tree model from a file.
        
        Args:
            path (str): The file path to the serialized model.
        
        Returns:
            The loaded decision tree model.
        """
        with open(path, 'rb') as f:  # Open the file in binary read mode
            model = pickle.load(f)  # Deserialize the model object
        return model

    def __parse_symptoms(self, symptoms):
        """
        Private method to convert the list of symptoms into a format suitable for the model.
        
        Args:
            symptoms (list): The list of symptoms reported by the user.
        
        Returns:
            A list of integers where 1 indicates the presence of a symptom and 0 indicates absence,
            based on the predefined list of symptoms the model recognizes.
        """
        sym = []
        for s in model_symptoms:
            sym.append(1 if s in symptoms else 0)  # Append 1 if the symptom is present, else 0
        return sym
    
    def __init__(self):
        """
        Initializes the DiseaseDetector by loading the decision tree model from the specified path.
        """
        self.__model = self.__load_model(self.__MODEL_PATH)  # Load the model upon instantiation

    def predict(self, symptoms) -> str:
        """
        Predicts the disease based on the symptoms provided.
        
        Args:
            symptoms (list): The list of symptoms to predict the disease for.
        
        Returns:
            The predicted disease as a string.
        """
        # Convert the user-provided symptoms into the format expected by the model
        syms = self.__parse_symptoms(symptoms)
        # Use the model to predict the disease and return the prediction
        return self.__model.predict([syms])[0]
