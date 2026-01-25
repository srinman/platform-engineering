# Platform Architecture

## Overview

This document describes the architecture of our platform engineering solution on Azure Kubernetes Service (AKS), including how different components orchestrate together, the control plane design, and integration patterns.

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  Developer Interface Layer                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │   Backstage      │  │   GitOps Repos   │  │     CLI      │ │
│  │     (IDP)        │  │   (GitHub/ADO)   │  │   Tools      │ │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘ │
│           │                     │                     │         │
└───────────┼─────────────────────┼─────────────────────┼─────────┘
            │                     │                     │
            ▼                     ▼                     ▼
┌────────────────────────────────────────────────────────────────┐
│  Platform Orchestration Layer (Control Plane)                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ArgoCD (GitOps Operator)                                │  │
│  │  - Watches Git repositories                              │  │
│  │  - Syncs application state                               │  │
│  │  - Manages application lifecycle                         │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  KRO (Kubernetes Resource Orchestrator)                  │  │
│  │  - ResourceGroup definitions (DSLs)                      │  │
│  │  - Application, ToolPlatform, Tenant abstractions        │  │
│  │  - Generates K8s resources from high-level specs         │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Infrastructure Provisioners                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  │
│  │  │  Terraform  │  │   CAPZ      │  │ Crossplane  │      │  │
│  │  │   (Azure)   │  │ (Clusters)  │  │ (Cloud Res.)│      │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────────────┐
│  Platform Services Layer                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Ingress    │  │   Cert-Mgr   │  │  Prometheus  │         │
│  │   (NGINX)    │  │    (TLS)     │  │ (Monitoring) │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  OPA/GK      │  │    Vault     │  │     Loki     │         │
│  │  (Policy)    │  │  (Secrets)   │  │  (Logging)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────┬────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────────────┐
│  Application Workload Layer                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Team A     │  │   Team B     │  │   Team C     │         │
│  │ Applications │  │ Applications │  │ Applications │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  Azure Infrastructure Layer                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │     AKS      │  │     VNet     │  │     ACR      │         │
│  │   Clusters   │  │  Networking  │  │  (Registry)  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Key Vault   │  │   Storage    │  │  Log Anal.   │         │
│  │  (Secrets)   │  │  Accounts    │  │  Workspace   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────────────────────────────────────────┘
```

## Control Plane Architecture

The control plane manages the entire platform lifecycle:

```
┌─────────────────────────────────────────────────────────────┐
│  Control Plane Cluster (baseline-cluster1)                  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  GitOps Controller (ArgoCD)                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │  App of     │  │  Bootstrap  │  │  Cluster    │   │ │
│  │  │  Apps       │  │  Apps       │  │  Add-ons    │   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │ │
│  │        │                 │                 │          │ │
│  │        └─────────────────┴─────────────────┘          │ │
│  │                          │                            │ │
│  │                  Watches Git Repos                    │ │
│  │                          │                            │ │
│  │                          ▼                            │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Git Repositories                               │ │ │
│  │  │  - Platform configurations                      │ │ │
│  │  │  - Application manifests                        │ │ │
│  │  │  - Infrastructure definitions                   │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Resource Orchestrator (KRO)                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │ │
│  │  │ Application  │  │ ToolPlatform │  │   Tenant   │  │ │
│  │  │ ResourceGroup│  │ ResourceGroup│  │ResourceGroup│ │ │
│  │  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │ │
│  │         │                 │                 │         │ │
│  │         └─────────────────┴─────────────────┘         │ │
│  │                          │                            │ │
│  │          Generates Kubernetes Resources              │ │
│  │                          │                            │ │
│  │                          ▼                            │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Kubernetes API Server                          │ │ │
│  │  │  Creates: Deployments, Services, Ingress, etc.  │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Infrastructure Provisioner (Terraform/Crossplane)    │ │
│  │  - Provision Azure resources                          │ │
│  │  - Manage AKS clusters                                │ │
│  │  - Configure networking                               │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Roles and Orchestration

### Layer 1: Developer Interface
**Components**: Backstage, Git, CLI

**Role**: Entry point for developers

**Orchestrates**:
- Developers create applications via templates
- Commits pushed to Git repositories
- Pull requests reviewed and merged
- Git triggers downstream automation

### Layer 2: GitOps Controller (ArgoCD)
**Role**: Continuous reconciliation and deployment

