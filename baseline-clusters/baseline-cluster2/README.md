# Baseline Cluster 2: AKS Automatic

This baseline provides an AKS Automatic cluster with simplified management and built-in best practices.

## Features

- **AKS Automatic**: Simplified AKS experience with managed configurations
- Auto-scaling (nodes and pods)
- Auto-upgrades with maintenance windows
- Built-in security defaults
- Integrated monitoring with Azure Monitor
- Cost optimization enabled by default
- Simplified networking

## What is AKS Automatic?

AKS Automatic is a new mode that provides:
- Opinionated, production-ready configuration
- Automatic node and pod scaling
- Automated security updates
- Built-in cost optimization
- Simplified operations

Perfect for teams who want Kubernetes without operational complexity.

## Quick Start

### 1. Configure Variables

```bash
cd baseline-clusters/baseline-cluster2/terraform

cp terraform.tfvars.example terraform.tfvars
vim terraform.tfvars
```

### 2. Deploy

```bash
terraform init
terraform apply
```

### 3. Access

```bash
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```

## What Gets Deployed

### Automatic Features
- Auto-scaling node pools
- Vertical Pod Autoscaler (VPA)
- Horizontal Pod Autoscaler (HPA)
- Cluster Autoscaler
- Automatic OS updates
- Automatic Kubernetes version updates

### Monitoring
- Azure Monitor for containers
- Container Insights
- Prometheus metrics (integrated)
- Log Analytics workspace

### Security
- Pod Security Standards (enforced)
- Network policies (enabled)
- Workload Identity
- Azure Policy integration

## Configuration

Key variables:

```hcl
cluster_name         = "baseline-cluster2"
location             = "eastus"
kubernetes_version   = "automatic"  # Special value for AKS Automatic
sku_tier             = "Standard"   # or "Premium"

# Node pool sizing (ranges, not exact values)
min_nodes            = 1
max_nodes            = 100

# Monitoring
enable_azure_monitor = true
log_analytics_retention_days = 30
```

## Comparison with Baseline Cluster 1

| Feature | Baseline 1 (Standard) | Baseline 2 (Automatic) |
|---------|----------------------|------------------------|
| Management | Manual configuration | Automated |
| Scaling | Configure manually | Auto-configured |
| Updates | Manual planning | Automatic |
| Security | Configure policies | Built-in defaults |
| Complexity | Higher | Lower |
| Flexibility | More customizable | Opinionated |
| Use Case | Advanced users | Simplified operations |

## Maintenance Windows

AKS Automatic uses maintenance windows for updates:

```bash
# Check maintenance windows
az aks maintenanceconfiguration list \
  --resource-group rg-baseline-cluster2 \
  --cluster-name baseline-cluster2
```

## Monitoring

Access Azure Monitor:
1. Navigate to Azure Portal
2. Go to your AKS cluster
3. Select "Monitoring" > "Insights"

## Cost Optimization

AKS Automatic includes:
- Right-sized node recommendations
- Spot instance support
- Auto-shutdown for dev/test
- Reserved instance recommendations

View cost analysis:
```bash
az aks cost-analysis show \
  --resource-group rg-baseline-cluster2 \
  --name baseline-cluster2
```

## Upgrading

Upgrades are automatic, but you can check status:

```bash
az aks show \
  --resource-group rg-baseline-cluster2 \
  --name baseline-cluster2 \
  --query "autoUpgradeProfile"
```

## Troubleshooting

### Check cluster health

```bash
az aks show \
  --resource-group rg-baseline-cluster2 \
  --name baseline-cluster2 \
  --query "powerState"
```

### View recent operations

```bash
az aks operation-list \
  --resource-group rg-baseline-cluster2 \
  --name baseline-cluster2
```

## When to Use AKS Automatic

✅ Use AKS Automatic when:
- You want simplified operations
- You prefer opinionated configurations
- You need automatic scaling and updates
- You're new to Kubernetes

❌ Use Standard AKS (Baseline 1) when:
- You need full control over configuration
- You have specific networking requirements
- You need custom node configurations
- You want to use CAPZ/Crossplane

## Cleanup

```bash
terraform destroy
```
