# chatmessages/flag_classifier.py

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from django.conf import settings

from .models import ChatMessage
import os


MODEL_PATH = os.path.join(settings.BASE_DIR, "chatmessages", "flag_model.joblib")


class FlagClassifier:
    def __init__(self):
        self.model = None

    def train(self):
        # 1. Load data from the database
        queryset = ChatMessage.objects.exclude(
            is_flagged=None
        )  # skip messages not reviewed
        texts = [msg.message for msg in queryset]
        labels = [msg.is_flagged for msg in queryset]

        if not texts:
            print("⚠️ No data to train on.")
            return None

        # 2. Create a pipeline: TF-IDF vectorizer + LogisticRegression
        pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer()),
                ("clf", LogisticRegression(max_iter=1000)),
            ]
        )

        # 3. Train the model
        pipeline.fit(texts, labels)

        # 4. Save the model
        joblib.dump(pipeline, MODEL_PATH)
        print(f"✅ Model trained and saved to {MODEL_PATH}")
        self.model = pipeline

    def predict(self, text):
        if self.model is None:
            if not os.path.exists(MODEL_PATH):
                raise ValueError("Model not trained yet. Run `train()` first.")
            self.model = joblib.load(MODEL_PATH)

        return self.model.predict([text])[0]
