# Loan Management Audit System

## Project Overview
This is a robust **Loan Management System (LOS)** backend designed with a primary focus on **Auditability** and **Activity Logging**. 

Unlike standard CRUD applications, this system implements a high-fidelity **"Who did What"** tracking engine. It is architected as a **modular component** ready to be plugged into a larger enterprise ecosystem, particularly designed to integrate seamlessly with an external Authentication/SSO provider.

## System Architecture

The project follows a strict **3-Layer Architecture** to ensure maintainability and testability:
1.  **Router Layer (API)**: Handles HTTP requests, validation, and response formatting.
2.  **Service Layer (Business Logic)**: Enforces business rules and orchestrates data flow.
3.  **Repository Layer (Data Access)**: Abstraction over raw database queries.

### Key Components

#### 1.Audit System (Event-Driven)
*   **Mechanism**: Uses SQLAlchemy Event Listeners (`after_flush`) to intercept **every** database change.
*   **Capabilities**:
    *   Automatically captures `INSERT`, `UPDATE`, and `DELETE` operations.
    *   Records **Snapshots**: Stores the exact state of data `before` and `after` the change.
    *   **Zero-Touch**: Developers do not need to write manual audit code; the system handles it automatically at the ORM level.

#### 2.Activity Logging (Middleware)
*   **Mechanism**: `ActivityLoggerMiddleware` intercepts every incoming HTTP request and outgoing response.
*   **Capabilities**:
    *   Logs endpoint access, IP addresses, and HTTP methods.
    *   **PII Protection**: Automatically detects and **encrypts sensitive fields** (like passwords, customer names) before storing logs to ensure GDPR/Compliance.
    *   *Configuration*: Define sensitive fields in [`app/constants/secure_fields.py`](app/constants/secure_fields.py).

---

## Key Architectural Decision: User Identity Management

### *"Why is `user_id` passed as a dependency?"*

You may notice that the system currently extracts `user_id` from request parameters. **This is a deliberate architectural choice to support "Plug-and-Play" Integration.**

In a distributed microservices environment, Authentication (AuthN) is often handled by a dedicated Gateway or Auth Service (e.g., Auth0, Keycloak). This backend is designed to be **Auth-Agnostic**.

*   **Current State (Standalone Mode)**: It accepts `user_id` allowing for easy testing and independent operation.
*   **Integration Ready**: The system treats User Identity as an injected dependency.
    *   **Merge Strategy**: When merging with the main Auth System, you simply point the dependency injector to the validated JWT token (`request.state.user.id`).
    *   **Benefit**: This decouples the Audit Logic from the Auth Logic. You can swap authentication providers without rewriting a single line of the Audit or Business logic.

---

## Tech Stack

*   **Framework**: FastAPI (High performance, async support)
*   **Language**: Python 3.14+
*   **Database**: PostgreSQL / SQLite (via SQLModel & SQLAlchemy)
*   **Security**: Cryptography (Fernet) for PII Encryption
*   **Validation**: Pydantic v2

## Installation & Setup

1.  **Clone the repository**
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Setup**:
    Create a `.env` file (facultative for dev, required for prod):
    ```ini
    DATABASE_URL=postgresql://user:pass@localhost:5432/db
    ENUM_ENCRYPTION_KEY=... # Optional (Auto-generated if missing)
    ```
4.  **Run the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Project Structure

```
app/
├── core/               # Config & Logger setup
├── middleware/         # Activity Logging Middleware
├── models/             # Database Models (Audit, Loan, Activity)
├── routers/            # API Endpoints
├── repositories/       # DB Access Layer
├── services/           # Business Logic
└── utils/              # Encryption & Helper functions
```


