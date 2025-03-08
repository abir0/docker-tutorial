# Docker Custom Build PDF Generator

This project demonstrates how to build and run a custom docker container using `Dockerfile`. For this project, a PDF Generator app is created and run using Python and ReportLab library. Here's the project overview:

1. Create the Python app, requirements, and mock data
2. Create a `Dockerfile` with the custom setup commands
3. Build the image from the Dockerfile and run it in a container


## Project Structure

```
docker-tutorial/2-pdf-generator/
├── data/
│   └── report_data.json    # Demo data (JSON format)
├── generated_pdfs/         # Directory to store generated PDFs (using Docker volumes)
├── app.py                  # Python application to generate PDFs
├── Dockerfile              # Dockerfile to containerize the app
├── requirements.txt        # Python dependencies
└── README.md
```


## Running with Docker

1. **Build the Docker Image:**

   ```bash
   cd 2-pdf-generator
   docker build -t pdf-generator .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run --rm -v $(pwd)/generated_pdfs:/app/generated_pdfs pdf-generator
   ```

This will mount the `generated_pdfs` directory from your local machine to the container and generate the PDFs inside the folder.


## Checking Container Status

To check if your container is running:

```bash
docker ps
```


## Cleaning Up

To remove the container:

```bash
docker rm <CONTAINER_ID>
```

To remove the pdf-generator image:

```bash
docker rmi pdf-generator
```
