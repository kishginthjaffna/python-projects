document.addEventListener("DOMContentLoaded", function () {
    const submitBtn = document.getElementById("submitButton");
    const inputField = document.getElementById("inputField");
    const container = document.getElementById("container");
    const loadingOverlay = document.getElementById("loadingOverlay");

    submitBtn.addEventListener("click", async () => {
        const topic = inputField.value.trim();
        if (!topic) {
            alert("Please enter a topic.");
            return;
        }

        // Show loading screen
        loadingOverlay.classList.remove("hidden");

        try {
            const response = await fetch("/summarize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: topic })
            });

            const data = await response.json();

            if (response.ok) {
                const summaries = data.summaries;

                container.innerHTML = summaries.map(news => `
                    <div class="news-card">
                        <h2 class="news-title">${news.title}</h2>
                        <p class="news-summary"><strong>Summary:</strong><br>${news.summary}</p>
                        
                        <div class="key-takeaways">
                            <strong>Key Takeaways:</strong>
                            <ul>
                                ${news.keyTakeaways.map(takeaway => `<li>${takeaway}</li>`).join("")}
                            </ul>
                        </div>

                        <div class="technologies">
                            <strong>Technologies Involved:</strong>
                            ${news.technologies.length ? news.technologies.join(", ") : "N/A"}
                        </div>
                    </div>
                `).join("");
            } else {
                container.innerHTML = `❌ Error: ${data.error || "Something went wrong."}`;
            }
        } catch (err) {
            container.innerHTML = `❌ Error: ${err.message}`;
        } finally {
            // Hide loading screen
            loadingOverlay.classList.add("hidden");
        }
    });
});
