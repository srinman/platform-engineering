# Common Terraform Modules

This directory contains reusable Terraform modules for platform engineering on AKS.

## Available Modules

### aks-cluster
Standard AKS cluster module with best practices

### aks-automatic
AKS Automatic cluster module

### networking
Virtual network and subnet configuration

### monitoring
Observability stack (Prometheus, Grafana, Loki)

### gitops
ArgoCD installation and configuration

## Usage Example

```hcl
module "aks_cluster" {
  source = "../../common/templates/aks-cluster"
  
  cluster_name        = "my-cluster"
  resource_group_name = "my-rg"
  location            = "eastus"
  kubernetes_version  = "1.28.3"
  
  # Additional configuration
}
```

## Module Structure

Each module follows this structure:

```
module-name/
├── main.tf          # Main resources
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── versions.tf      # Provider requirements
└── README.md        # Module documentation
```

## Best Practices

1. **Pin versions**: Always specify provider versions
2. **Use variables**: Make modules configurable
3. **Provide outputs**: Export useful information
4. **Document thoroughly**: Include examples and descriptions
5. **Test modules**: Validate before using in production
