# Baseline Cluster 1: Standard AKS with GitOps

This baseline provides a production-ready AKS cluster with GitOps using ArgoCD and infrastructure management via CAPZ (Cluster API Provider Azure).

## Features

- Standard AKS cluster (not Automatic)
- GitOps with ArgoCD
- CAPZ for infrastructure orchestration
- Full observability stack (Prometheus, Grafana, Loki)
- Policy enforcement (Azure Policy, Gatekeeper)
- Workload Identity for authentication
- Network policies enabled
- Cost optimization with node auto-scaling

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Control Plane Cluster                                   │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────────┐ │
│  │  ArgoCD   │  │   CAPZ   │  │  Observability       │ │
│  │           │  │          │  │  - Prometheus        │ │
│  └───────────┘  └──────────┘  │  - Grafana           │ │
│                                │  - Loki              │ │
│                                └──────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

- Azure subscription
- Azure CLI (2.60.0+)
- Terraform (1.8.3+)
- kubectl (1.28.9+)
- Sufficient Azure quota for AKS

## Quick Start

### 1. Configure Variables

```bash
cd baseline-clusters/baseline-cluster1/terraform

# Copy and edit the variables file
cp terraform.tfvars.example terraform.tfvars
vim terraform.tfvars
```

### 2. Deploy the Cluster

```bash
terraform init
terraform plan
terraform apply
```

### 3. Access the Cluster

```bash
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```

### 4. Access ArgoCD

```bash
# Get ArgoCD admin password
kubectl get secret argocd-initial-admin-secret -n argocd \
  --template="{{index .data.password | base64decode}}"

# Port-forward to ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open https://localhost:8080
# Username: admin
# Password: <from above command>
```

## What Gets Deployed

### Core Components
- AKS cluster (3 nodes, autoscaling enabled)
- Azure CNI networking
- Workload Identity
- Azure Key Vault integration
- Managed Prometheus and Grafana (optional)

### GitOps Components
- ArgoCD (with UI and CLI)
- ApplicationSets for app-of-apps pattern
- Bootstrap applications

### Infrastructure Management
- CAPZ (Cluster API Provider Azure)
- Azure Service Operator (ASO)
- KRO (Kubernetes Resource Orchestrator)

### Policy & Governance
- Azure Policy for AKS
- Gatekeeper (OPA)
- Pod Security Standards

### Observability
- Prometheus Operator
- Grafana
- Loki (log aggregation)
- Kubernetes Dashboard

## Configuration

Key variables in `terraform.tfvars`:

```hcl
# Cluster configuration
cluster_name            = "baseline-cluster1"
resource_group_name     = "rg-baseline-cluster1"
location                = "eastus"
kubernetes_version      = "1.28.3"

# Node configuration
node_count              = 3
node_vm_size            = "Standard_D4s_v3"
enable_auto_scaling     = true
min_count               = 2
max_count               = 10

# GitOps configuration
gitops_repo_url         = "https://github.com/srinman/platform-engineering"
gitops_repo_branch      = "main"
gitops_repo_path        = "baseline-clusters/baseline-cluster1/gitops"

# Infrastructure provider
infrastructure_provider = "capz"  # or "crossplane"

# Observability
enable_prometheus       = true
enable_grafana          = true
enable_loki             = true
```

## GitOps Structure

```
baseline-cluster1/
├── gitops/
│   ├── bootstrap/
│   │   └── applicationset.yaml    # App of Apps pattern
│   ├── addons/
│   │   ├── argocd/
│   │   ├── capz/
│   │   ├── kro/
│   │   ├── prometheus/
│   │   ├── grafana/
│   │   └── gatekeeper/
│   └── apps/
│       └── (application deployments)
└── terraform/
    ├── main.tf
    ├── variables.tf
    └── terraform.tfvars
```

## Upgrading

### Kubernetes Version

```bash
# Update terraform.tfvars
kubernetes_version = "1.29.0"

# Apply changes
terraform apply
```

### Add-ons

Edit the ArgoCD Applications in `gitops/addons/` and commit to Git. ArgoCD will automatically sync.

## Monitoring

Access Grafana:

```bash
kubectl port-forward svc/grafana -n monitoring 3000:80
# Open http://localhost:3000
# Username: admin
# Password: kubectl get secret grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 -d
```

## Troubleshooting

### ArgoCD not syncing

```bash
# Check ArgoCD application status
kubectl get applications -n argocd

# Check ArgoCD logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller
```

### CAPZ issues

```bash
# Check CAPZ controller logs
kubectl logs -n capz-system -l control-plane=capz-controller-manager
```

## Cleanup

```bash
terraform destroy
```

## Next Steps

1. Deploy applications using the scenarios
2. Configure monitoring dashboards
3. Set up alerting
4. Implement backup and DR
5. Configure cost management
