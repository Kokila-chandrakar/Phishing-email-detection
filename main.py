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
    
    # Common phishing patterns
    phishing_urls = [
        "http://secure-paypal-verify.com", "https://amazon-account-update.net",
        "http://bankofamerica-security.com", "https://appleid-verify.org",
        "http://netflix-account-suspended.com", "https://chase-banking-alert.net",
        "http://microsoft-security-update.com", "https://paypal-verification-service.com",
        "bit.ly/3xYZ123", "tinyurl.com/secure-login"
    ]
    
    # Legitimate URLs
    safe_urls = [
        "https://amazon.com", "https://paypal.com", "https://bankofamerica.com",
        "https://apple.com", "https://netflix.com", "https://chase.com",
        "https://microsoft.com", "https://google.com", "https://linkedin.com"
    ]

    # Phishing keywords
    phishing_keywords = [
        "verify your account", "confirm your identity", "account suspended",
        "urgent action required", "security alert", "unauthorized login",
        "click here to verify", "update your payment", "account locked",
        "verify immediately"
    ]

    # Legitimate keywords
    safe_keywords = [
        "newsletter", "your statement", "weekly digest", "transaction receipt",
        "welcome to", "thank you for your purchase", "your subscription",
        "account summary", "payment received", "order confirmed"
    ]

    emails = []
    labels = []

    # Generate phishing emails
    for i in range(n_samples // 2):
        # Select random URL (80% chance of phishing URL, 20% legitimate URL to make it realistic)
        if np.random.random() < 0.8:
            url = np.random.choice(phishing_urls)
        else:
            url = np.random.choice(safe_urls)
