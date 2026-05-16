terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "random_password" "pg_password" {
  length           = 16
  special          = true
  override_special = "!#%&*()-_=+[]{}<>:?"
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-devops-task-tracker"
  location = "Switzerland North"
}

resource "azurerm_postgresql_flexible_server" "pg_server" {
  name                   = "pg-tasktracker-${random_string.suffix.result}"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "14"
  administrator_login    = "pgadmin"
  administrator_password = random_password.pg_password.result
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
}

resource "azurerm_postgresql_flexible_server_database" "pg_db" {
  name      = "tasks_db"
  server_id = azurerm_postgresql_flexible_server.pg_server.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_all" {
  name             = "AllowAllIPs"
  server_id        = azurerm_postgresql_flexible_server.pg_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

resource "azurerm_service_plan" "app_plan" {
  name                = "plan-tasktracker-${random_string.suffix.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "app_service" {
  name                = "app-tasktracker-${random_string.suffix.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.app_plan.id

  site_config {
    application_stack {
      python_version = "3.11"
    }

    always_on        = true
    app_command_line = "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
  }

  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "DB_HOST"                        = azurerm_postgresql_flexible_server.pg_server.fqdn
    "DB_NAME"                        = azurerm_postgresql_flexible_server_database.pg_db.name
    "DB_USER"                        = azurerm_postgresql_flexible_server.pg_server.administrator_login
    "DB_PASSWORD"                    = random_password.pg_password.result
  }
}