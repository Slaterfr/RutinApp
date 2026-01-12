# RutinApp

# RutinApp - Personal Fitness Tracker & AI Coach API

RutinApp is a robust backend API designed to help users track their fitness journey, manage workout routines, and get personalized advice from an AI coach. Built with FastAPI and PostgreSQL, it offers a secure and scalable solution for fitness data management.

## Features

-   **Workout Management**: Create, update, and track detailed workout routines.
-   **Granular Tracking**: Break down routines into specific training days (e.g., Push, Pull, Legs) and log exercise details like sets, reps, and weights.
-   **AI Fitness Coach**: Integrated **AI Chatbot** (powered by Llama 3.3 via Groq) accessible via WebSockets for real-time fitness advice and Q&A(Work in progress).
-   **Secure Authentication**: Full user signup/login system with JWT-based authentication to protect user data.
-   **Database Driven**: specific routines and user data are persisted using PostgreSQL and SQLModel.

## Tech Stack

-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy / SQLModel
-   **Authentication**: JWT (JSON Web Tokens) with `python-jose`
-   **AI Integration**: Groq API (Llama 3.3)
-   **Migration**: Alembic

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/RutinApp.git
    cd RutinApp
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the `RutinApp` directory and add your configuration:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/dbname
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    GROQ_KEY=your_groq_api_key
    ```

5.  **Run Migrations:**
    ```bash
    alembic upgrade head
    ```

## Usage

1.  **Start the server:**
    ```bash
    fastapi dev
    ```

2.  **Access the API Docs:**
    Go to `http://localhost:8000/docs` to see the interactive Swagger UI and test the endpoints.

3.  **Talk to the AI Coach:**
    Connect to the WebSocket endpoint at `ws://localhost:8000/ws` (or use the provided HTML UI at `http://localhost:8000/bot/`) to chat with the fitness coach.
