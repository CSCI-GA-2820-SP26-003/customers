# Customers Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![CI Build](https://github.com/CSCI-GA-2820-SP26-003/customers/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/CSCI-GA-2820-SP26-003/customers/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP26-003/customers/graph/badge.svg?token=ZHS21LAGLP)](https://codecov.io/gh/CSCI-GA-2820-SP26-003/customers)

## Overview

The Customers service is a RESTful API that maintains a list of customers and their details for an e-commerce application. This is a part of the Project for the Spring 2026 NYU DevOps Course

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

## Running Tests
```shell
make test
```
Running this command runs the full test suite with pytest and displays the coverage %

```shell
make lint
```
Running this command to lint the code

## API Reference
All endpoints are under the base path ```/customers ```

### Service Info

| Method | URL | Description |
|---|---|---|
| POST | ```/customers``` | Creates a customer. Required fields ```name, address``` |
| GET | ```/customers``` | Lists all the customers and their details |
| GET | ```/customers/{id}``` | Retrieves a single customers details |
| PUT | ```/customers/{id}``` | Updates a single customers details |
| PUT | ```/customers/{id}/suspend``` | Sets customer status to ```suspended``` |
| PUT | ```/customers/{id}/activate``` | Sets customer status to ```active``` |
| DELETE | ```/customers/{id}``` | Deletes a single customers details |
   
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
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

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
