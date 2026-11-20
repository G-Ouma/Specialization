
const complaintInput = document.getElementById("complaint");
const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");

const resultSection = document.getElementById("result");
const replyOutput = document.getElementById("reply");
const statusMessage = document.getElementById("status");


// Generate reply
generateBtn.addEventListener("click", async () => {

    const complaint = complaintInput.value.trim();

    // Validate input
    if (!complaint) {
        statusMessage.textContent = "Please enter a customer complaint.";
        resultSection.style.display = "none";
        return;
    }

    // Set loading state
    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";
    statusMessage.textContent = "Please wait while we prepare your reply.";

    resultSection.style.display = "none";

    try {

        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                complaint: complaint
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to generate a reply.");
        }

        // Display generated reply
        replyOutput.textContent = data.reply;
        resultSection.style.display = "block";

        statusMessage.textContent = "Your reply is ready!";

    } catch (error) {

        statusMessage.textContent = error.message;

    } finally {

        // Restore generate button
        generateBtn.disabled = false;
        generateBtn.textContent = "Generate Reply";

    }

});


// Copy generated reply
copyBtn.addEventListener("click", async () => {

    const reply = replyOutput.textContent;

    if (!reply.trim()) {
        statusMessage.textContent = "There is no reply to copy.";
        return;
    }

    try {

        await navigator.clipboard.writeText(reply);

        statusMessage.textContent = "Reply copied successfully!";

    } catch (error) {

        statusMessage.textContent = "Unable to copy reply. Please copy it manually.";

    }

});
