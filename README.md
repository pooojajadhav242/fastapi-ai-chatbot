# FastAPI AI Chatbot

A secure AI-powered chatbot backend built using FastAPI, SQLAlchemy, SQLite, JWT Authentication, User Management, and Google Gemini AI.

This project demonstrates authentication, authorization, database integration, AI integration, and chat persistence using modern backend development practices.

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
* SQLite Database Integration
* Secure API Access using Bearer Token

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

### AI APIs

| Method | Endpoint | Description                     |
| ------ | -------- | ------------------------------- |
| POST   | /ask-ai  | Ask Gemini AI (Protected Route) |

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
Gemini AI
      ↓
Store Chat Message
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
* [ ] Chat History Retrieval API
* [ ] Conversation Memory
* [ ] Google Login
* [ ] Refresh Tokens
* [ ] Role-Based Authorization
* [ ] Docker Support
* [ ] Deployment

---

## Future Enhancements

* Chat History API
* Conversation Memory
* Multiple Chat Sessions
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

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
JWT_SECRET_KEY=your_secret_key_here
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
