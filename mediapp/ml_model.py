import numpy as np
import os
import logging
import pandas as pd
from django.conf import settings
from .ml_models.medical_cost_model import MedicalCostModel
from .ml_models.data_preprocessing import preprocess_input

logger = logging.getLogger(__name__)

class MedicalCostPredictor:
    #A class to handle loading and predictions from a trained ML model for medical cost predictions    
    def __init__(self):
        self.model = MedicalCostModel()
        self.model_loaded = False
        self.model_path = os.path.join(settings.BASE_DIR, 'mediapp', 'ml_models', 'cost_predictor_model.pkl')
        self.dataset_path = os.path.join(settings.BASE_DIR, 'mediapp', 'ml_models', 'insurance.csv')
        self.load_model()
    
    def load_model(self):
        #Load the trained model from file if it exists
        try:
            self.model_loaded = self.model.load(self.model_path)
            if self.model_loaded:
                logger.info("ML model loaded successfully")
            else:
                logger.warning(f"Model file not found at {self.model_path}, falling back to default prediction")
                # Try to train the model with the dataset
                if os.path.exists(self.dataset_path):
                    logger.info(f"Attempting to train model with dataset at {self.dataset_path}")
                    self.train_model()
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
    
    def train_model(self, dataset_path=None):
        """
        Train the model with the dataset
        
        Args:
            dataset_path (str, optional): Path to the dataset file. If None, use default path.
            
        Returns:
            bool: True if training was successful, False otherwise
        """
        try:
            # Use provided dataset path or default
            dataset_path = dataset_path or self.dataset_path
            
            if not os.path.exists(dataset_path):
                logger.error(f"Dataset file not found at {dataset_path}")
                return False
                
            # Load the dataset
            X, y = self.model.load_dataset(dataset_path)
            if X is None or y is None:
                logger.error("Failed to load dataset")
                return False
                
            # Compare different models
            best_model, results = self.model.compare_models(X, y)
            logger.info(f"Best model: {best_model}")
            
            # Train the Linear Regression model (our default model for predictions)
            success = self.model.fit(X, y)
            
            if success:
                # Save the trained model
                self.model.save(self.model_path)
                self.model_loaded = True
                logger.info("Model trained and saved successfully")
                return True
            else:
                logger.error("Failed to train model")
                return False
                
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def predict(self, age, gender, bmi, children, smoker, region):
        """
        Make a prediction using the trained model, or fall back to the
        calculation-based approach if the model isn't available
        """
        try:
            # Preprocess the input data using the utility function
            features = preprocess_input(age, gender, bmi, children, smoker, region)
            
            # Check if model is loaded, if not try to load it
            if not self.model_loaded:
                self.load_model()
                
            # If still not loaded and dataset exists, try to train it
            if not self.model_loaded and os.path.exists(self.dataset_path):
                self.train_model()
                
            # Make prediction using the model (Linear Regression is used by default)
            prediction = self.model.predict(features)
            
            # Round to 2 decimal places
            return round(float(prediction), 2)
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            # Fall back to original calculation logic
            return self.fallback_prediction(age, gender, bmi, children, smoker, region)
    
    def fallback_prediction(self, age, gender, bmi, children, smoker, region):
        """The original calculation logic as a fallback"""
        # ... keep existing code (fallback prediction logic)

# Create a singleton instance
predictor = MedicalCostPredictor()