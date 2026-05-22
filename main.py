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

# Create DataFrame for better visualization
df = pd.DataFrame({'email': emails, 'label': labels})
df['label_name'] = df['label'].map({1: 'Phishing', 0: 'Safe'})

# Display sample emails
print("\n" + "="*80)
print("SAMPLE PHISHING EMAIL:")
print("="*80)
print(df[df['label']==1]['email'].iloc[0])
print("\n" + "="*80)
print("SAMPLE SAFE EMAIL:")
print("="*80)
print(df[df['label']==0]['email'].iloc[0])

# Feature extraction functions
def extract_url_features(text):
    """Extract URL-related features from email text"""
    # Find all URLs
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*|bit\.ly/\S+|tinyurl\.com/\S+'
    urls = re.findall(url_pattern, text)

    features = {
        'num_urls': len(urls),
        'has_http': any('http://' in url for url in urls),
        'has_url_shortener': any('bit.ly' in url or 'tinyurl' in url for url in urls),
        'avg_url_length': np.mean([len(url) for url in urls]) if urls else 0,
        'has_suspicious_tld': any(url.endswith(('.tk', '.ml', '.ga', '.cf', '.xyz')) for url in urls)
    }
    
    return features

def extract_keyword_features(text):
    """Extract keyword-based features"""
    phishing_indicators = [
        'verify', 'confirm', 'urgent', 'suspended', 'security alert',
        'unauthorized', 'click here', 'update now', 'immediately',
        'bank account', 'credit card', 'password', 'social security'
    ]

    features = {
        'num_phishing_keywords': sum(text.lower().count(keyword) for keyword in phishing_indicators),
        'has_urgent_language': any(word in text.lower() for word in ['urgent', 'immediately', 'asap']),
        'has_threat': any(word in text.lower() for word in ['suspended', 'locked', 'closed', 'terminated'])
    }
    
    return features

def extract_structural_features(text):
    """Extract email structural features"""
    features = {
        'text_length': len(text),
        'num_exclamation': text.count('!'),
        'num_uppercase_words': sum(1 for word in text.split() if word.isupper() and len(word) > 2),
        'has_deadline': any(word in text.lower() for word in ['24 hours', '48 hours', 'within', 'today'])
    }
    
    return features

# Apply feature extraction to all emails
print("\n" + "="*80)
print("EXTRACTING FEATURES...")
print("="*80)

feature_list = []
for email in emails:
    # Extract all features
    url_features = extract_url_features(email)
    keyword_features = extract_keyword_features(email)
    structural_features = extract_structural_features(email)

    # Combine all features
    all_features = {**url_features, **keyword_features, **structural_features}
    feature_list.append(all_features)

# Create feature DataFrame
X = pd.DataFrame(feature_list)
y = np.array(labels)

print(f"\nFeatures extracted: {X.shape[1]} features")
print(f"Feature names: {list(X.columns)}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")
print(f"Training distribution: {sum(y_train)} phishing, {len(y_train)-sum(y_train)} safe")
print(f"Test distribution: {sum(y_test)} phishing, {len(y_test)-sum(y_test)} safe")

# Train Random Forest Classifier
print("\n" + "="*80)
print("TRAINING MODEL...")
print("="*80)

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)

rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)
y_pred_proba = rf_model.predict_proba(X_test)[:, 1]

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
