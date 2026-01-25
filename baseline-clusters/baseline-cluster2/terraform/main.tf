terraform {
  required_version = ">= 1.8.3"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
  
  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Purpose     = "Platform Engineering - AKS Automatic"
  }
}

# Log Analytics Workspace for monitoring
resource "azurerm_log_analytics_workspace" "main" {
  name                = "law-${var.cluster_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = var.log_analytics_retention_days
  
  tags = azurerm_resource_group.main.tags
}

# AKS Automatic Cluster
resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = var.cluster_name
  
  # AKS Automatic uses "Automatic" SKU tier
  sku_tier            = "Standard"
  automatic_upgrade_channel = "stable"
  
  # Enable AKS Automatic mode (preview feature)
  # This enables all automatic features
  node_os_upgrade_channel = "NodeImage"
  
  # Workload Identity
  oidc_issuer_enabled       = true
  workload_identity_enabled = true
  
  default_node_pool {
    name                = "system"
    vm_size             = var.node_vm_size
    enable_auto_scaling = true
    min_count           = var.min_nodes
    max_count           = var.max_nodes
    os_disk_size_gb     = 100
    
    # AKS Automatic optimizations
    ultra_ssd_enabled = false
    
    upgrade_settings {
      max_surge = "33%"
    }
  }
  
  identity {
    type = "SystemAssigned"
  }
  
  network_profile {
    network_plugin     = "azure"
    network_policy     = "azure"
    load_balancer_sku  = "standard"
  }
  
  # Enable Azure Monitor
  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }
  
  # Enable Azure Policy
  azure_policy_enabled = true
  
  # Key Vault integration
  key_vault_secrets_provider {
    secret_rotation_enabled  = true
    secret_rotation_interval = "2m"
  }
  
  # Maintenance window for updates
  maintenance_window {
    allowed {
      day   = "Sunday"
      hours = [2, 3, 4]
    }
  }
  
  # Auto-scaler profile for cost optimization
  auto_scaler_profile {
    balance_similar_node_groups      = true
    expander                         = "random"
    max_graceful_termination_sec     = 600
    max_node_provisioning_time       = "15m"
    max_unready_nodes                = 3
    max_unready_percentage           = 45
    new_pod_scale_up_delay           = "10s"
    scale_down_delay_after_add       = "10m"
    scale_down_delay_after_delete    = "10s"
    scale_down_delay_after_failure   = "3m"
    scan_interval                    = "10s"
    scale_down_unneeded              = "10m"
    scale_down_unready               = "20m"
    scale_down_utilization_threshold = "0.5"
    skip_nodes_with_local_storage    = false
    skip_nodes_with_system_pods      = true
  }
  
  tags = azurerm_resource_group.main.tags
}

# Save kubeconfig
resource "local_file" "kubeconfig" {
  content  = azurerm_kubernetes_cluster.main.kube_config_raw
  filename = "${path.module}/kubeconfig"
  
  file_permission = "0600"
}

# Outputs
output "cluster_name" {
  value = azurerm_kubernetes_cluster.main.name
}

output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "cluster_fqdn" {
  value = azurerm_kubernetes_cluster.main.fqdn
}

output "kubeconfig_path" {
  value = local_file.kubeconfig.filename
}

output "oidc_issuer_url" {
  value = azurerm_kubernetes_cluster.main.oidc_issuer_url
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.main.id
}
