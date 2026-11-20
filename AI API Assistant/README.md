# Week 3 — AI API Assistant

## Overview

This week explores how to use generative AI APIs from Python to build practical assistants for different tasks.

The projects use Google's Gemini API to interpret natural-language input, generate responses, extract structured information, and call external tools or services where appropriate.

## Projects

### 1. [Matatu Assistant](1%20-%20Matatu%20Assistant/README.md)

A command-line prototype for a matatu SACCO. It uses Gemini to interpret member questions and respond using sample information about balances, meetings, and membership fees.

The current version uses fixed demonstration data; it does not connect to a live SACCO database or retrieve real member accounts.

### 2. [Property Inquiry](2%20-%20Property%20Inquiry/README.md)

An AI-powered information extraction tool that processes property inquiries written in natural language, converts relevant details into structured fields, and saves the extracted information to Google Sheets.

### 3. [Pharmacy Chatbot](3%20-%20Pharmacy%20Chatbot/README.md)

A conversational assistant that answers common pharmacy-related questions using configured pharmacy information. It maintains context during an active chat session.

It does not access live inventory or replace a pharmacist's professional judgement.

### 4. [Tea Harvest Assistant](4%20-%20Tea%20Harvest%20Assistant/README.md)

An AI assistant that uses Gemini function calling to retrieve weather information from external APIs and provide weather-based tea-harvesting guidance.

The harvesting rules are initial guidelines and require validation against actual estate practices.

### 5. [AI Proposal Assistant](AI%20Proposal%20Assistant/README.md)

A web-based application that analyses client project briefs, identifies unclear requirements, estimates project effort, and generates structured freelance proposals.

It uses Python for deterministic pricing calculations based on a configurable pricing profile. Version 1.0 includes brief analysis and proposal generation; proposal review is planned for a later version.

## Shared setup

All Python projects in this specialization use the virtual environment and dependency file at the repository root.

Follow the [main repository README](../README.md) for environment setup and dependency installation.

Add your Gemini API key to the root `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Some projects require additional API credentials or service configuration. Refer to the individual project README before running them.

Do not create another virtual environment or install dependencies from a week-specific requirements file. Keep credentials and tokens out of version control.

## Concepts explored

- Calling generative AI APIs from Python
- Prompt and system-instruction design
- Natural-language understanding and structured extraction
- JSON response handling
- Gemini chat sessions and conversation context
- Function calling and external API integration
- Saving extracted information to Google Sheets
- Building a web interface with FastAPI and JavaScript
- Separating AI-generated reasoning from deterministic application logic
- Error handling and testing API-backed applications

## Development note

These are learning projects and prototypes, not production-ready systems. Each project README describes its current capabilities, setup requirements, and known limitations.
