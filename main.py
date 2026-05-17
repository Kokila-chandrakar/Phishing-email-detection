import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import re
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.parse import urlparse

# Set random seed for reproducibility
np.random.seed(42)

# Create synthetic dataset
def generate_email_dataset(n_samples=1000):
    """
    Generate synthetic email dataset with phishing and legitimate emails
    """
    
