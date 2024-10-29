# feature_extractor.py

import numpy as np
import librosa

class FeatureExtractor:
    def __init__(self, n_mfcc=13):
        self.n_mfcc = n_mfcc

    def extract_features(self, file_path):
        """Extracts MFCC features from an audio file."""
        audio, sr = librosa.load(file_path, sr=None)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=self.n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)
        return mfccs_mean
