# Email Processing API

A FastAPI-based service for generating and validating email addresses.

## Features

- Email pattern generation
- Email validation using ZeroBounce
- Catch-all email filtering
- REST API endpoints

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your actual API keys in `.env`

## Usage

1. Start the server:
```bash
uvicorn app:app --reload
```

2. Access the API:
- Health check: `GET http://localhost:8000/health`
- Process emails: `POST http://localhost:8000/process-emails`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Security

- Never commit your `.env` file
- Keep your API keys secure
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 