**Orchestrates**:
1. Watches Git repositories for changes
2. Detects drift between desired (Git) and actual (cluster) state
3. Syncs resources to Kubernetes clusters
4. Manages application lifecycle (create, update, delete)
5. Provides deployment history and rollback

**Decision**: When to use?
- ✅ Application deployments
- ✅ Configuration updates
- ✅ Platform service updates
- ❌ Azure infrastructure (use Terraform/Crossplane)

### Layer 3: Resource Orchestrator (KRO)
**Role**: Translate high-level DSLs to Kubernetes resources

**Orchestrates**:
1. Receives high-level specifications (Application, Tenant, ToolPlatform)
2. Validates input against schemas
3. Generates multiple Kubernetes resources
4. Applies security policies and best practices
5. Creates resources in correct order with dependencies

**Example Flow**:
```
Developer creates Application DSL
           ↓
KRO receives Application CR
           ↓
KRO validates spec (image, resources, etc.)
           ↓
KRO generates:
  - Deployment (with security context)
  - Service (ClusterIP or LoadBalancer)
  - Ingress (with TLS)
  - HPA (autoscaling)
  - PDB (disruption budget)
  - NetworkPolicy (isolation)
  - ServiceMonitor (Prometheus)
           ↓
Resources created in Kubernetes
```

**Decision**: When to use?
- ✅ Application deployments
- ✅ Multi-resource patterns
- ✅ Enforcing standards
- ❌ Simple, one-off resources

### Layer 4: Infrastructure Provisioners

#### Terraform
**Role**: Provision and manage Azure infrastructure

**Orchestrates**:
- AKS cluster creation and configuration
- Networking (VNets, Subnets, NSGs)
- Azure services (Key Vault, ACR, Storage)
- RBAC and identity

**Lifecycle**:
```
terraform init
    ↓
terraform plan (review changes)
    ↓
terraform apply (provision)
    ↓
State stored in Azure Storage
    ↓
Day 2: terraform apply (updates)
```

**Decision**: When to use?
- ✅ Initial cluster provisioning
- ✅ Azure-specific resources
- ✅ Networking infrastructure
- ❌ Application deployments (use KRO/ArgoCD)

#### CAPZ (Cluster API Provider Azure)
**Role**: Kubernetes-native cluster management

**Orchestrates**:
- Create AKS clusters via Kubernetes CRs
- Manage node pools
- Upgrade clusters
- Scale operations

**Decision**: When to use?
- ✅ Scenario 2 (dedicated tool clusters)
- ✅ Dynamic cluster provisioning
- ✅ Kubernetes-native workflows
- ❌ Baseline clusters (use Terraform for stability)

#### Crossplane
**Role**: Provision cloud resources via Kubernetes APIs

**Orchestrates**:
- Azure databases, storage, networking
- Managed via Kubernetes CRDs
- GitOps-driven infrastructure

**Decision**: When to use?
- ✅ Application-tied infrastructure (DB per app)
- ✅ GitOps for infrastructure
- ✅ Self-service infrastructure
- ❌ Baseline infrastructure (use Terraform)

## Tool Selection Decision Tree

```
What are you provisioning?
    │
    ├─ Azure Infrastructure (VNets, AKS, Storage)?
    │  ├─ One-time/baseline? → Terraform
    │  └─ Dynamic/app-driven? → Crossplane or CAPZ
    │
    ├─ Kubernetes Applications?
    │  ├─ Simple pattern? → KRO DSL → ArgoCD
    │  ├─ Complex multi-cluster? → ArgoCD ApplicationSet
    │  └─ Raw manifests? → ArgoCD (but prefer KRO)
    │
    ├─ Dedicated AKS Cluster?
    │  ├─ Baseline/production? → Terraform
    │  └─ Dynamic/ephemeral? → CAPZ (Scenario 2)
    │
    └─ Platform Services (Ingress, Monitoring)?
       → ArgoCD (via Helm charts)
```

## Data Flow: Deploying an Application

### Step-by-Step Flow

