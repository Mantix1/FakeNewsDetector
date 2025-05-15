chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyze") {
      try {
          console.log("📡 Received 'analyze' message from popup.");

          // Try to extract the main article text
          let text = "";
          const articleTag = document.querySelector("article");
          const bodyTag = document.querySelector("body");

          if (articleTag) {
              text = articleTag.innerText;
              console.log("📰 Extracted from <article> tag:", text.slice(0, 100));
          } else if (bodyTag) {
              text = bodyTag.innerText;
              console.warn("⚠️ <article> tag not found. Fallback to <body>:", text.slice(0, 100));
          }

          if (!text || text.length < 50) {
              console.error("❌ Extracted text is too short or empty.");
              sendResponse({ error: "Extracted text is too short or not found." });
          } else {
              sendResponse({ text });
          }
      } catch (err) {
          console.error("❌ background.js crashed:", err);
          sendResponse({ error: err.message });
      }

      return true; // Keep the message channel open
  }
});
