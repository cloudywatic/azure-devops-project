# Azure DevOps Task Tracker

## Project Overview

This project is a cloud-native DevOps application built using Python Flask, Azure Cloud services, Terraform Infrastructure as Code (IaC), and GitHub Actions CI/CD.

The application is a simple Task Tracker web application where users can:

- Add tasks
- View tasks
- Delete tasks

All task data is stored inside an Azure PostgreSQL database.

---

# Technologies Used

## Application

- Python 3.11
- Flask
- HTML

## Cloud Platform

- Microsoft Azure

## Azure Services

- Azure App Service (PaaS)
- Azure Database for PostgreSQL Flexible Server (DBaaS)

## DevOps / Automation

- Terraform
- GitHub Actions
- Git
- GitHub

---

# Architecture

```text
GitHub Repository
        ↓
GitHub Actions CI/CD Pipeline
        ↓
Azure App Service
        ↓
Azure PostgreSQL Database
```

---

# Why These Technologies Were Chosen

## Azure App Service

Azure App Service was selected because it is a Platform as a Service (PaaS) solution that allows deployment of Python web applications without manually managing virtual machines or operating systems.

Benefits:

- Easy deployment
- Managed infrastructure
- Automatic scaling support
- Simplified cloud hosting

## Azure PostgreSQL Flexible Server

Azure PostgreSQL Flexible Server was chosen as the backend database because it is a managed Database as a Service (DBaaS) platform.

Benefits:

- Managed backups
- Cloud-hosted PostgreSQL
- Secure database management
- Easy integration with Azure services

## Terraform

Terraform was used to provision the cloud infrastructure using Infrastructure as Code (IaC).

Benefits:

- Reproducible infrastructure
- One-command deployment
- Version-controlled infrastructure
- Automated cloud provisioning

## GitHub Actions

GitHub Actions was used to implement Continuous Integration and Continuous Deployment (CI/CD).

Benefits:

- Automatic deployment after git push
- Integration with GitHub repository
- Automated cloud deployment workflow

---

# Infrastructure Created by Terraform

Terraform automatically creates:

- Azure Resource Group
- Azure App Service Plan
- Azure Linux Web App
- Azure PostgreSQL Flexible Server
- PostgreSQL Database
- Firewall Rule
- Environment Variables for database connection

---

# Environment Variables

The application uses these environment variables:

```text
DB_HOST
DB_NAME
DB_USER
DB_PASSWORD
PORT
```

These are automatically configured by Terraform inside Azure App Service.

---

# CI/CD Pipeline

The CI/CD pipeline automatically triggers whenever code is pushed to the `main` branch.

Pipeline stages:

1. Checkout source code
2. Setup Python environment
3. Install dependencies
4. Deploy application to Azure App Service

This ensures that every code change is automatically deployed to the cloud environment.

---

# Local Development Setup

## Create Virtual Environment

```powershell
python -m venv venv
```

## Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

## Install Dependencies

```powershell
pip install -r requirements.txt
```

## Run Flask Application

```powershell
python app.py
```

---

# Terraform Commands

## Initialize Terraform

```powershell
terraform init
```

## Preview Infrastructure Changes

```powershell
terraform plan
```

## Create Infrastructure

```powershell
terraform apply
```

## Destroy Infrastructure

```powershell
terraform destroy
```

---

# GitHub Actions Secret

The following GitHub repository secret is required:

```text
AZURE_WEBAPP_PUBLISH_PROFILE
```

This secret stores the Azure publish profile used for automatic deployment.

---

# Deployment Workflow

```text
Developer pushes code to GitHub
            ↓
GitHub Actions workflow starts automatically
            ↓
Application is deployed to Azure App Service
            ↓
Flask app connects to Azure PostgreSQL database
```

---

# Project Structure

```text
azure-devops-project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── infra/
│   ├── main.tf
│   ├── outputs.tf
│   └── .terraform.lock.hcl
│
└── .github/
    └── workflows/
        └── deploy.yml
```

---

# Infrastructure Information

## Resource Group

```text
rg-devops-task-tracker
```

## Azure Region

```text
Switzerland North
```

---

# Future Improvements

Possible future improvements include:

- Docker containerization
- Kubernetes deployment
- Authentication system
- Better frontend styling
- Task completion status
- Automated testing

---

# Author
Mohannad Alkharoubi W9K8X1

DevOps and Cloud Engineering Project