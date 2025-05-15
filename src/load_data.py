# load_data.py

import pandas as pd

# Load the datasets
fake = pd.read_csv('data/Fake.csv')  # Path to Fake news
real = pd.read_csv('data/True.csv')  # Path to Real news

# Add a label column: 0 = Fake, 1 = Real
fake['label'] = 0
real['label'] = 1

# Combine the two datasets
df = pd.concat([fake, real])

# Shuffle the rows randomly
df = df.sample(frac=1).reset_index(drop=True)

# Show first few rows
print("First 5 entries:")
print(df.head())

# Save cleaned data
df.to_csv('data/cleaned_news.csv', index=False)

print("\n✅ Cleaned data saved to 'data/cleaned_news.csv'")
