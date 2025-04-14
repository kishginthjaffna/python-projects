document.addEventListener("DOMContentLoaded", function () {
    const submitBtn = document.getElementById("submitButton");
    const inputField = document.getElementById("inputField");
    const container = document.getElementById("container");

    submitBtn.addEventListener("click", async () => {
        const url = inputField.value.trim();
        if (!url) {
            alert("Please enter a YouTube video URL.");
            return;
        }

        container.style.display = "none";
        container.innerHTML = "⏳ Summarizing...";

        try {
            const response = await fetch("/summarize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();
            if (response.ok) {
                container.innerHTML = `<strong>Summary:</strong><br><br>${data.summary}`;
            } else {
                container.innerHTML = `❌ Error: ${data.error || "Something went wrong."}`;
            }
        } catch (err) {
            container.innerHTML = `❌ Error: ${err.message}`;
        }

        container.style.display = "block";
    });
});
