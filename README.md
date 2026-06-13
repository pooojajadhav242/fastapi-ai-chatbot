# FastAPI AI Chatbot

A secure AI-powered chatbot backend built using FastAPI, SQLAlchemy, SQLite, JWT Authentication, Multi-Session Conversations, Chat History Management, and Google Gemini AI.

This project demonstrates authentication, authorization, AI integration, conversation memory, chat persistence, database relationships, and modern backend development practices.

---

# Features

* User Registration
* User Login
* Password Hashing
* Email Validation
* Username Validation
* Password Policy Validation
* JWT Authentication
* Protected Routes
* Google Gemini AI Integration
* User-specific Chat Storage
* Conversation Memory
* Multi-Session Conversations
* Create Conversation
* Update Conversation
* Delete Conversation
* List Conversations
* Chat History Retrieval
* Delete Single Chat Message
* Cascade Delete Support
* SQLite Database Integration
* Secure API Access using Bearer Token
* Route-based Project Structure

---

# Tech Stack

* FastAPI
* Python
* SQLAlchemy ORM
* SQLite
* Pydantic
* JWT Authentication
* Google Gemini AI
* Passlib
* Git & GitHub

---

# Project Structure

```text
fastapi-ai-chatbot/
│
├── main.py
├── database.py
├── models.py
├── auth.py
├── ai_service.py
├── schemas.py
│
├── routes/
│   ├── auth_routes.py
│   └── chat_routes.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# API Endpoints

## Authentication APIs

| Method | Endpoint   | Description                  |
| ------ | ---------- | ---------------------------- |
| POST   | /register  | Register a new user          |
| POST   | /login     | Login and generate JWT token |
| GET    | /protected | Verify JWT token             |

---

## Conversation APIs

| Method | Endpoint                        | Description               |
| ------ | ------------------------------- | ------------------------- |
| POST   | /conversation                   | Create a conversation     |
| GET    | /conversations                  | Get all conversations     |
| GET    | /conversation/{conversation_id} | Get conversation details  |
| PUT    | /conversation/{conversation_id} | Update conversation title |
| DELETE | /conversation/{conversation_id} | Delete conversation       |

---

## Chat APIs

| Method | Endpoint                        | Description               |
| ------ | ------------------------------- | ------------------------- |
| POST   | /ask-ai                         | Ask Gemini AI             |
| GET    | /chat-history/{conversation_id} | Get conversation messages |
| DELETE | /chat-history/{chat_id}         | Delete a single message   |

---

# Database Models

## User

| Field    | Type    |
| -------- | ------- |
| id       | Integer |
| username | String  |
| email    | String  |
| password | String  |

---

## Conversation

| Field   | Type        |
| ------- | ----------- |
| id      | Integer     |
| title   | String      |
| user_id | Foreign Key |

---

## ChatMessage

| Field           | Type        |
| --------------- | ----------- |
| id              | Integer     |
| conversation_id | Foreign Key |
| user_id         | Foreign Key |
| role            | String      |
| message         | Text        |

---

# Authentication Flow

```text
User Registration
        ↓
Store Hashed Password
        ↓
User Login
        ↓
Generate JWT Token
        ↓
Access Protected APIs
```

---

# AI Chat Flow

```text
User Question
      ↓
JWT Verification
      ↓
Validate Conversation
      ↓
Load Previous Messages
      ↓
Build Conversation Context
      ↓
Gemini AI
      ↓
Store User Message
      ↓
Store AI Response
      ↓
Return Response
```

---

# Database Relationships

```text
User
 │
 └── Conversation
        │
        └── ChatMessage
```

Conversation deletion automatically removes related chat messages using SQLAlchemy Cascade Delete.

---

# Security Features

* Password Hashing
* JWT Authentication
* Protected API Endpoints
* Input Validation
* Email Validation
* Username Validation
* Strong Password Validation
* User Isolation using JWT

---

# Current Progress

* [x] User Registration
* [x] User Login
* [x] Password Hashing
* [x] JWT Authentication
* [x] Protected Routes
* [x] Gemini AI Integration
* [x] Conversation Management
* [x] Multi-Session Conversations
* [x] Chat History
* [x] Delete Chat Message
* [x] Delete Conversation
* [x] Cascade Delete
* [x] Database Relationships

---

# Future Enhancements

* Auto Conversation Title Generation
* PDF Upload & Document Chat
* Image Upload & Analysis
* Google OAuth Login
* Refresh Tokens
* Role-Based Access Control (RBAC)
* Rate Limiting
* Docker Support
* PostgreSQL Migration
* AWS / GCP Deployment
* Admin Dashboard

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/pooojajadhav242/fastapi-ai-chatbot.git
cd fastapi-ai-chatbot
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

```env
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

## Run Application

```bash
uvicorn main:app --reload
```

## Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

# Author

**Pooja Shewale**

AI Engineer | FastAPI Developer | Machine Learning Enthusiast
