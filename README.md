# 🕵️‍♂️ Fake News Detector Extension

This is a Chrome Extension that checks if the news article you're reading is **real or fake** using a machine learning model hosted on your local Flask server.

---

## ✨ Features

- 📰 Detects whether an article is **REAL** or **FAKE**
- 🌐 Works best on **plain HTML news websites** (see list below)
- 🔌 Communicates with a local Flask server
- 🤖 Uses a Logistic Regression model and TF-IDF vectorizer
- 📊 Shows prediction result with a confidence percentage

---

## 🧪 Good & Bad Pages for Testing

### ✅ Good Pages (WORKS WELL)

These pages:
- Show **full article text in plain HTML**
- Do **not use JavaScript-heavy frameworks**
- Are **not behind paywalls or logins**
- Do **not require scrolling** to load content

**Examples:**
- Archive websites (e.g., [text.npr.org](https://text.npr.org))
- Plain HTML blogs or static news pages
- Minimalistic independent journalism pages

---

### ❌ Bad Pages (WON’T WORK)

Avoid pages with:
- 🔐 Paywalls or login popups (CNN, Washington Post)
- ⚙️ React/Vue/Angular apps (SPA)
- 🔄 Dynamically loaded content (AJAX after scrolling)
- 🧱 Shadow DOM or iframes

**Examples that often fail:**
- CNN, Fox News, BBC (some), Washington Post
- Most AMP or modern JS-driven sites

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mantix1/FakeNewsDetector.git
cd FakeNewsDetector
