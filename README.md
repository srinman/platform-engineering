# Platform Engineering on Azure Kubernetes Service (AKS)

A comprehensive reference implementation for building a platform engineering environment on AKS, featuring GitOps-based deployment patterns, self-service capabilities, and multiple real-world scenarios.

## Attributes of Platform 

- Implement best practices of compute, network and storage 
- Cost optimization 
- Multi-tenancy management
- GitOps for App and Infrastructure management 
- Application release management with canary, blue/green management 
- CRDs for Platform services  (KRO) and automation with Operators
- Observabilty implementation for platform and application 
- Security 
  - Network
  - RBAC
  - Policy constraints
  - App security - build and runtime


## Repository Structure

```
platform-engineering/
├── scenarios/              # Real-world platform engineering scenarios
│   ├── scenario1/         # Application DSL with security & governance
│   ├── scenario2/         # Dedicated cluster for 3rd party tools
│   ├── scenario3/         # Multi-tenant application platform
│   └── scenario4/         # ML/AI workload platform
├── baseline-clusters/     # Baseline cluster configurations
│   ├── baseline-cluster1/ # Standard AKS with GitOps
│   ├── baseline-cluster2/ # AKS Automatic
│   └── baseline-cluster3/ # High-security cluster
├── common/               # Shared components and utilities
│   ├── kro-definitions/  # Reusable KRO ResourceGroups
│   ├── policies/         # Azure Policies and Gatekeeper
│   └── templates/        # Common Terraform modules
└── docs/                 # Documentation and guides
```

## What is Platform Engineering?

Platform engineering focuses on building an internal developer platform (IDP) that abstracts infrastructure complexity, enables self-service, and accelerates application delivery. It emerged from the need to overcome the limitations of traditional "ticket ops" workflows and reduce developer cognitive load.

### Problems This Platform Solves

**Traditional "Ticket Ops" Challenges:**
- Developers blocked waiting for infrastructure provisioning tickets
- Manual processes creating bottlenecks (days/weeks to provision resources)
- Fragmented knowledge and undocumented processes
- High cognitive load from managing infrastructure complexity
- Inconsistent configurations across teams and environments
- Slow development cycles and delayed time-to-market
- Security and compliance applied as afterthoughts

**Platform Engineering Approach:**
- **Self-Service**: Developers provision resources instantly using declarative DSLs
- **Automation**: Infrastructure, deployment, and security policies applied automatically
- **Standardization**: Golden paths ensure consistency and best practices
- **Reduced Cognitive Load**: Developers focus on code, not Kubernetes/infrastructure details
- **Faster Delivery**: Minutes instead of days/weeks for common tasks
- **Built-in Security**: Compliance and security policies enforced at platform level
- **Improved Developer Experience**: Modern, frictionless workflows increase productivity and satisfaction

### Platform Capabilities

This repository demonstrates a platform-as-a-product approach with:

- **Self-Service Capabilities**: Developers declare what they need using simple DSLs
- **Security & Governance**: Built-in compliance and security policies
- **GitOps Principles**: Infrastructure and applications managed through Git
- **Multi-Cluster Management**: Separation of concerns across environments
- **Day 2 Operations**: Automated operations, monitoring, and lifecycle management
- **Golden Paths**: Approved patterns for common use cases
- **Internal Developer Portal Ready**: Designed for integration with Backstage or similar IDPs

## Scenarios

### Scenario 1: Application Deployment DSL
**Use Case**: Application teams need a simple way to deploy their applications without managing Kubernetes complexity.

**Solution**: Provides a declarative DSL (using KRO) where teams specify:
- Application name and container image
- Resource requirements
- Networking and ingress rules
- Security policies

Platform automatically provisions compliant infrastructure.

[→ See Scenario 1 Details](./scenarios/scenario1/README.md)

### Scenario 2: 3rd Party Tool Platform
**Use Case**: Deploy external tools (monitoring, security scanning, CI/CD tools) that require Kubernetes API access in isolated environments.

**Solution**: Automated provisioning of dedicated AKS clusters with:
- Isolated network configuration
- RBAC and service account setup
- Tool-specific configurations via DSL

[→ See Scenario 2 Details](./scenarios/scenario2/README.md)

