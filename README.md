# 📚 Bookstore REST API

A simple REST API for managing a bookstore inventory, built with **FastAPI** and **SQLite**.  
This project was developed as part of my internship project submission.  

---

## 🚀 Features
- Create, Read, Update, Delete (CRUD) books
- Search books by title
- Auto-loads sample books at startup
- SQLite database with SQLAlchemy ORM
- Swagger UI & ReDoc API documentation
- Postman collection included for testing

---

## 🛠️ Tech Stack
- **FastAPI** (Python web framework)  
- **SQLite** (lightweight relational database)  
- **SQLAlchemy** (ORM for database operations)  
- **Uvicorn** (ASGI server)  
- **Postman** (API testing tool)  

---

## 📂 Project Structure
bookstore-api/
│── main.py # FastAPI app & API routes
│── models.py # Database schema (Book model)
│── database.py # Database connection setup
│── requirements.txt # Project dependencies
│── bookstore.db # SQLite DB (auto-created on first run)
│── BookstoreAPI.postman_collection.json # Postman test collection
│── README.md # Project documentation
│── .gitignore
---

---

