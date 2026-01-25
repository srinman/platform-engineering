variable "cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "baseline-cluster1"
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "rg-baseline-cluster1"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28.3"
}

variable "node_count" {
  description = "Initial number of nodes"
  type        = number
  default     = 3
}

variable "node_vm_size" {
  description = "VM size for nodes"
  type        = string
  default     = "Standard_D4s_v3"
}

variable "enable_auto_scaling" {
  description = "Enable auto-scaling for the node pool"
  type        = bool
  default     = true
}

variable "min_count" {
  description = "Minimum number of nodes when auto-scaling is enabled"
  type        = number
  default     = 2
}

variable "max_count" {
  description = "Maximum number of nodes when auto-scaling is enabled"
  type        = number
  default     = 10
}

variable "vnet_address_space" {
  description = "Address space for the virtual network"
  type        = string
  default     = "10.1.0.0/16"
}

variable "aks_subnet_address_prefix" {
  description = "Address prefix for the AKS subnet"
  type        = string
  default     = "10.1.0.0/22"
}

variable "gitops_repo_url" {
  description = "GitOps repository URL"
  type        = string
  default     = "https://github.com/srinman/platform-engineering"
}

variable "gitops_repo_branch" {
  description = "GitOps repository branch"
  type        = string
  default     = "main"
}

variable "gitops_repo_path" {
  description = "Path to GitOps configurations"
  type        = string
  default     = "baseline-clusters/baseline-cluster1/gitops"
}

variable "infrastructure_provider" {
  description = "Infrastructure provider (capz or crossplane)"
  type        = string
  default     = "capz"
  
  validation {
    condition     = contains(["capz", "crossplane"], var.infrastructure_provider)
    error_message = "Infrastructure provider must be either 'capz' or 'crossplane'."
  }
}