### Scenario 3: Multi-Tenant Application Platform
**Use Case**: Host multiple application teams on shared infrastructure with isolation and resource quotas.

**Solution**: Namespace-per-team model with:
- Resource quotas and limits
- Network policies for isolation
- RBAC per team
- Cost tracking per tenant

[→ See Scenario 3 Details](./scenarios/scenario3/README.md)

### Scenario 4: ML/AI Workload Platform
**Use Case**: Data science teams need GPU-enabled compute for training and inference workloads.

**Solution**: Specialized cluster configuration with:
- GPU node pools
- JupyterHub for notebooks
- MLflow for experiment tracking
- Model serving capabilities

[→ See Scenario 4 Details](./scenarios/scenario4/README.md)

## Baseline Clusters

### baseline-cluster1: Standard AKS with GitOps
- Standard AKS cluster
- ArgoCD for GitOps
- CAPZ/Crossplane for infrastructure management
- Full observability stack

### baseline-cluster2: AKS Automatic
- Leverages AKS Automatic features
- Simplified management
- Auto-scaling and auto-upgrades
- Built-in security defaults

### baseline-cluster3: High-Security Cluster
- Private cluster configuration
- Azure Policy integration
- Workload Identity
- Network policies and egress lockdown

## Prerequisites

- Azure subscription
- Azure CLI (2.60.0+)
- Terraform (1.8.3+)
- kubectl (1.28.9+)
- Helm (3.0+)
- Git

## Quick Start

1. **Choose a scenario** based on your requirements
2. **Deploy a baseline cluster** that matches your needs
3. **Apply the scenario configuration** using the provided DSL
4. **Onboard your teams** with self-service capabilities

```bash
# Example: Deploy Scenario 1 with baseline-cluster1
cd baseline-clusters/baseline-cluster1
terraform init
terraform apply

cd ../../scenarios/scenario1
kubectl apply -f kro-definitions/
kubectl apply -f examples/my-app.yaml
```

## Architecture Principles

This repository follows the **GitOps Bridge Pattern** and implements:

1. **Control Plane Cluster**: Manages infrastructure and application clusters
2. **Separation of Concerns**: Different clusters for different purposes
3. **Declarative Configuration**: Everything defined in Git
4. **Progressive Delivery**: Safe rollout strategies
5. **Observability First**: Built-in monitoring and logging

## Documentation

### Core Concepts
- **[Platform Architecture](./docs/PLATFORM-ARCHITECTURE.md)**: Complete architecture overview, orchestration, and control plane design
- **[Golden Paths](./docs/GOLDEN-PATHS.md)**: Recommended patterns and best practices for common use cases
- **[Developer Experience](./docs/DEVELOPER-EXPERIENCE.md)**: DORA metrics, DevEx measurements, and continuous improvement
- **[Team Topologies](./docs/TEAM-TOPOLOGIES.md)**: Team structure, responsibilities, and collaboration patterns

### Implementation Guides
- **[Getting Started](./docs/GETTING-STARTED.md)**: Step-by-step onboarding guide
- **[Internal Developer Portal](./docs/INTERNAL-DEVELOPER-PORTAL.md)**: Backstage integration for service discovery and self-service
- **[Observability](./docs/OBSERVABILITY.md)**: Metrics, logging, tracing, and alerting implementation
- **[Quick Reference](./docs/QUICK-REFERENCE.md)**: Common commands and troubleshooting

### Additional Resources
- **[Contributing](./docs/CONTRIBUTING.md)**: How to contribute to the platform
- **[Repository Summary](./docs/REPOSITORY-SUMMARY.md)**: Overview of repository structure and contents

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for details.

## External Resources

- [CNCF Platform Engineering](https://www.cncf.io/blog/2025/11/19/what-is-platform-engineering/)
- [Microsoft Platform Engineering Guide](https://learn.microsoft.com/en-us/platform-engineering/)
- [AKS Platform Engineering Sample](https://learn.microsoft.com/en-us/samples/azure-samples/aks-platform-engineering/aks-platform-engineering/)
- [KRO Project](https://kro.run/)
- [GitOps Bridge Pattern](https://github.com/gitops-bridge-dev/gitops-bridge)
- [Team Topologies](https://teamtopologies.com/)
- [Backstage](https://backstage.io/)

## License

MIT License - see [LICENSE](./LICENSE) for details
