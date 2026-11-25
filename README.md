# AI Document Assistant

An AI-powered document assistant built with **Python** and **FastAPI**.
It supports general question answering and PDF-based question answering
using Google's Gemini API.

The application is containerized with Docker and deployed on **AWS EC2**
through an automated **GitHub Actions CI/CD pipeline**.

## Features

-   Ask general questions and receive AI-generated responses.
-   Upload PDF documents.
-   Extract PDF text using PyMuPDF.
-   Ask questions based on the content of uploaded PDFs.
-   Explore the REST API through FastAPI Swagger UI.
-   Build, publish, and deploy Docker images through CI/CD.

## Technology Stack

  Area                 Technologies
  -------------------- ------------------------------------------------
  Language and API     Python, FastAPI
  AI integration       Google Gemini API (`gemini-3.5-flash-lite`)
  PDF processing       PyMuPDF
  Containerization     Docker
  Container registry   GitHub Container Registry (GHCR)
  AWS services         Amazon EC2, AWS IAM, AWS Systems Manager (SSM)
  CI/CD                GitHub Actions, GitHub OIDC

## How It Works

1.  A client sends a request to the FastAPI backend.
2.  For general questions, the backend sends the question to Google's
    Gemini API and returns the generated answer.
3.  For PDF workflows, the backend accepts a PDF and extracts its text
    using PyMuPDF.
4.  The extracted text is used as context when answering
    document-related questions with Gemini.
5.  The API returns the response to the client.

## API Endpoints

  Method   Endpoint        Purpose
  -------- --------------- ----------------------------------
  `GET`    `/`             Home endpoint
  `GET`    `/health`       Application health check
  `POST`   `/ask`          Ask a general question
  `POST`   `/upload-pdf`   Upload a PDF document
  `POST`   `/ask-pdf`      Ask a question about PDF content

Visit `/docs` on the running application to inspect request parameters
and response schemas.

## Run Locally

### Prerequisites

-   Python 3.12 or later
-   Google Gemini API key
-   Git

### 1. Clone the repository

``` bash
git clone https://github.com/faridhaiderkhanjoya/ai-document-assistant.git
cd ai-document-assistant
```

### 2. Create and activate a virtual environment

``` bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
```

### 3. Install dependencies

``` bash
cd backend
pip install -r requirements.txt
```

### 4. Configure the API key

Create `backend/.env`:

``` env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own Gemini API key. Never commit
`.env` or expose the key publicly.

### 5. Start the API

From the `backend/` directory:

``` bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

-   Swagger UI: `http://localhost:8000/docs`
-   Health check: `http://localhost:8000/health`

## Run with Docker

Build the image from the `backend/` directory:

``` bash
docker build -t ai-document-assistant .
```

Run the container, passing the environment file securely:

``` bash
docker run -d \
  --name ai-document-assistant \
  --restart unless-stopped \
  --env-file .env \
  -p 8000:8000 \
  ai-document-assistant
```

Check the container and application:

``` bash
docker ps
curl http://localhost:8000/health
```

Open `http://localhost:8000/docs` to explore the API.

## CI/CD Pipeline

GitHub Actions automates delivery when changes are pushed to the `main`
branch.

### 1. Validate Backend

-   Install dependencies.
-   Compile-check the Python application.
-   Run Ruff linting.
-   Run dependency security auditing with `pip-audit`.
-   Execute automated tests with `pytest`.

### 2. Build and Push Docker Image

-   Build the Docker image.
-   Authenticate to GitHub Container Registry.
-   Publish the `latest` image and a commit-specific image tag.

### 3. Deploy to AWS EC2

-   Authenticate to AWS using GitHub OIDC and an IAM role.
-   Use AWS Systems Manager to execute deployment commands on EC2.
-   Pull the latest image from GHCR.
-   Replace the running container.
-   Run health checks and attempt rollback if the new deployment is
    unhealthy.

This workflow reduces manual deployment steps and makes releases more
repeatable.

## AWS Services Used

-   **Amazon EC2:** Hosts the Dockerized FastAPI application.
-   **AWS IAM:** Manages permissions for the EC2 instance and GitHub
    Actions deployment role.
-   **AWS Systems Manager (SSM):** Executes deployment commands on EC2
    without requiring the CI/CD workflow to connect over SSH.

GitHub Actions and GitHub Container Registry are GitHub services, not
AWS services.

## Security Practices

-   The Gemini API key is supplied through an environment variable and
    is not built into the Docker image.
-   Keep `.env` files out of version control and exclude secrets from
    the Docker build context.
-   GitHub Actions uses OIDC to assume an AWS IAM role instead of
    storing long-lived AWS access keys for deployment.
-   Restrict EC2 Security Group inbound rules to trusted source IP
    addresses and only the required ports.
-   Never publish API keys, private SSH keys, AWS credentials, or
    sensitive environment files.

## Deployment Notes

The application runs on an EC2 instance and is exposed on port `8000`.
An automatically assigned public IPv4 address can change after an EC2
stop/start cycle. An Elastic IP can provide a persistent public IPv4
address; review AWS pricing before allocating one.

The Docker container uses the `unless-stopped` restart policy, allowing
Docker to restart it when the EC2 instance boots, provided the container
was not manually stopped.

## Skills Practiced

-   Python and FastAPI REST API development
-   Gemini API integration
-   PDF text extraction
-   Docker image creation and container management
-   GitHub Container Registry
-   AWS EC2, IAM, and Systems Manager
-   GitHub Actions CI/CD
-   OIDC-based AWS authentication
-   Automated testing and dependency security auditing
-   Cloud networking and deployment troubleshooting

## Future Improvements

-   Add a frontend interface.
-   Add authentication and authorization.
-   Add stronger file validation and upload limits.
-   Improve document storage and retrieval for larger workloads.
-   Add structured logging, metrics, and monitoring.
-   Expand automated integration testing.

## Author

**Farid Haider**

-   GitHub: https://github.com/faridhaiderkhanjoya
-   Project repository:
    https://github.com/faridhaiderkhanjoya/ai-document-assistant

------------------------------------------------------------------------

*Built as a hands-on project to apply Python, AI integration, Docker,
AWS, and CI/CD concepts in a practical deployment workflow.*
