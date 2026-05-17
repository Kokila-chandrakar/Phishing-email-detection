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
            
        # Select phishing keywords
        num_keywords = np.random.randint(2, 5)
        selected_keywords = np.random.choice(phishing_keywords, num_keywords, replace=False)

        # Create email content
        email = f"""
        Subject: {np.random.choice(['URGENT', 'Important', 'Security Alert', 'Action Required'])}: {selected_keywords[0].title()}

        {np.random.choice(phishing_keywords)}. Our system detected {np.random.choice(['suspicious activity', 'unusual login', 'multiple failed attempts'])}.
        
        Please {selected_keywords[1]} by clicking the link below:
        {url}

        Failure to {selected_keywords[2] if len(selected_keywords) > 2 else 'verify'} within 24 hours will result in account suspension.
        
        Best regards,
        Security Team
        """

        emails.append(email)
        labels.append(1)  # 1 for phishing

    # Generate legitimate emails
    for i in range(n_samples // 2):
        # Select URL
        url = np.random.choice(safe_urls)

        # Select safe keywords
        num_keywords = np.random.randint(2, 4)
        selected_keywords = np.random.choice(safe_keywords, num_keywords, replace=False)

        # Create email content
        email = f"""
        Subject: {np.random.choice(['Your', 'Monthly', 'Weekly'])} {selected_keywords[0].title()}
        
        Hello,
        
        {selected_keywords[1]}. You can view your details at:
        {url}

                {selected_keywords[2] if len(selected_keywords) > 2 else 'Thank you for being a valued customer'}.
        
        Best regards,
        Customer Service
        """

        emails.append(email)
        labels.append(0)  # 0 for safe/legitimate

    return emails, labels

# Generate the dataset
print("Generating synthetic email dataset...")
emails, labels = generate_email_dataset(1000)
print(f"Dataset created: {len(emails)} emails")
print(f"Phishing: {sum(labels)} emails")
print(f"Safe: {len(labels) - sum(labels)} emails")
