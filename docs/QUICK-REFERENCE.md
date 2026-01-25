# Platform Engineering Repository - Quick Reference

## 📁 Repository Structure

```
platform-engineering/
│
├── scenarios/                      # Real-world use cases
│   ├── scenario1/                 # ✨ Application Deployment DSL
│   │   ├── README.md              # Complete documentation
│   │   ├── kro-definitions/       # KRO ResourceGroup for Application
│   │   └── examples/              # Sample applications
│   │
│   ├── scenario2/                 # 🔧 3rd Party Tool Platform
│   │   ├── README.md              # Tool platform guide
│   │   ├── kro-definitions/       # KRO ResourceGroup for ToolPlatform
│   │   └── examples/              # GitLab Runner, Argo CD examples
│   │
│   ├── scenario3/                 # 👥 Multi-Tenant Platform
│   │   ├── README.md              # Multi-tenancy guide
│   │   └── kro-definitions/       # KRO ResourceGroup for Tenant
│   │
│   └── scenario4/                 # 🤖 ML/AI Workload Platform
│       ├── README.md              # ML platform guide
│       └── kro-definitions/       # KRO ResourceGroup for MLPlatform
│
├── baseline-clusters/             # Foundation cluster templates
│   ├── baseline-cluster1/         # 🏗️ Standard AKS with GitOps
│   │   ├── README.md              # Deployment guide
│   │   ├── terraform/             # Infrastructure as Code
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── values/            # ArgoCD values
│   │   └── gitops/                # GitOps configurations
│   │       └── bootstrap/         # ArgoCD ApplicationSet
│   │
│   └── baseline-cluster2/         # ⚡ AKS Automatic
│       ├── README.md              # AKS Automatic guide
│       └── terraform/             # Simplified infrastructure
│
├── common/                        # Shared resources
│   ├── kro-definitions/           # Reusable KRO ResourceGroups
│   ├── templates/                 # Terraform modules
│   └── policies/                  # Azure Policies & Gatekeeper
│
└── docs/                          # Documentation
    ├── GETTING-STARTED.md         # 🚀 Quick start guide
    └── CONTRIBUTING.md            # Contribution guidelines
```

## 🎯 Scenarios Overview

| Scenario | Use Case | Key Technology |
|----------|----------|----------------|
| **Scenario 1** | Application teams deploy apps without K8s complexity | KRO Application DSL |
| **Scenario 2** | Isolated clusters for 3rd party tools (GitLab, Argo) | KRO ToolPlatform + CAPZ |
| **Scenario 3** | Multiple teams sharing cluster with isolation | KRO Tenant + Quotas |
| **Scenario 4** | ML/AI workloads with GPU support | KRO MLPlatform + JupyterHub |

## 🏗️ Baseline Clusters

| Cluster | Type | Best For |
|---------|------|----------|
| **baseline-cluster1** | Standard AKS + GitOps | Production, full control |
| **baseline-cluster2** | AKS Automatic | Simplified ops, auto-scaling |

## 🚀 Quick Start Commands

### Deploy Baseline Cluster 1
```bash
cd baseline-clusters/baseline-cluster1/terraform
terraform init
terraform apply
export KUBECONFIG=$(pwd)/kubeconfig
```

### Deploy Application (Scenario 1)
```bash
cd scenarios/scenario1
kubectl apply -f kro-definitions/application-resourcegroup.yaml
kubectl create namespace dev-team-a
kubectl apply -f examples/simple-web-app.yaml
```

### Deploy Tool Platform (Scenario 2)
```bash
cd scenarios/scenario2
kubectl apply -f kro-definitions/toolplatform-resourcegroup.yaml
kubectl apply -f examples/gitlab-runner-platform.yaml
```

### Create Multi-Tenant Namespace (Scenario 3)
```bash
cd scenarios/scenario3
kubectl apply -f kro-definitions/tenant-resourcegroup.yaml
kubectl apply -f examples/team-a-tenant.yaml
```

## 🔑 Key Technologies

- **KRO (Kubernetes Resource Orchestrator)**: High-level DSL for K8s resources
- **ArgoCD**: GitOps continuous deployment
- **CAPZ**: Cluster API Provider Azure for infrastructure management
- **Azure Policy**: Governance and compliance
- **Workload Identity**: Secure authentication

## 📚 Learning Path

1. ✅ Read main [README.md](../README.md)
2. ✅ Review [GETTING-STARTED.md](GETTING-STARTED.md)
3. ✅ Deploy baseline-cluster1
4. ✅ Try Scenario 1 (simplest)
5. ✅ Explore other scenarios
6. ✅ Customize for your needs

## 🛠️ Common Tasks

### Get Cluster Info
```bash
kubectl cluster-info
kubectl get nodes
```

### Access ArgoCD
```bash
kubectl get secret argocd-initial-admin-secret -n argocd \
  --template="{{index .data.password | base64decode}}"
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Open https://localhost:8080
```

### Check Application Status
```bash
kubectl get applications -n <namespace>
kubectl describe application <app-name> -n <namespace>
```

### View Logs
```bash
kubectl logs -n <namespace> -l app=<app-name>
```

## 🔗 Important Links

- Main README: [README.md](../README.md)
- Getting Started: [GETTING-STARTED.md](GETTING-STARTED.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Microsoft Platform Engineering: https://learn.microsoft.com/en-us/platform-engineering/
- KRO Project: https://kro.run/

## 💡 Decision Tree

```
Need to deploy an application?
  └─> Use Scenario 1 (Application DSL)

Need to run a tool (GitLab, Argo, etc)?
  └─> Use Scenario 2 (ToolPlatform)

Need to host multiple teams?
  └─> Use Scenario 3 (Multi-Tenant)

Need GPU for ML/AI?
  └─> Use Scenario 4 (ML Platform)

Starting from scratch?
  └─> Deploy baseline-cluster1 or baseline-cluster2 first
```

## 📊 Features Matrix

| Feature | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|---------|-----------|-----------|-----------|-----------|
| Simple DSL | ✅ | ✅ | ✅ | ✅ |
| Auto-scaling | ✅ | ✅ | ❌ | ✅ |
| Resource Quotas | ✅ | ❌ | ✅ | ✅ |
| Network Policies | ✅ | ✅ | ✅ | ✅ |
| Monitoring | ✅ | ✅ | ✅ | ✅ |
| Multi-Cluster | ❌ | ✅ | ❌ | ❌ |
| GPU Support | ❌ | ❌ | ❌ | ✅ |

---

**Repository**: srinman/platform-engineering  
**License**: MIT  
**Last Updated**: December 2025
