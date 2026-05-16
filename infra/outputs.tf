output "app_url" {
  value = "https://${azurerm_linux_web_app.app_service.default_hostname}"
}

output "postgres_server" {
  value = azurerm_postgresql_flexible_server.pg_server.fqdn
}