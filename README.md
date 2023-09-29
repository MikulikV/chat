# Chat with CBN

Chat with CBN Assistant.

## Table of Contents

- [Backend](#backend)
- [Frontend](#frontend)
- [Installation](#installation)
- [Usage](#usage)

## Backend

The `backend` folder contains the backend components of the project.

### Files

- `requirements.txt`: This file contains a list of Python packages required for the backend. You can install these packages using `pip install -r requirements.txt`.
- `config.py`: This configuration file stores sensitive information and application settings. It is used to configure the backend server (`server.py`) with necessary credentials and parameters.
- `server.py`: This file contains the backend server code.

## Frontend

The `frontend` folder contains the frontend React.JS components of the project.

## Installation

### 1. Backend setup

```bash
# Virtual Environment Setup
cd backend
python -m venv .venv

# Activate the virtual environment
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Frontend setup

```bash
cd frontend

# Install required packages
npm install
```

## Usage

### Set Environment Variables:

Create a `.env` file in the backend folder. Add your API keys and environment variables in the following format:

```plaintext
OPENAI_API_KEY=<your_openai_api_key>
PINECONE_API_KEY=<your_pinecone_api_key>
PINECONE_ENV=<your_pinecone_environment>
```

### Start the Backend Server:

```bash
cd backend

# Inside the backend folder
python server.py
```

Access the Server:
Open your browser and visit http://127.0.0.1:8080/

### Start the Frontend App:

```bash
cd frontend

# Inside the frontend folder
npm start
# or
yarn start
```

Access the App:
Open your browser and visit http://localhost:3000 to use the app.
