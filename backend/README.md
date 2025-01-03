# Backend

# Table of Contents

# Technologies

# Development

Aura.ai's backend exposes a RESTful API that is developed using FastAPI, that is leveraged by the frontend for querying. It is advisable to use Docker for working with the backend, and if it's to be used along with the frontend, it's recommended to use Docker compose for easier development.

## Pre-requisites

1. [**Python:**](https://www.python.org/) Used for development of backend with FastAPI. Installing Python usually ensures installation of `pip`, which can be used for package management.
2. [**Docker:**](https://www.docker.com/) (optional) Supports containerization of backend for easier deployment.

## Steps

### Manual

1. Ensure you have Python, pip and Docker (optional) on your system:

```shell
python --version
pip --version
docker -v
```

2. Install the needed dependencies for the project after cloning the project and setting a virtual environment by the following command:

```shell
git clone https://github.com/arunpranav-at/aura.ai
cd aura.ai/backend
python -m venv .venv

# For Linux
source .venv/bin/activate

# For Windows
.venv\\Scripts\\Activate.ps1
```

3. Configure the needed environment variables as per `.env.sample` file. Generate a secret for JWT to be stored under `JWT_SECRET` environment variable.

4. Start the development server with the following command:

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 --certfile='../certs/cert.pem' --keyfile='../certs/key.pem' -b localhost:8000 server:app
```

The backend should be accessible at [https://localhost:8000](https://localhost:8000)

### Docker

1. Build a Docker image with the following command after configuring the necessary environment variables (assuming you're using `aura.ai/backend` as the working directory):

```shell
docker build -t aura-ai-backend:latest .
```

2. Run the image with the following command:
```shell
docker run --network host aura-ai-backend:latest 
```

The backend should be accessible at [http://localhost:8000](http://localhost:8000)