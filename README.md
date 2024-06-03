# Implementing a Load Balancer with Flask and Docker

## Introduction

This project demonstrates the implementation of a load balancer using consistent hashing with Python, Flask, and Docker. Consistent hashing is an efficient technique used to distribute data evenly across a cluster of servers, ensuring minimal disruption when servers are added or removed. This load balancer manages server replicas and routes requests to the appropriate server using consistent hashing.

## Requirements

- Docker Desktop
- Python 3.8+

## How to Run the Project

1. **Clone the Repository**

   Clone this repository to your local machine.

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment**

   Create and activate a virtual environment.

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements**

   Install the necessary Python packages.

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Application**

   Use Docker Compose to build and run the application.

   ```sh
   docker-compose up --build
   ```

   This will start the Flask application and an Nginx load balancer.

## API Endpoints

- **`GET /`**: Returns a simple homepage message.

- **`GET /home`**: Returns a greeting message from a specific server.

- **`GET /heartbeat`**: Checks if the server is alive.

- **`GET /rep`**: Returns the list of current server replicas.

## API Endpoints

- **`POST /add`**: Adds new server replicas.
  - Request body:
    ```json
    {
      "n": "<number_of_replicas>",
      "hostnames": "<list_of_hostnames>"
    }
    ```

- **`DELETE /rm`**: Removes existing server replicas.
  - Request body:
    ```json
    {
      "n": "<number_of_replicas>",
      "hostnames": "<list_of_hostnames>"
    }
    ```

- **`GET /<path>`**: Routes a request to a specific server based on the path.

## Conclusion

This project showcases the implementation of a load balancer using consistent hashing to distribute requests evenly across a cluster of servers. By using Flask for the web application and Docker for containerization, the project ensures easy deployment and management. The provided API endpoints allow dynamic management of server replicas, making it a robust solution for handling distributed requests in a scalable manner.