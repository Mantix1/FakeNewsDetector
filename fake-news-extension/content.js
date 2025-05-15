try {
    console.log("📄 content.js loaded.");

    function extractArticleText() {
        let textContent = "";

        // Try to extract common article elements used by news websites
        const articleTags = document.querySelectorAll("article, .article, .story-body, .post-content, .entry-content, .main-content");

        articleTags.forEach(tag => {
            textContent += tag.innerText + "\n";
        });

        // Fallback if no known article structure is found
        if (!textContent.trim()) {
            console.warn("⚠️ No article tags matched. Falling back to full body text.");
            textContent = document.body.innerText;
        }

        return textContent.trim();
    }

    // Listen for requests from popup.js
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === "analyze") {
            const articleText = extractArticleText();

            if (articleText) {
                console.log("✅ Article text successfully extracted.");
                sendResponse({ text: articleText });
            } else {
                console.error("❌ Failed to extract article text.");
                sendResponse({ error: "No article text found." });
            }
        }
        return true; // Required to keep the message channel open for async response
    });

} catch (err) {
    console.error("❌ content.js failed with error:", err);
}
