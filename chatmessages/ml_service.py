from joblib import load
import os


model_path = os.path.join(os.path.dirname(__file__), "flag_model.joblib")
model = load(model_path)


def is_flagged_message(text):
    return model.predict([text])[0]
