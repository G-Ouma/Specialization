# AI API Assistant Projects

This collection contains Python prototypes that use Google's Gemini API to support practical information and workflow tasks.

## Projects

| Project | What it does |
|---|---|
| [Matatu Assistant](1%20-%20Matatu%20Assistant/README.md) | Answers common matatu SACCO member questions from prompt-defined demonstration information |
| [Property Inquiry Extractor](2%20-%20Property%20Inquiry/README.md) | Extracts property requirements from a manually entered enquiry and appends them to Google Sheets |
| [Pharmacy Chatbot](3%20-%20Pharmacy%20Chatbot/README.md) | Provides information from configured pharmacy guidance in a conversational terminal session |
| [Tea Harvest Assistant](4%20-%20Tea%20Harvest%20Assistant/README.md) | Uses Gemini function calling to retrieve weather information for a Kericho tea estate |
| [AI Proposal Assistant](AI%20Proposal%20Assistant/README.md) | Analyses client briefs and generates concise proposals using deterministic Python pricing |

## Shared setup

These projects use the Python environment at the root of the repository. Follow the [main setup guide](../README.md), activate the shared `venv`, and install the root dependencies.

Most projects require the following root environment variable:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Projects that read the model name from configuration can also use:

```env
GEMINI_MODEL=gemini-3.5-flash-lite
```

Check each project's README for additional credentials, such as OpenWeather or Google OAuth. Do not assume every project uses the same configuration: some scripts set their model directly in source code, while others read it from the environment.

## Concepts explored

- Gemini model requests and system instructions
- Prompt design and structured JSON extraction
- Conversational chat sessions
- Function calling and external API integration
- Google Sheets OAuth and data insertion
- Separating deterministic application logic from AI-generated text
- Error handling and prototype limitations

These are learning projects. Their individual READMEs identify sample data, implemented behaviour, external dependencies, and limitations.