```
1. Developer Action (Backstage)
   ├─ Fill out "Deploy Application" template
   ├─ Specify: name, image, resources, ingress
   └─ Click "Create"
        ↓
2. Template Execution
   ├─ Generate Git repository with Application CR
   ├─ Create catalog-info.yaml (Backstage metadata)
   ├─ Create ArgoCD Application manifest
   └─ Commit and push to GitHub
        ↓
3. ArgoCD Detection
   ├─ ArgoCD watches Git repository (polling every 3min)
   ├─ Detects new Application manifest
   └─ Initiates sync
        ↓
4. ArgoCD Sync
   ├─ Fetches manifests from Git
   ├─ Applies to Kubernetes API server
   └─ Creates Application CR in cluster
        ↓
5. KRO Processing
   ├─ KRO controller watches Application CRs
   ├─ Receives new Application
   ├─ Validates specification
   ├─ Generates child resources:
   │   ├─ Deployment
   │   ├─ Service
   │   ├─ Ingress
   │   ├─ HPA
   │   ├─ PDB
   │   ├─ NetworkPolicy
   │   └─ ServiceMonitor
   └─ Applies to Kubernetes
        ↓
6. Kubernetes Execution
   ├─ Deployment controller creates ReplicaSet
   ├─ ReplicaSet creates Pods
   ├─ Pods scheduled to nodes
   ├─ Containers started
   ├─ Service creates endpoints
   ├─ Ingress controller configures NGINX
   └─ Cert-Manager provisions TLS certificate
        ↓
7. Observability
   ├─ Prometheus scrapes metrics (ServiceMonitor)
   ├─ Logs shipped to Loki
   ├─ Traces sent to Tempo
   └─ Dashboards updated in Grafana
        ↓
8. Policy Enforcement
   ├─ OPA/Gatekeeper validates resources
   ├─ Azure Policy checks compliance
   └─ Alerts if violations detected
        ↓
9. Developer Visibility (Backstage)
   ├─ Catalog updated with new service
   ├─ ArgoCD sync status visible
   ├─ Kubernetes resources displayed
   ├─ Metrics and logs accessible
   └─ Tech Insights scorecard updated
```

**Total Time**: ~5-10 minutes (first deployment)

## Cluster Topology

### Multi-Cluster Strategy

```
┌────────────────────────────────────────────────────────┐
│  Control Plane Cluster (baseline-cluster1)             │
│  - ArgoCD                                              │
│  - KRO                                                 │
│  - Platform services                                   │
│  - Does NOT run application workloads                  │
└───────────────────┬────────────────────────────────────┘
                    │
                    │ Manages
                    │
    ┌───────────────┼────────────────┐
    │               │                │
    ▼               ▼                ▼
┌─────────┐  ┌─────────────┐  ┌─────────────┐
│  Dev    │  │  Staging    │  │ Production  │
│ Cluster │  │  Cluster    │  │  Cluster    │
│         │  │             │  │             │
│ Team A  │  │  Team A     │  │  Team A     │
│ Team B  │  │  Team B     │  │  Team B     │
│ Team C  │  │  Team C     │  │  Team C     │
└─────────┘  └─────────────┘  └─────────────┘

┌─────────────────────────────────────────────┐
│  Dedicated Clusters (Scenario 2)            │
│  - GitLab Runners                           │
│  - ArgoCD Platform                          │
│  - Security Scanning Tools                  │
│  Each isolated for security                 │
└─────────────────────────────────────────────┘
```

### When to Use Multi-Cluster

**Separate Clusters For**:
- ✅ Environments (dev, staging, production)
- ✅ Security boundaries (PCI, PHI data)
- ✅ Blast radius isolation
- ✅ Tools requiring K8s API access (Scenario 2)
- ✅ Different SLAs/availability zones

**Single Cluster With Namespaces For**:
- ✅ Team isolation (Scenario 3)
- ✅ Cost optimization (smaller workloads)
- ✅ Simplified management
- ✅ Non-production environments

## Security Architecture

### Defense in Depth

```
┌─────────────────────────────────────────────────────┐
│  Layer 7: Application Security                     │
│  - Code scanning (SAST/DAST)                        │
│  - Dependency scanning                              │
│  - Runtime protection (AppArmor/Seccomp)            │
└────────────────┬────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────┐
│  Layer 6: Pod Security                              │
│  - Pod Security Standards (restricted)              │
│  - Non-root users                                   │
│  - Read-only root filesystem                        │
│  - No privileged containers                         │
└────────────────┬────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────┐
│  Layer 5: Network Security                          │
│  - Network Policies (default deny)                  │
│  - Service mesh (mTLS)                              │
│  - Ingress TLS termination                          │
└────────────────┬────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────┐
│  Layer 4: Policy Enforcement                        │
│  - OPA Gatekeeper (admission control)               │
│  - Azure Policy (compliance)                        │
│  - Resource quotas                                  │
└────────────────┬────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────┐
│  Layer 3: Identity & Access                         │
│  - RBAC (least privilege)                           │
│  - Workload Identity (no service principal keys)    │
│  - Azure AD integration                             │
└────────────────┬────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────┐
│  Layer 2: Cluster Security                          │
│  - Private clusters                                 │
│  - Authorized IP ranges                             │
│  - Azure Firewall for egress                        │
│  - Audit logging enabled                            │
└────────────────┬────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────┐
│  Layer 1: Infrastructure Security                   │
│  - Encrypted disks                                  │
│  - Secure boot                                      │
│  - Network isolation (VNets, NSGs)                  │
│  - Azure Defender for Containers                    │
└─────────────────────────────────────────────────────┘
```

