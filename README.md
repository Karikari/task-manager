# Beckend Test Task Manager API
---
## 🚀 **Setup & Run the Project**

### Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
---

### Clone the Repository

[git clone git@github.com:Karikari/task-manager.git](git clone git@github.com:Karikari/task-manager.git)

```bash
cd task-manager
```

## Running the API

#### Inside the task-manager run the docker-compose.yml

```bash
  docker-compose --env-file=.env.prod up --build -d
```

#### Confirm if docker is running

```bash
  docker ps
```

### Run Migrations

makemigrations

```bash
  docker exec task-manager-api python3 manager.py makemigrations

```

migrate

```bash
  docker exec task-manager-api python3 manager.py migrate
```

Create Super User

```bash
  docker exec task-manager-api python3 manager.py createsuperuser
```

Running Test

```bash
  docker exec task-manager-api python3 manager.py test
```
#### Open Documentation

[Api Documentation ](http://localhost:8000/docs)

#### Go to Admin

[Admin Portal](http://localhost:8000/admin)


#### Postman Collection can be found in the repository
