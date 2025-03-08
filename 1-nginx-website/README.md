# Docker Basic Nginx Website

This project demonstrates how to setup a basic pre-built docker container. For this project, Nginx docker image used to host a static website. Here's the project overview:

1. Create a static website with HTML/CSS
2. Use the official Nginx Docker image from Docker Hub
3. Serve the static website using Docker and Nginx

## Project Structure

```
docker-tutorial/1-nginx-website/
├── website/
│   ├── index.html
│   ├── styles.css
│   └── images/
└── README.md
```

## Running with Docker

### 1. Pull the Nginx Docker Image

Pull the official Nginx image from Docker Hub:

```bash
cd 1-nginx-website
docker pull nginx:latest
```

### 2. Run the Nginx Container

Navigate to your project directory and run the following command:

```bash
docker run --name nginx-website \
  -v $(pwd)/website:/usr/share/nginx/html \
  -p 8080:80 \
  -d nginx
```

This command:

- Names the container `nginx-website`
- Maps the local `website` directory to Nginx's HTML directory in the container
- Maps port 8080 on your host to port 80 in the container
- Runs the container in detached mode

## Accessing the Website

Open your web browser and navigate to:

```
http://localhost:8080/index.html
```

You should see the website in your browser which is running locally and if you have a domain you can also host it from your computer and anyone can access it!

## Checking Container Status

To check if your container is running:

```bash
docker ps
```

To view container logs:

```bash
docker logs nginx-website
```

## Cleaning Up

To stop the Nginx container:

```bash
docker stop nginx-website
```

To remove the container:

```bash
docker rm nginx-website
```

To remove the Nginx image:

```bash
docker rmi nginx
```