## Observability Architecture

```
┌────────────────────────────────────────────────────┐
│  Data Sources (Applications & Platform)            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Metrics │  │   Logs   │  │  Traces  │         │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘         │
└────────┼─────────────┼─────────────┼──────────────┘
         │             │             │
         ▼             ▼             ▼
┌────────────────────────────────────────────────────┐
│  Collection Layer                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  Prometheus  │  │    Fluent    │  │   OTEL   │ │
│  │              │  │     Bit      │  │Collector │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬────┘ │
└─────────┼──────────────────┼─────────────────┼─────┘
          │                  │                 │
          ▼                  ▼                 ▼
┌────────────────────────────────────────────────────┐
│  Storage Layer                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  Prometheus  │  │     Loki     │  │  Tempo   │ │
│  │   (TSDB)     │  │   (Logs)     │  │ (Traces) │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬────┘ │
└─────────┼──────────────────┼─────────────────┼─────┘
          │                  │                 │
          └──────────────────┴─────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────┐
│  Visualization Layer                               │
│  ┌─────────────────────────────────────────────┐   │
│  │             Grafana                         │   │
│  │  - Unified dashboards                       │   │
│  │  - Correlation across signals               │   │
│  │  - Alerting                                 │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘
```

## Deployment Patterns

### Pattern 1: Single Application (Scenario 1)
```
Git Commit → ArgoCD → KRO (Application) → K8s Resources
```

### Pattern 2: Multi-Environment
```
Git (main) → ArgoCD AppSet → Deployed to Dev, Staging, Prod
```

### Pattern 3: Infrastructure + Application
```
Terraform (AKS) → ArgoCD (Bootstrap) → KRO (Applications)
```

### Pattern 4: Progressive Delivery
```
Git → ArgoCD → Canary (10%) → Validation → Full Rollout
```

## Disaster Recovery

### Backup Strategy

**What to Back Up**:
- ✅ Git repositories (source of truth)
- ✅ Terraform state (Azure Storage with versioning)
- ✅ Kubernetes ETCD (AKS managed)
- ✅ Persistent volumes (Azure Disk snapshots)
- ✅ Secrets (Key Vault with soft delete)

**Recovery Time Objectives (RTO)**:
- Control Plane: 4 hours
- Application Cluster: 2 hours
- Individual Application: 15 minutes

**Recovery Point Objectives (RPO)**:
- Git: 0 (distributed)
- Terraform State: < 1 hour
- Application Data: < 15 minutes

### Recovery Process

1. **Cluster Lost**: Terraform recreate → ArgoCD sync (auto-recovery)
2. **Application Failed**: ArgoCD rollback to previous version
3. **Region Outage**: Failover to secondary region cluster

## Scaling the Platform

### Vertical Growth (More Features)
- Add new KRO ResourceGroups for patterns
- Integrate additional Azure services
- Enhance observability stack

### Horizontal Growth (More Teams)
- Multi-tenant namespaces (Scenario 3)
- Dedicated clusters per team (if needed)
- Regional clusters for compliance

### Performance Optimization
- ArgoCD sharding for large deployments
- Prometheus federation for metrics
- Separate clusters for workload types

## Resources

- [GitOps Bridge Pattern](https://github.com/gitops-bridge-dev/gitops-bridge)
- [KRO Documentation](https://kro.run/)
- [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [AKS Architecture](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/containers/aks/baseline-aks)

## Related Documentation

- [Golden Paths](./GOLDEN-PATHS.md)
- [Developer Experience](./DEVELOPER-EXPERIENCE.md)
- [Internal Developer Portal](./INTERNAL-DEVELOPER-PORTAL.md)
- [Team Topologies](./TEAM-TOPOLOGIES.md)
