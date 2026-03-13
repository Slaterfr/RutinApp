# RutinApp - Personal Fitness Tracker & AI Coach API

RutinApp is a robust backend API designed to help users track their fitness journey, manage workout routines, and get personalized advice from an AI coach. Built with FastAPI and PostgreSQL, it offers a secure and scalable solution for fitness data management.

## Features

### Core Functionality
-   **User Management**: User registration, login, and profile management with JWT authentication.
-   **Routine Management**: Create, read, update, and delete workout routines with full CRUD operations.
-   **Sub-Routines**: Organize routines into specific training days (e.g., Push, Pull, Legs).
-   **Exercise Tracking**: Log and track exercise details including sets, reps, and weights.
-   **AI Fitness Coach**: Integrated **AI Chatbot** (powered by Groq-Llama) for real-time fitness advice via WebSocket.
-   **AI Analysis**: Analyze routines and get AI-powered recommendations. (Work in progress)

### Security & Architecture
-   **Secure Authentication**: JWT-based authentication protecting user data.
-   **CORS Enabled**: Cross-Origin Resource Sharing configured for API accessibility.
-   **Service Layer Pattern**: Clean separation of concerns with dedicated service classes.
-   **Error Handling**: Comprehensive error handling with custom exception handlers.

## Tech Stack

-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13)
-   **Database**: PostgreSQL 16
-   **ORM**: SQLAlchemy / SQLModel
-   **Authentication**: JWT (JSON Web Tokens)
-   **AI Integration**: Groq API (Llama 3.3)
-   **Containerization**: Docker & Docker Compose
-   **Real-time Communication**: WebSockets

## 📦 API Endpoints

The API includes the following router modules:
- `/routines` - Workout routine management
- `/users` - User management
- `/exercises` - Exercise tracking
- `/auth` - Authentication
- `/sub-routines` - Training day management
- `/bot` - AI chatbot WebSocket
- `/ai-analyze` - AI analysis and recommendations

## Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Or: Python 3.13+ and PostgreSQL 16

### Using Docker (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Slaterfr/RutinApp.git
    cd RutinApp/RutinApp
    ```

2.  **Environment Variables:**
    Create a `.env.docker` file:
    ```env
    DATABASE_URL=postgresql://...
    SECRET_KEY=your_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    GROQ_KEY=your_groq_api_key_here
    ```

3.  **Start the application:**
    ```bash
    docker compose up --build
    ```

4.  **Access the API:**
    - API Docs: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`
    - AI Bot: `ws://localhost:8000/ws`

### Local Development

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file with your PostgreSQL connection details.

4.  **Run migrations:**
    ```bash
    alembic upgrade head
    ```

5.  **Start the server:**
    ```bash
    fastapi dev
    ```

## Usage

-   **Interactive API Documentation**: Visit `http://localhost:8000/docs` for Swagger UI.
-   **Chat with AI Coach**: Connect to `ws://localhost:8000/ws` or use the web interface.
-   **View all endpoints**: Check the Swagger UI for detailed endpoint documentation.
