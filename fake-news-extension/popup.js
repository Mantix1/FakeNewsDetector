document.getElementById("checkButton").addEventListener("click", () => {
  try {
      console.log("📌 Button clicked. Sending message to content script...");

      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (!tabs.length) {
              alert("❌ No active tab found.");
              return;
          }

          chrome.tabs.sendMessage(tabs[0].id, { action: "analyze" }, (response) => {
              if (chrome.runtime.lastError) {
                  console.error("🚫 Could not send message:", chrome.runtime.lastError.message);
                  alert("❌ Error: Could not connect to the page.");
                  return;
              }

              if (response?.error) {
                  console.error("⚠️ Error from content script:", response.error);
                  alert("❌ Failed to extract text: " + response.error);
                  return;
              }

              if (!response?.text) {
                  console.error("⚠️ No article text returned.");
                  alert("❌ No text extracted.");
                  return;
              }

              console.log("✅ Sending extracted text to backend:", response.text.slice(0, 100), "...");
              
              // Send article text to Flask API
              fetch("http://127.0.0.1:5001/predict", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ text: response.text }),
              })
              .then(res => res.json())
              .then(data => {
                if (data.error) {
                    alert("❌ Prediction failed: " + data.error);
                    return;
                }
            
                const prediction = data.prediction || "Unknown";
                const rawConfidence = typeof data.confidence === "number" ? data.confidence : 0;
                const confidencePercent = (rawConfidence).toFixed(2);
            
                alert(`✅ Prediction: ${prediction} (${confidencePercent}%)`);
            })            
              .catch(err => {
                  console.error("❌ Fetch error:", err);
                  alert("❌ Failed to fetch prediction: " + err.message);
              });
          });
      });
  } catch (err) {
      console.error("❌ popup.js runtime error:", err);
      alert("❌ popup.js crashed: " + err.message);
  }
});
