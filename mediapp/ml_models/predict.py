import joblib
import numpy as np
import os
from django.conf import settings

# Load the model
model_path = os.path.join(settings.BASE_DIR, 'mediapp', 'ml_models', 'insurance_model.pkl')
model = joblib.load(model_path)

def predict(age, sex, bmi, children, smoker, region):
    """
    Make insurance cost prediction
    Args:
        age: int
        sex: str ('male'/'female')
        bmi: float
        children: int
        smoker: str ('yes'/'no')
        region: str (one of ['northeast', 'northwest', 'southeast', 'southwest'])
    Returns:
        float: predicted cost
    """
    # Convert categorical features
    sex_encoded = 0 if sex == 'male' else 1
    smoker_encoded = 1 if smoker == 'yes' else 0
    region_mapping = {
        'northwest': 0,
        'northeast': 1,
        'southeast': 2,
        'southwest': 3
    }
    region_encoded = region_mapping.get(region.lower(), 0)
    
    # Prepare input array
    input_data = np.array([
        age,
        sex_encoded,
        bmi,
        children,
        smoker_encoded,
        region_encoded
    ]).reshape(1, -1)
    
    return float(model.predict(input_data)[0])