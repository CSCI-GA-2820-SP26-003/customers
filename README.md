# Customers Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![CI Build](https://github.com/CSCI-GA-2820-SP26-003/customers/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/CSCI-GA-2820-SP26-003/customers/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP26-003/customers/graph/badge.svg?token=ZHS21LAGLP)](https://codecov.io/gh/CSCI-GA-2820-SP26-003/customers)

## Overview

The Customers service is a RESTful API that maintains a list of customers and their details for an e-commerce application. This is a part of the Project for the Spring 2026 NYU DevOps Course.

## Setup

### Prerequisites
- Docker
- Visual Studio Code with the Dev Containers extension

### Manual Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Getting Started
1. Clone the repository and open it in Visual Studio Code.
2. Click the Reopen in Container when prompted or select the Dev Containers: Reopen in Container option
3. Initialize the database:
   ```shell
    flask db-create
   ```
4. Start the service:
   ```shell
   make run
   ```
   The service will be available at http://localhost:8080

## UI

The service includes a customer administration UI scaffold that is served by Flask.

- UI page: http://localhost:8080/ui
- Root endpoint: http://localhost:8080/
- Health endpoint: http://localhost:8080/health

The UI supports the following wired operations:
- **Create** — POST /customers
- **Retrieve by ID** — GET /customers/{id}, populates the form and results table

The remaining controls (update, delete, list, search, suspend, activate) are scaffolded but not yet wired to API calls.

## Kubernetes Deployment

This repository includes Kubernetes manifests for both the Customers service and a PostgreSQL database.

### Kubernetes Resources

- `k8s/deployment.yaml` deploys the Customers service
- `k8s/service.yaml` exposes the Customers pod internally in the cluster
- `k8s/ingress.yaml` exposes the application through the cluster ingress
- `k8s/postgres/statefulset.yaml` deploys PostgreSQL as a StatefulSet
- `k8s/postgres/service.yaml` provides stable network identity for PostgreSQL
- `k8s/postgres/secret.yaml` stores the database credentials and application database URI

### Local Kubernetes Workflow

Use the following commands to build and deploy the application in the local development environment:

```shell
make cluster
make deploy
```

`make cluster` creates the k3d cluster (or reuses it if it already exists) and automatically configures `kubectl` to point at it. `make deploy` builds the image, imports it into the cluster, and applies all Kubernetes manifests.

After deployment, the application is reachable at:

```text
http://localhost:8080/
http://localhost:8080/health
http://localhost:8080/ui
```

## Running Tests

### Unit Tests

```shell
make test
```

Runs the full pytest suite with coverage reporting. Coverage must be ≥ 95% to pass.

```shell
make lint
```

Runs `flake8` and `pylint` on `service/` and `tests/`.

### BDD / Integration Tests (Behave + Selenium)

BDD tests use Selenium with a headless Chromium browser and require the service to be running and reachable.

#### One-time setup

If `behave` is not found, install all dev dependencies:

```shell
make install
```

> **Note:** Chromium is pre-installed in the dev container image. No manual browser setup is needed.

#### Option A — Run against a local service

Open two terminals:

**Terminal 1 — start the service:**
```shell
make run
```

**Terminal 2 — run BDD tests:**
```shell
BASE_URL=http://localhost:8080 behave
```

#### Option B — Run against the Kubernetes cluster

Deploy first, then run tests:

```shell
make deploy
BASE_URL=http://localhost:8080 behave
```

#### Running a single scenario

```shell
BASE_URL=http://localhost:8080 behave features/customers.feature --name "Read a Customer"
```

## API Reference

Service-level endpoints:

| Method | URL | Description |
|---|---|---|
| GET | `/` | Returns service metadata |
| GET | `/health` | Returns service health status |
| GET | `/ui` | Returns the customer administration UI page |

Customer resource endpoints are under the base path `/customers`

### Service Info

| Method | URL | Description |
|---|---|---|
| POST | `/customers` | Creates a customer. Required fields `name, address` |
| GET | `/customers` | Lists all customers |
| GET | `/customers?name={name}` | Queries customers by name |
| GET | `/customers/{id}` | Retrieves a single customer's details |
| PUT | `/customers/{id}` | Updates a single customer's details |
| PUT | `/customers/{id}/suspend` | Sets customer status to `suspended` |
| PUT | `/customers/{id}/activate` | Sets customer status to `active` |
| DELETE | `/customers/{id}` | Deletes a single customer's details |
   
## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
├── static                 - CSS and JavaScript assets for the UI
├── templates              - HTML templates rendered by Flask
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

k8s/                       - Kubernetes manifests for app deployment
├── deployment.yaml        - Customers service deployment
├── service.yaml           - Customers service definition
├── ingress.yaml           - Ingress for external access
└── postgres/              - PostgreSQL manifests
    ├── secret.yaml        - Database secrets
    ├── service.yaml       - Headless service for PostgreSQL
    └── statefulset.yaml   - PostgreSQL StatefulSet

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
