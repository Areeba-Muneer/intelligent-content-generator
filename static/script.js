const steps = ["step1", "step2", "step3", "step4", "step5"];

async function generateContent() {
    const topic = document.getElementById("topic").value.trim();
    const tone = document.getElementById("tone").value;
    const contentLength = document.getElementById("contentLength").value;
    const visualStyle = document.getElementById("visualStyle").value;

    const button = document.getElementById("generateButton");
    const error = document.getElementById("error");
    const result = document.getElementById("result");

    hideError();
    result.style.display = "none";

    if (!topic) {
        showError("Please enter a topic before generating content.");
        return;
    }

    button.disabled = true;
    button.textContent = "Generating...";
    resetPipeline();

    try {
        activate("step1");
        setStatus("Generating Content...");

        const response = await fetch("/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                topic,
                tone,
                content_length: contentLength,
                visual_style: visualStyle
            })
        });

        const data = await response.json();

        if (!data.success) {
            handleError(data);
            return;
        }

        complete("step1");

        activate("step2");
        setStatus("Validating...");
        await sleep(350);
        complete("step2");

        activate("step3");
        setStatus("Creating Image Prompt...");
        await sleep(350);
        complete("step3");

        activate("step4");
        setStatus("Generating Image...");
        await sleep(350);
        complete("step4");

        complete("step5");
        setStatus("Completed Successfully");

        document.getElementById("generatedText").textContent = data.text;
        document.getElementById("imagePrompt").textContent = data.image_prompt;
        document.getElementById("generatedImage").src = data.image_url;

        result.style.display = "block";
    } catch (err) {
        console.error(err);
        showError("The server could not complete the request. Please try again.");
        setStatus("Failed");
    } finally {
        button.disabled = false;
        button.textContent = "Generate Content";
    }
}

function activate(id) {
    const el = document.getElementById(id);
    el.classList.remove("completed");
    el.classList.add("active");
}

function complete(id) {
    const el = document.getElementById(id);
    el.classList.remove("active");
    el.classList.add("completed");
}

function resetPipeline() {
    steps.forEach(id => {
        document.getElementById(id).classList.remove("active", "completed");
    });
    setStatus("Starting...");
}

function setStatus(message) {
    document.getElementById("status").textContent = message;
}

function showError(message) {
    const error = document.getElementById("error");
    error.textContent = message;
    error.style.display = "block";
}

function hideError() {
    document.getElementById("error").style.display = "none";
}

function handleError(data) {
    showError(data.message || "Generation failed. Please try again.");
    setStatus(`Failed at ${data.stage || "unknown stage"}`);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
