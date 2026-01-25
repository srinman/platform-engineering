# Golden Paths - Paved Roads for Platform Engineering

## Overview

Golden Paths (also called "Paved Roads") are the recommended, pre-approved patterns for common development tasks on our platform. They represent the easiest, most secure, and most compliant way to accomplish goals while maintaining flexibility for teams with special requirements.

## Philosophy

> "Make the right thing easy and the wrong thing hard (but not impossible)"

Golden Paths are designed to:
- **Reduce Cognitive Load**: Developers don't need to research every decision
- **Ensure Compliance**: Security and governance built-in by default
- **Enable Self-Service**: Clear, documented patterns for common tasks
- **Promote Consistency**: Standardized approaches across teams
- **Allow Escape Hatches**: Advanced teams can deviate when justified

## Core Principles

### 1. Default to Secure
All golden paths include security by default:
- Container image scanning
- Network policies
- Resource limits
- Non-root users
- Read-only root filesystems
- Secret management

### 2. Observable by Default
Every deployment includes:
- Prometheus metrics scraping
- Structured logging
- Distributed tracing integration
- Health check endpoints
- SLO monitoring

### 3. Scalable by Default
Standard patterns include:
- Horizontal Pod Autoscaling (HPA)
- Pod Disruption Budgets (PDB)
- Resource requests and limits
- Multiple replicas for HA

### 4. GitOps-Driven
All changes flow through Git:
- Infrastructure as Code
- Declarative configuration
- Automated sync
- Audit trail

## Golden Paths by Scenario

### 🌟 Golden Path 1: Deploying a Web Application

**When to Use**: Standard stateless web applications, APIs, services

**Recommended Pattern**: Scenario 1 - Application DSL

**Why This Path**:
- Simplest abstraction (just specify image, resources, and ingress)
- Security policies applied automatically
- Auto-scaling configured out-of-box
- TLS certificates managed automatically
- Monitoring and logging enabled by default

**Example**:
```yaml
apiVersion: platform.example.com/v1alpha1
kind: Application
metadata:
  name: my-api
  namespace: team-alpha
spec:
  image: myregistry.azurecr.io/my-api:v1.2.3
  replicas: 3
  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
    limits:
      cpu: "500m"
      memory: "512Mi"
  ingress:
    enabled: true
    hostname: api.example.com
    tls: true
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
```

**Time to Deploy**: ~15 minutes

**Compliance**: ✅ All security policies, ✅ Monitoring, ✅ HA configuration

**Enforcement**: 
- KRO validation ensures required fields
- Admission controllers prevent non-compliant configurations
- Scorecard checks validate best practices

---

### 🌟 Golden Path 2: Requesting Infrastructure (Clusters, Databases)

**When to Use**: Tools requiring dedicated clusters, external service integration

**Recommended Pattern**: Scenario 2 - ToolPlatform DSL

**Why This Path**:
- Isolated environments for security
- RBAC and networking pre-configured
- Integration with Azure services
- Cost tracking enabled

**Example**:
```yaml
apiVersion: platform.example.com/v1alpha1
kind: ToolPlatform
metadata:
  name: gitlab-runners
  namespace: devops-tools
spec:
  purpose: "GitLab CI/CD Runners"
  clusterSize: medium
  nodePool:
    vmSize: Standard_D4s_v3
    nodeCount: 3
  networking:
    vnetIntegration: true
    privateCluster: true
  tools:
    - name: gitlab-runner
      version: "16.5.0"
      rbacEnabled: true
```

**Time to Provision**: ~30 minutes

**Compliance**: ✅ Network isolation, ✅ RBAC, ✅ Cost allocation

---

### 🌟 Golden Path 3: Multi-Tenant Namespace

**When to Use**: Onboarding new teams, project isolation

**Recommended Pattern**: Scenario 3 - Tenant DSL

**Why This Path**:
- Resource quotas prevent noisy neighbors
- Network policies ensure isolation
- RBAC grants appropriate permissions
- Cost visibility per tenant

**Example**:
```yaml
apiVersion: platform.example.com/v1alpha1
kind: Tenant
metadata:
  name: team-beta
spec:
  owner: "team-beta@example.com"
  resourceQuota:
    cpu: "20"
    memory: "40Gi"
    pods: "50"
    storage: "100Gi"
  networkPolicy:
    isolation: true
    allowedNamespaces:
      - common-services
  rbac:
    adminUsers:
      - user1@example.com
      - user2@example.com
```

**Time to Onboard**: ~10 minutes

**Compliance**: ✅ Quotas, ✅ Network isolation, ✅ RBAC

---

### 🌟 Golden Path 4: ML/AI Workloads

**When to Use**: GPU-intensive workloads, model training, inference

**Recommended Pattern**: Scenario 4 - ML Platform

**Why This Path**:
- GPU node pools optimized for ML
- JupyterHub for experimentation
- Experiment tracking with MLflow
- Model registry integration

**Example**: See [Scenario 4 README](../scenarios/scenario4/README.md)

**Time to Deploy**: ~20 minutes

**Compliance**: ✅ GPU quotas, ✅ Cost tracking, ✅ Data governance

---

## Path Selection Decision Tree

