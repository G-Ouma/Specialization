# Kisumu Pharmacy Chatbot

A Python command-line chatbot designed to help staff at Kisumu Pharmacy in Kisumu, Kenya, respond to common customer enquiries consistently.

The chatbot uses Google's Gemini API to answer questions about pharmacy services, operating hours, prescriptions and general customer enquiries.

## Features

- **Pharmacy information:** Provides operating hours and available services.
- **Prescription enquiries:** Explains prescription processing and repeat prescription requirements.
- **Conversation memory:** Maintains context throughout an active conversation, allowing users to ask follow-up questions without repeating themselves.
- **Knowledge boundaries:** Avoids inventing medicine availability, prices or unsupported services.
- **Error handling:** Handles API failures and provides user-friendly error messages.

## Pharmacy Information

**Operating hours**

| Day | Hours |
|---|---|
| Monday – Saturday | 8:00 AM – 8:00 PM |
| Sunday | 10:00 AM – 4:00 PM |

**Services**

1. Prescription dispensing.
2. Repeat prescription processing.
3. Over-the-counter medication sales.
4. Prescription review and verification.
5. Blood pressure checks.
6. Blood glucose testing.
7. Medication counselling.
8. General health and wellness products.

## Technologies Used

- Python
- Google Gemini API
- Google Gen AI SDK
- python-dotenv

## Project Structure

```text
Pharmacy Chatbot/
│
├── main.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <git@github.com:G-Ouma/Specialization.git>
```

Navigate to the project directory:

```bash
cd "Week 3 - AI API Assistant/Pharmacy Chatbot"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-flash-latest
```

Replace `your_gemini_api_key` with your actual Gemini API key.

Never commit your `.env` file to GitHub.

### 4. Run the chatbot

```bash
python main.py
```

## Example Conversation

```text
Staff: I have a prescription.

Chatbot: We can help you with that!
Straightforward prescriptions typically take
15 to 30 minutes, depending on workload,
medicine availability and pharmacist verification.

Staff: How long will it take?

Chatbot: Straightforward prescriptions typically
take 15 to 30 minutes. The exact time depends
on workload and medicine availability.
```

The chatbot remembers the earlier prescription enquiry and understands the follow-up question.

## Conversation Memory

The application uses Gemini's chat session functionality to maintain conversation history.

This allows the chatbot to:
- Understand follow-up questions.
- Retain relevant information shared earlier.
- Provide more natural conversational responses.

Conversation history is maintained during the active application session. It is not permanently stored between application restarts.

## Limitations

- Requires an active internet connection and a valid Gemini API key.
- Depends on Gemini API availability and usage limits.
- Does not access live pharmacy inventory.
- Does not have access to an official medication price list.
- Does not replace professional medical advice or pharmacist verification.
- Prescription processing times and documentation requirements should be confirmed by pharmacy management.

## Future Improvements

- Integrate a pharmacy inventory database.
- Add medication pricing information.
- Introduce persistent conversation history.
- Build a graphical or web-based interface.
- Add more robust API retry and recovery mechanisms.

## Author

Developed as a Python AI API assistant project.