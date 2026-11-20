
const generateBtn = document.getElementById("generateBtn");
const reviewBtn = document.getElementById("reviewBtn");

const inputLabel = document.getElementById("inputLabel");
const userInput = document.getElementById("userInput");
const submitBtn = document.getElementById("submitBtn");

const resultSection = document.getElementById("resultSection");
const result = document.getElementById("result");

let currentMode = "generate";

// Safely display dynamic text returned by Gemini.
function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[character]);
}

// Switch to Generate mode
generateBtn.addEventListener("click", () => {
    currentMode = "generate";

    generateBtn.classList.add("active");
    reviewBtn.classList.remove("active");

    inputLabel.textContent = "Paste your client brief";
    userInput.placeholder = "Paste the client brief here...";
    submitBtn.textContent = "Generate Proposal";

    resultSection.classList.add("hidden");
});

// Switch to Review mode
reviewBtn.addEventListener("click", () => {
    currentMode = "review";

    reviewBtn.classList.add("active");
    generateBtn.classList.remove("active");

    inputLabel.textContent = "Paste your existing proposal";
    userInput.placeholder = "Paste your freelance proposal here...";
    submitBtn.textContent = "Review Proposal";

    resultSection.classList.add("hidden");
});

// Helper
function formatProposal(markdown) {
    const lines = markdown.split(/\r?\n/);
    const output = [];

    let inBulletList = false;
    let inNumberedList = false;

    for (const rawLine of lines) {
        const line = rawLine.trim();

        // Close lists when the next line is not a list item
        if (!line.startsWith("- ") && inBulletList) {
            output.push("</ul>");
            inBulletList = false;
        }

        if (!/^\d+\.\s/.test(line) && inNumberedList) {
            output.push("</ol>");
            inNumberedList = false;
        }

        if (!line) continue;

        // Headings
        if (line.startsWith("### ")) {
            output.push(`<h4>${escapeHTML(line.slice(4))}</h4>`);
            continue;
        }

        // Bullet lists
        if (line.startsWith("- ")) {
            if (!inBulletList) {
                output.push("<ul>");
                inBulletList = true;
            }

            output.push(`<li>${formatInlineMarkdown(line.slice(2))}</li>`);
            continue;
        }

        // Numbered lists
        if (/^\d+\.\s/.test(line)) {
            if (!inNumberedList) {
                output.push("<ol>");
                inNumberedList = true;
            }

            output.push(
                `<li>${formatInlineMarkdown(line.replace(/^\d+\.\s/, ""))}</li>`
            );
            continue;
        }

        // Italic assumption or note
        if (line.startsWith("*") && line.endsWith("*")) {
            output.push(`<p><em>${escapeHTML(line.slice(1, -1))}</em></p>`);
            continue;
        }

        // Normal paragraphs
        output.push(`<p>${formatInlineMarkdown(line)}</p>`);
    }

    // Close any lists remaining at the end
    if (inBulletList) output.push("</ul>");
    if (inNumberedList) output.push("</ol>");

    return output.join("\n");
}

// Format bold and italic text safely
function formatInlineMarkdown(text) {
    return escapeHTML(text)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>");
}

// Display the generated results
function displayGenerationResults(data) {
    const analysis = data.analysis || {};
    const effort = analysis.effort_estimate || {};

    const unclearItems = Array.isArray(analysis.what_is_unclear)
        ? analysis.what_is_unclear
        : [];

    const redFlags = Array.isArray(analysis.red_flags)
        ? analysis.red_flags
        : [];

    const unclearHTML = unclearItems.length
        ? unclearItems.map(item => `<li>${escapeHTML(item)}</li>`).join("")
        : "<li>No major uncertainties identified.</li>";

    const redFlagsHTML = redFlags.length
        ? redFlags.map(flag => {
            // Support both string and object red-flag formats.
            if (typeof flag === "string") {
                return `<li>${escapeHTML(flag)}</li>`;
            }

            return `
                <li>
                    <strong>${escapeHTML(flag.phrase)}</strong>
                    <p>${escapeHTML(flag.concern)}</p>
                    <p>${escapeHTML(flag.reason)}</p>
                </li>
            `;
        }).join("")
        : "<li>No red flags identified.</li>";

    let effortHTML;

    if (
        effort.working_days !== null &&
        effort.working_days !== undefined &&
        !effort.needs_scoping
    ) {
        effortHTML = `
            <p><strong>Estimated effort:</strong>
                ${escapeHTML(effort.working_days)} working days</p>
            <p><strong>Confidence:</strong>
                ${escapeHTML(effort.confidence)}</p>
            <p><strong>Reason:</strong>
                ${escapeHTML(effort.reason)}</p>
        `;
    } else {
        effortHTML = `
            <p><strong>Estimated effort:</strong> Requires further scoping</p>
            <p><strong>Reason:</strong>
                ${escapeHTML(effort.reason || "The project scope is unclear.")}</p>
        `;
    }

    result.innerHTML = `
        <section>
            <h3>Client Brief Analysis</h3>

            <h4>1. Problem</h4>
            <p>${escapeHTML(analysis.problem)}</p>

            <h4>2. Deliverable</h4>
            <p>${escapeHTML(analysis.deliverable)}</p>

            <h4>3. Deadline</h4>
            <p>${escapeHTML(analysis.deadline)}</p>

            <h4>4. What is unclear</h4>
            <ul>${unclearHTML}</ul>

            <h4>5. Red Flags</h4>
            <ul>${redFlagsHTML}</ul>
        </section>

        <section>
            <h3>Project Effort Estimate</h3>
            ${effortHTML}
        </section>

        <section>
            <h3>Generated Proposal</h3>
            <div class="proposal-text">
                ${formatProposal(data.proposal)}
            </div>
        </section>
    `;
}

// Send request to FastAPI
submitBtn.addEventListener("click", async () => {
    const text = userInput.value.trim();

    if (!text) {
        alert("Please enter some text first.");
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Processing...";

    resultSection.classList.remove("hidden");
    result.textContent = "Sending your request...";

    try {
        const response = await fetch("http://127.0.0.1:8000/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mode: currentMode,
                text: text
            })
        });

        const data = await response.json();

        console.log("RAW PROPOSAL:", JSON.stringify(data.proposal));

        if (!response.ok) {
            throw new Error(
                data.detail || data.error || "Something went wrong."
            );
        }

        if (currentMode === "generate") {
            displayGenerationResults(data);
        } else {
            result.textContent = data.message;
        }

    } catch (error) {
        result.textContent = `Error: ${error.message}`;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent =
            currentMode === "generate"
                ? "Generate Proposal"
                : "Review Proposal";
    }
});
