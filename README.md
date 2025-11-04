# EGL-backend

This is the backend service for EGL Budget Managament application built using:
- ⚡ FastAPI


## 🚀 Getting Started (Local Dev)

### Prerequisites
- python3

### Steps

#### 1. Clone the Repo

```bash
git clone https://github.com/Velu-profile/EGL-backend.git
```

#### 2. Create and Activate a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Setup the environment variables

```bash
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
SUPABASE_JWT_SECRET=
```

#### 5. Run the Backend Server

```bash
uvicorn app.main:app --reload
```

Server will run at: [http://127.0.0.1:8000](http://127.0.0.1:8000)