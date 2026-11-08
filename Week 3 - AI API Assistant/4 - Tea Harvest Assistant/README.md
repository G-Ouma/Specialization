# Tea Harvest Assistant 🌱

An AI-powered assistant designed to help tea estate staff make informed harvesting decisions using weather information and Google's Gemini API.

The project combines live weather data from OpenWeatherMap and Open-Meteo with Gemini's function-calling capabilities to provide practical tea harvesting recommendations.

## 1. Project Overview

The assistant accepts natural-language questions and determines whether live weather information is needed.

When weather information is relevant, Gemini can call a Python weather function that retrieves current conditions and the next six hours of forecasts for Kericho, Kenya.

The assistant then interprets the information and provides a recommendation in simple language.

## 2. Technologies Used

- **Python** – Main programming language.
- **Google Gemini API** – Natural-language understanding and AI responses.
- **Gemini Function Calling** – Allows the model to request external weather information.
- **OpenWeatherMap API** – Retrieves current weather conditions.
- **Open-Meteo API** – Provides hourly weather forecasts.
- **Requests** – Makes HTTP requests to the weather APIs.
- **python-dotenv** – Loads API keys from environment variables.

## 3. How It Works

1. The user submits a question.
2. Gemini interprets the question.
3. Gemini decides whether live weather information is required.
4. If required, Gemini calls the Python `get_weather()` function.
5. The function retrieves current weather and the next six hours of forecasts.
6. Gemini interprets the returned information and generates a practical response.

For general questions and greetings, the assistant can respond without retrieving weather information.

## 4. Weather Decision Rules

The current harvesting guidelines used in the system instruction are:

| Condition | Guideline |
|---|---|
| Temperature | Preferred range: 15–25°C |
| Humidity | Below 70% is preferred |
| Rain | No rain expected over the next six hours |
| Active rain | Unfavourable for harvesting |
| Temperature above 28°C | Unfavourable for harvesting |

**Note:** The 70% humidity threshold is an initial operational assumption, not a universal tea harvesting standard. These guidelines will need validation against actual tea estate practices.

## 5. Current Project Features

- Natural-language interaction with Gemini.
- Automatic weather function calling.
- Current weather retrieval.
- Six-hour hourly weather forecasting.
- Combined weather data from two APIs.
- Plain-language harvesting recommendations.
- Direct responses to general questions and greetings.

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or later.
- A Google Gemini API key.
- An OpenWeatherMap API key.

### Install dependencies

```bash
pip install google-genai requests python-dotenv
```

### Environment variables

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never commit your `.env` file or expose your API keys.

### Run the assistant

```bash
python main.py
```

Type `exit` to close the application.

## 7. Initial Testing

The assistant has been tested with the following questions:

| User question | Expected behaviour | Result |
|---|---|---|
| Is today suitable for harvesting tea? | Retrieve weather and provide a recommendation | Passed |
| What does humidity mean? | Explain without retrieving live weather | Passed |
| Good morning | Respond without retrieving live weather | Passed |

The initial tests demonstrate that Gemini can respond to general questions and use the weather function when weather information is relevant.

## 8. Areas for Improvement

The project is still under development.

### A. Conversation management
- Replace direct `generate_content()` usage with `client.chats.create()` and `chat.send_message()`.
- Maintain conversation context between messages.
- Improve multi-turn interactions.

### B. Function calling visibility
- Add logging to show when Gemini requests the weather function.
- Display when the weather API is being accessed.
- Handle failed function calls more gracefully.

### C. Weather data and decision-making
- Improve rain detection using both current weather conditions and forecast data.
- Handle missing or incomplete weather forecasts.
- Validate harvesting thresholds with actual tea estate operating practices.
- Consider additional factors that influence plucking and field operations.

### D. Error handling
- Improve handling of Gemini API failures and rate limits.
- Handle weather API timeouts and unavailable services.
- Provide clearer feedback when live weather data cannot be retrieved.

### E. Future development
- Allow users to select different tea estate locations.
- Add a simple web interface.
- Store weather observations and harvesting recommendations.
- Introduce historical weather analysis.
- Explore predictive models for harvesting conditions.

## 9. Current Development Status

**Working prototype.**

The weather retrieval function and initial Gemini integration are operational. Initial conversational tests have passed.

The next development milestone is improving conversation management and adding function-calling logs.

---

*This project is being developed as a practical exploration of AI agents, Python API integration, and tool/function calling.*