```
┌─────────────────────────────────────┐
│   What are you deploying?           │
└─────────────┬───────────────────────┘
              │
              ├─ Stateless web app/API
              │  → Golden Path 1 (Application DSL)
              │
              ├─ Requires Kubernetes API access?
              │  → Golden Path 2 (ToolPlatform DSL)
              │
              ├─ New team onboarding?
              │  → Golden Path 3 (Tenant DSL)
              │
              ├─ ML/AI with GPUs?
              │  → Golden Path 4 (ML Platform)
              │
              └─ None of the above?
                 → Consult platform team (#platform-engineering)
```

## Enforcement and Validation

### Level 1: Design-Time Validation (KRO)
KRO ResourceGroups validate inputs:
- Required fields present
- Valid resource ranges
- Naming conventions
- Image from approved registries

### Level 2: Admission Control (OPA/Gatekeeper)
Policies enforce:
- No privileged containers
- Resource limits required
- Only approved image registries
- Labels required for cost allocation
- Network policies required

### Level 3: Continuous Compliance (Policy Controller)
Ongoing validation:
- Scan for drift from golden path
- Alert on non-compliant resources
- Generate compliance reports

### Level 4: Scorecard/Checks
Provide visibility:
- Application health score (0-100)
- Best practices adherence
- Security posture
- Observability coverage

**Example Scorecard**:
```
Application: my-api (team-alpha)
Overall Score: 85/100

✅ Security (95/100)
  ✅ Image from approved registry
  ✅ Non-root user
  ✅ Read-only root filesystem
  ⚠️  No AppArmor profile (-5)

✅ Reliability (90/100)
  ✅ Multiple replicas
  ✅ PodDisruptionBudget
  ✅ Liveness/Readiness probes
  ⚠️  No topology spread constraints (-10)

✅ Observability (75/100)
  ✅ Prometheus metrics
  ✅ Structured logs
  ❌ No tracing headers (-25)

⚠️  Cost Optimization (80/100)
  ✅ Resource requests set
  ✅ Autoscaling enabled
  ⚠️  No vertical pod autoscaler (-20)
```

## Escape Hatches: When to Deviate

Golden paths cover 80% of use cases. Deviations are allowed when:

1. **Technical Requirements**: Specific technology needs not covered by golden paths
2. **Performance**: Golden path doesn't meet performance requirements
3. **Cost**: Specific optimizations needed for cost reduction
4. **Innovation**: Experimenting with new approaches

**Deviation Process**:
1. Document why golden path doesn't work
2. Submit architectural decision record (ADR)
3. Platform team review and approval
4. Implement with additional scrutiny
5. Consider adding to golden paths if broadly applicable

**Example Deviation**:
```yaml
apiVersion: platform.example.com/v1alpha1
kind: Application
metadata:
  name: legacy-app
  namespace: team-gamma
  annotations:
    platform.example.com/deviation: "true"
    platform.example.com/deviation-reason: "Requires privileged access for hardware device"
    platform.example.com/deviation-approval: "ADR-2025-042"
spec:
  # ... configuration that deviates from golden path
  securityContext:
    privileged: true  # Normally forbidden
```

## Measuring Golden Path Adoption

Track adoption to identify gaps:

```bash
# Golden Path usage
kubectl get applications -A --show-labels | grep "platform.example.com/pattern=golden"

# Deviations
kubectl get applications -A -o json | \
  jq '[.items[] | select(.metadata.annotations["platform.example.com/deviation"] == "true")] | length'

# Adoption by team
kubectl get applications -A -o json | \
  jq 'group_by(.metadata.namespace) | 
      map({namespace: .[0].metadata.namespace, count: length})'
```

**Target**: >85% of applications use golden paths

## Documentation for Each Golden Path

Each golden path includes:
- [ ] **Quick Start**: 5-minute getting started guide
- [ ] **Reference**: Complete API documentation
- [ ] **Examples**: Real-world use cases
- [ ] **Migration Guide**: From raw Kubernetes
- [ ] **Troubleshooting**: Common issues and solutions
- [ ] **Runbooks**: Operational procedures

## Evolution of Golden Paths

Golden paths evolve through:

### Quarterly Review
- Analyze deviation patterns
- Survey developer satisfaction
- Review incident post-mortems
- Update based on new Azure/K8s features

### Version Management
- Semantic versioning (v1alpha1, v1beta1, v1)
- Deprecation policy (6-month notice)
- Migration guides between versions

### Communication
- Announce changes in #platform-engineering
- Update documentation
- Provide migration support
- Office hours for questions

## Anti-Patterns to Avoid

❌ **Don't**:
- Copy-paste raw Kubernetes YAML
- Deploy without resource limits
- Skip security scanning
- Bypass GitOps (kubectl apply directly)
- Deploy to production without testing
- Ignore scorecard warnings

✅ **Do**:
- Use the appropriate golden path DSL
- Let platform handle complexity
- Follow GitOps workflow
- Monitor scorecard and improve
- Ask questions in #platform-engineering

## Resources

- [Example Applications](../scenarios/scenario1/examples/)
- [KRO Documentation](https://kro.run/)
- [Developer Experience Guide](./DEVELOPER-EXPERIENCE.md)
- [Team Topologies](./TEAM-TOPOLOGIES.md)

## Getting Help

- **Documentation**: Start with scenario READMEs
- **Office Hours**: Tuesdays 2-3 PM
- **Slack**: #platform-engineering
- **Requests**: GitHub Issues with `golden-path` label
