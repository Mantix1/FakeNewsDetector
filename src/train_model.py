# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# 1. Load cleaned dataset
df = pd.read_csv('data/cleaned_news.csv')

# 2. Drop missing or empty values in clean_text column
df.dropna(subset=['clean_text'], inplace=True)
df = df[df['clean_text'].str.strip() != '']

print(f"✅ Loaded {len(df)} cleaned articles.")

# 3. Define features and labels
X = df['clean_text']  # Features: cleaned news text
y = df['label']       # Labels: 0 for fake, 1 for real

# 4. Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"📊 Data split: {len(X_train)} training / {len(X_test)} testing")

# 5. Convert text to vectors using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)
print("🔠 Text vectorization complete.")

# 6. Train Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_vectors, y_train)
print("🤖 Model training complete.")

# 7. Evaluate on test set
y_pred = model.predict(X_test_vectors)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy:.4f}\n")
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))
