# Docker Compose Medical Text Extraction Service

This project demonstrates how to deploy a multi-container application using Docker Compose. In this project, an ML service is created where users can input medical prescription text, and the service processes the input using the OpenAI API, extracts structured data, and stores it in a PostgreSQL database. Here's the project overview:

1. **Frontend**: A Streamlit app for users to input prescription text.
2. **Backend**: A FastAPI app that handles the API endpoints and data processing.
3. **Database**: A PostgreSQL database that stores the structured data.


## Project Structure

```
docker-tutorial/3-text-extractor/
├── backend/
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── extraction.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── .env
├── docker-compose.yml
└── README.md
```

## Running with Docker

1. **Set Environment Variables:**

   Create a `.env` file in the project directory with the following environment variables:

   ```bash
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   POSTGRES_USER=YOUR_POSTGRES_USER_NAME
   POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
   POSTGRES_DB=YOUR_POSTGRES_DATABASE_NAME
   ```

2. **Build and run the Docker Containers:**

   Navigate to the project directory and run:

   ```bash
   cd 3-text-extractor
   docker compose up --build -d
   ```

   > Note: You must be in the same directory as the `docker-compose.yml` file.

   This single command will build and start up all the containers: the frontend app, backend APIs, and PostgreSQL database


## Accessing the Application

1. **Frontend:**
   - Open your browser and go to `http://localhost:8501` to access the Streamlit frontend.
   - Enter natural language text and click **Process Text** to extract structured data.

2. **Backend:**
   - The backend API will be running on `http://localhost:8000` and is responsible for handling requests and processing data using OpenAI.
   
3. **PostgreSQL Database:**
   - The database is running in the `postgres` container.
   - You can connect to it with your preferred Postgres client using `localhost:5432` and the credentials defined in the `.env` file.


## Checking Container Status

To check if your containers are running, use the following command:

```bash
docker ps
```

To check docker compose logs in real-time:
```bash
docker compose logs -f
```

To access the shell of a specific container, use:

```bash
docker exec -it <container_id_or_name> bash
```

For example, to enter the backend container, you can run:

```bash
docker exec -it 3-text-extraction-backend_api-1 bash
```


## Cleaning Up

To stop and remove the containers:

```bash
docker-compose down
```

To remove all images associated with this project:

```bash
docker-compose down --rmi all
```
