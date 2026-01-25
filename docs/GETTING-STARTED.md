# Getting Started with Platform Engineering on AKS

This guide will help you get started with the platform engineering repository.

## Overview

This repository provides reference implementations for building a platform engineering environment on Azure Kubernetes Service (AKS). It includes:

- **Scenarios**: Real-world use cases with complete implementations
- **Baseline Clusters**: Production-ready cluster templates
- **Common Components**: Reusable modules and definitions
- **Documentation**: Comprehensive guides and best practices

## Prerequisites

Before you begin, ensure you have:

1. **Azure Subscription**: An active Azure subscription with appropriate permissions
2. **Tools Installed**:
   - Azure CLI (2.60.0+)
   - Terraform (1.8.3+)
   - kubectl (1.28.9+)
   - Helm (3.0+)
   - Git

3. **Azure Permissions**:
   - Create resource groups
   - Create AKS clusters
   - Assign roles
   - Create networking resources

## Quick Start

### Step 1: Choose Your Path

Select based on your needs:

#### Path A: Deploy a Baseline Cluster First
Start with a foundational cluster, then add scenarios.

```bash
# Deploy baseline-cluster1 (standard AKS with GitOps)
cd baseline-clusters/baseline-cluster1
```

#### Path B: Start with a Scenario
Jump directly to a specific use case.

```bash
# Example: Application deployment scenario
cd scenarios/scenario1
```

### Step 2: Deploy a Baseline Cluster

We'll use baseline-cluster1 as an example:

```bash
cd baseline-clusters/baseline-cluster1/terraform

# Configure your settings
cp terraform.tfvars.example terraform.tfvars
vim terraform.tfvars  # Edit with your values

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Deploy
terraform apply

# Get kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```

### Step 3: Access ArgoCD

```bash
# Get ArgoCD password
kubectl get secret argocd-initial-admin-secret -n argocd \
  --template="{{index .data.password | base64decode}}"

# Port-forward to ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open https://localhost:8080
# Username: admin
# Password: <from above>
```

### Step 4: Deploy a Scenario

Now deploy Scenario 1 (Application DSL):

```bash
cd ../../../scenarios/scenario1

# Install the KRO ResourceGroup
kubectl apply -f kro-definitions/application-resourcegroup.yaml

# Deploy an example application
kubectl create namespace dev-team-a
kubectl apply -f examples/simple-web-app.yaml

# Check the created resources
kubectl get applications -n dev-team-a
kubectl get deployment,service,ingress -n dev-team-a
```

### Step 5: Verify Deployment

```bash
# Check application status
kubectl get application simple-web-app -n dev-team-a

# View created resources
kubectl get all -n dev-team-a -l app.kubernetes.io/name=simple-web-app

# Get ingress URL (if configured)
kubectl get ingress -n dev-team-a
```

## Common Workflows

### Onboard a New Team (Scenario 3)

```bash
cd scenarios/scenario3

# Install Tenant ResourceGroup
kubectl apply -f kro-definitions/tenant-resourcegroup.yaml

# Create a tenant for the team
kubectl apply -f examples/team-a-tenant.yaml

# Team can now deploy in their namespace
kubectl config set-context --current --namespace=team-a
```

### Deploy 3rd Party Tool (Scenario 2)

```bash
cd scenarios/scenario2

# Install ToolPlatform ResourceGroup
kubectl apply -f kro-definitions/toolplatform-resourcegroup.yaml

# Deploy GitLab Runner platform
kubectl apply -f examples/gitlab-runner-platform.yaml

# Monitor cluster creation
kubectl get toolplatform gitlab-runner -w
```

### Set Up ML Platform (Scenario 4)

```bash
cd scenarios/scenario4

# Install MLPlatform ResourceGroup
kubectl apply -f kro-definitions/mlplatform-resourcegroup.yaml

# Deploy ML platform
kubectl apply -f examples/ml-platform.yaml
```

## Architecture Decision Flow

```
┌─────────────────────────────────────────────┐
│ What do you need?                            │
└──────────────────┬──────────────────────────┘
                   │
    ┌──────────────┼──────────────┬──────────────────┐
    │              │              │                  │
    ▼              ▼              ▼                  ▼
┌────────┐   ┌─────────┐   ┌──────────┐      ┌──────────┐
│ Deploy │   │ Deploy  │   │ Multi-   │      │ ML/AI    │
│ Apps   │   │ Tools   │   │ Tenant   │      │ Platform │
└───┬────┘   └────┬────┘   └────┬─────┘      └────┬─────┘
    │             │              │                  │
    ▼             ▼              ▼                  ▼
Scenario 1    Scenario 2    Scenario 3        Scenario 4
```

## Next Steps

After completing the quick start:

1. **Customize for Your Organization**
   - Modify KRO ResourceGroups
   - Add custom policies
   - Configure monitoring

2. **Set Up CI/CD**
   - Integrate with GitHub Actions
   - Configure GitOps workflows
   - Automate deployments

3. **Implement Security**
   - Configure Azure AD integration
   - Set up RBAC policies
   - Enable security scanning

4. **Add Monitoring**
   - Configure alerting
   - Set up dashboards
   - Enable log aggregation

5. **Cost Management**
   - Set up budgets
   - Configure cost allocation
   - Implement auto-scaling

## Troubleshooting

### Terraform Errors

```bash
# Check Azure CLI authentication
az account show

# Verify Azure permissions
az role assignment list --assignee $(az account show --query user.name -o tsv)

# Clean up failed deployments
terraform destroy
```

### Kubernetes Errors

```bash
# Verify kubeconfig
kubectl cluster-info

# Check pod logs
kubectl logs -n <namespace> <pod-name>

# Describe resource for events
kubectl describe <resource-type> <resource-name> -n <namespace>
```

### ArgoCD Not Syncing

```bash
# Check ArgoCD application status
kubectl get applications -n argocd

# View ArgoCD logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller

# Force sync
argocd app sync <app-name>
```

## Support and Resources

- **Documentation**: See `docs/` directory for detailed guides
- **Examples**: Check scenario `examples/` directories
- **Issues**: Report issues on GitHub
- **Community**: Join discussions in GitHub Discussions

## Learning Path

1. ✅ Complete quick start
2. ⬜ Deploy all scenarios
3. ⬜ Customize for your needs
4. ⬜ Implement CI/CD
5. ⬜ Add monitoring and alerting
6. ⬜ Configure cost management
7. ⬜ Implement security policies
8. ⬜ Set up backup and DR

## Additional Resources

- [Microsoft Platform Engineering Guide](https://learn.microsoft.com/en-us/platform-engineering/)
- [AKS Best Practices](https://learn.microsoft.com/en-us/azure/aks/best-practices)
- [KRO Documentation](https://kro.run/docs)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [CNCF Landscape](https://landscape.cncf.io/)
