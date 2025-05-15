# src/predict.py

import joblib
import os

# 1. Load saved model and vectorizer
model_path = 'models/fake_news_model.pkl'
vectorizer_path = 'models/tfidf_vectorizer.pkl'

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    print("❌ Model or vectorizer not found. Make sure you've run save_model.py first.")
    exit()

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

print("✅ Model and vectorizer loaded.")

# 2. Ask the user to enter a news article or headline
print("\n📰 Enter a news article or headline to analyze (or type 'exit' to quit):\n")

while True:
    user_input = input(">> ")

    if user_input.lower() == 'exit':
        print("👋 Exiting. Stay informed!")
        break

    # 3. Clean input and vectorize
    input_vector = vectorizer.transform([user_input])

    # 4. Predict using the model
    prediction = model.predict(input_vector)

    # 5. Show result
    if prediction[0] == 0:
        print("❌ This article is likely FAKE.\n")
    else:
        print("✅ This article is likely REAL.\n")
