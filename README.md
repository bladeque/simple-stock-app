# A simple stock quote app

## Architecture
The architecture consists in the backend and frontend parts.

## Backend
Django 2.0 + DRF based solution utilizing Celery (off request/response cycle computation) 
and Redis (caching). Dockerized.

### Prerequisites

You’ll need at least Docker 1.10.

Add the Alpha Vantage API key in `backend/.envs/.local/.django` 
(`ALPHA_VANTAGE_API_KEY` variable).

### Build the stack

```sh
$ cd backend
$ docker-compose -f local.yml build
```

### Boot the system

```sh
$ docker-compose -f local.yml up
```

## Frontend
React 16 + Bootstrap 4

### Install React dependencies

```sh
$ cd frontend
$ npm install
```

### Run the Webpack Development server
```sh
$ npm start
```

## Future improvements

A few things I had _not enough time_ to add:
* write **tests** (!)
* add API documentation (e.g. Swagger)
* implement automatic refresh of a current quote - this can be achieved for example 
by polling an API endpoint in time intervals or using Django Channels + WebSockets. 
