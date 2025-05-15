# clean_and_visualize.py

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tqdm import tqdm

# Download stopwords (only once)
nltk.download('stopwords')

# Enable tqdm progress bar with pandas
tqdm.pandas()

# 1. Load the cleaned news data
print("📄 Loading dataset...")
df = pd.read_csv('data/cleaned_news.csv')

# 2. Load stopwords once (important for speed!)
stop_words = set(stopwords.words('english'))

# 3. Define a faster text cleaning function
def clean_text(text):
    text = str(text).lower()                      # Lowercase
    text = re.sub(r'[^a-z\s]', '', text)           # Remove punctuation/numbers
    words = text.split()                          # Split into words
    words = [w for w in words if w not in stop_words]  # Remove stopwords
    return ' '.join(words)

# 4. Clean the text column with progress bar
print("🧹 Cleaning text... (please wait)")
df['clean_text'] = df['text'].progress_apply(clean_text)

# 5. Separate fake and real texts
print("🔀 Splitting fake and real news...")
fake_text = ' '.join(df[df['label'] == 0]['clean_text'])
real_text = ' '.join(df[df['label'] == 1]['clean_text'])

# 6. Generate and show word clouds
def show_wordcloud(text, title):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.show()

print("☁️ Generating Fake News WordCloud...")
show_wordcloud(fake_text, 'Fake News Word Cloud')

print("☁️ Generating Real News WordCloud...")
show_wordcloud(real_text, 'Real News Word Cloud')

print("\n✅ All done! Word clouds generated.")

# 7. Save the updated DataFrame with the cleaned column
df.to_csv('data/cleaned_news.csv', index=False)
print("💾 Cleaned data saved to data/cleaned_news.csv")
