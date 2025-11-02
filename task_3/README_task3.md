# AgroBot – Universal AI Agricultural Assistant

## Overview
This project is a web-based agriculture chatbot that helps users get farming-related information in multiple languages. Users can create an account, log in, and chat with the assistant to ask questions related to crops, soil, fertilizers, pests, and harvesting. All chats are stored for each user.
This version includes an **Admin Dashboard** that allows the admin to monitor and manage users and their chat history easily.

## Features
- User registration, login, and logout with secure authentication
- Chat interface to interact with the agriculture chatbot
- Offline knowledge base for farming guidance
- Uses OpenAI only when offline knowledge doesn’t have an answer
- Multi‑language responses based on user preference
- Chat history stored per user in SQLite
- **Admin Dashboard to view and manage users and chats**

## Key Components and Files

### app.py
- Contains all route handling for user login, signup, logout, chat, and admin panel
- Stores each chat into the database
- Includes admin‑only features for monitoring users and chat history

### database.py
- Defines SQLAlchemy models: **User** and **ChatHistory**
- Stores user profile, language preference, and chat records
- Auto‑creates a default admin account on first run

### chatbot_model.py
- Detects user language and provides farming‑related answers
- Checks offline knowledge base first before using GPT
- Supports multilingual responses for better user experience

### translator_util.py
- Handles language detection and translation for chatbot responses

### Admin Dashboard
- Admin‑only webpage to view all users and their chat history
- Helps track usage and manage the platform effectively
