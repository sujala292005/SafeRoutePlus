variable "project_name" {
  type        = string
  description = "Project name prefix"
  default     = "saferouteplus"
}

variable "location" {
  type        = string
  description = "Azure region"
  default     = "centralindia"
}

variable "key_vault_name" {
  type        = string
  description = "Exact Key Vault name"
  default     = "saferoutepluskvci"
}
