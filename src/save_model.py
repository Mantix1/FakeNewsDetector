# src/save_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# 1. Load cleaned dataset
df = pd.read_csv('data/cleaned_news.csv')

# 2. Drop any bad/missing cleaned_text
df.dropna(subset=['clean_text'], inplace=True)
df = df[df['clean_text'].str.strip() != '']

# 3. Split into input and labels
X = df['clean_text']
y = df['label']

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Vectorize the text
vectorizer = TfidfVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

# 6. Train the model
model = MultinomialNB()
model.fit(X_train_vectors, y_train)

# 7. Evaluate it
y_pred = model.predict(X_test_vectors)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))

# 8. Save model and vectorizer
os.makedirs('models', exist_ok=True)  # create models/ folder if it doesn't exist

joblib.dump(model, 'models/fake_news_model.pkl')
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')

print("\n💾 Model and vectorizer saved in 'models/' directory.")
