# predictor.py

import random
from config import EMOTIONS, RANDOM_EMOTIONS

class EmotionPredictor:
    def __init__(self, use_random=True):
        self.use_random = use_random

    def predict_emotion(self, features=None):
        """
        Predicts the emotion based on extracted features.
        Currently returns a random emotion for simulation.
        """
        if self.use_random:
            emotion = random.choice(RANDOM_EMOTIONS)
        else:
            # Placeholder for actual prediction logic using ML models
            emotion = "Unknown"
        return emotion
