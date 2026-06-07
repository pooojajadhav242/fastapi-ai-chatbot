# FastAPI AI Chatbot

A secure AI-powered chatbot backend built using FastAPI, SQLAlchemy, SQLite, JWT Authentication, User Management, Chat History, Conversation Memory, and Google Gemini AI.

This project demonstrates authentication, authorization, database integration, AI integration, chat persistence, and clean project architecture using modern backend development practices.

---

## Features

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
* Chat History Retrieval
* Delete Single Chat
* Delete All Chats
* SQLite Database Integration
* Secure API Access using Bearer Token
* Route-based Project Structure

---

## Tech Stack

* FastAPI
* Python
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Google Gemini AI
* Git & GitHub

---

## Project Structure

```text
fastapi-ai-chatbot/
│
├── main.py
├── models.py
├── database.py
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

## API Endpoints

### Authentication APIs

| Method | Endpoint   | Description                  |
| ------ | ---------- | ---------------------------- |
| POST   | /register  | Register a new user          |
| POST   | /login     | Login and generate JWT token |
| GET    | /protected | Verify JWT token             |

### Chat APIs

| Method | Endpoint                | Description           |
| ------ | ----------------------- | --------------------- |
| POST   | /ask-ai                 | Ask Gemini AI         |
| GET    | /chat-history           | Get user chat history |
| DELETE | /chat-history/{chat_id} | Delete a single chat  |
| DELETE | /chat-history           | Delete all chats      |

---

## Database Models

### User

| Field    | Type    |
| -------- | ------- |
| id       | Integer |
| username | String  |
| email    | String  |
| password | String  |

### ChatMessage

| Field   | Type        |
| ------- | ----------- |
| id      | Integer     |
| user_id | Foreign Key |
| role    | String      |
| message | Text        |

---

## Authentication Flow

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
        ↓
Ask Gemini AI
```

---

## AI Chat Flow

```text
User Question
      ↓
JWT Verification
      ↓
Load Previous Chat History
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

## Security Features

* Password Hashing
* JWT Authentication
* Protected API Endpoints
* Input Validation
* Email Validation
* Strong Password Validation
* User Isolation using JWT

---

## Current Progress

* [x] User Registration
* [x] Password Hashing
* [x] Email Validation
* [x] Username Validation
* [x] Password Policy Validation
* [x] User Login
* [x] JWT Authentication
* [x] Protected Routes
* [x] Gemini AI Integration
* [x] User-specific Chat Storage
* [x] Chat History Retrieval API
* [x] Conversation Memory
* [x] Delete Single Chat
* [x] Delete All Chats
* [ ] Multiple Chat Sessions
* [ ] Google Login
* [ ] Refresh Tokens
* [ ] Role-Based Authorization
* [ ] Docker Support
* [ ] Deployment

---

## Future Enhancements

* Multiple Chat Sessions
* PDF Upload & Document Chat
* Image Upload & Analysis
* Refresh Tokens
* Google OAuth Login
* Role-Based Access Control (RBAC)
* Docker Containerization
* AWS/GCP Deployment
* Rate Limiting
* Admin Dashboard

---

## Getting Started

### Clone Repository

```bash
git clone https://github.com/pooojajadhav242/fastapi-ai-chatbot.git
cd fastapi-ai-chatbot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment Variables

```env
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

### Run Application

```bash
uvicorn main:app --reload
```

### Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

## Author

**Pooja Shewale**

AI Engineer | FastAPI Developer | Machine Learning Enthusiast
