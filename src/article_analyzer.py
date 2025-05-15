# src/analyze_article.py

from newspaper import Article
from transformers import pipeline
from googlesearch import search
import time
import random

# Load claim extraction model
print("🔍 Loading claim extraction model...")
nlp = pipeline("text2text-generation", model="philschmid/bart-large-cnn-samsum")

def extract_claims(article_text):
    print("✂️ Extracting claims...")
    chunks = [article_text[i:i+1024] for i in range(0, len(article_text), 1024)]
    all_claims = []
    for chunk in chunks:
        result = nlp(f"extract_fact: {chunk}", max_length=128, do_sample=False)[0]['generated_text']
        claims = result.split(". ")
        all_claims.extend(claims)
    return list(set([c.strip(". ") for c in all_claims if len(c) > 20]))

def verify_claim_with_google(claim):
    try:
        print(f"🔎 Verifying: {claim}")
        results = list(search(claim, num_results=3))
        found_sources = sum(1 for link in results if any(domain in link for domain in ['bbc', 'cnn', 'reuters', 'nytimes', 'npr', 'apnews']))
        return found_sources >= 2
    except Exception as e:
        print("Error searching:", e)
        return False

def assess_article(url):
    article = Article(url)
    article.download()
    article.parse()
    print(f"\n📰 Article Title: {article.title}\n")
    claims = extract_claims(article.text)
    print(f"\n🧠 Found {len(claims)} claims.\n")

    verified = 0
    for claim in claims:
        if verify_claim_with_google(claim):
            verified += 1
        time.sleep(random.uniform(1, 2))

    if not claims:
        print("❌ No factual claims found. Cannot determine reliability.")
        return

    prob_real = verified / len(claims)
    verdict = "Real ✅" if prob_real > 0.7 else "Possibly Fake ❌" if prob_real < 0.4 else "Uncertain ⚠️"
    print(f"\n🧾 Verdict: {verdict}")
    print(f"🧮 Verified {verified}/{len(claims)} claims → Probability real: {prob_real:.2%}")
