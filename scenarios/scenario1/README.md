# Scenario 1: Application Deployment DSL

## Overview

This scenario provides a simple, declarative DSL for application teams to deploy their applications without managing Kubernetes complexity. The platform team ensures all deployments comply with security requirements and governance policies.

## Problem Statement

Application teams need to:
- Deploy containerized applications quickly
- Focus on application code, not infrastructure
- Comply with organizational security and governance policies
- Access their applications via HTTPS with automatic TLS

## Solution

Using KRO (Kubernetes Resource Orchestrator), we create a high-level abstraction called `Application` that:
1. Deploys the application with appropriate resource limits
2. Creates necessary services and ingress
3. Applies security policies automatically
4. Configures monitoring and logging
5. Sets up auto-scaling based on load

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Developer declares Application                          │
│  (Simple YAML with app requirements)                     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  KRO ResourceGroup: Application                          │
│  - Validates requirements                                │
│  - Applies security policies                             │
│  - Creates Kubernetes resources                          │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Platform automatically creates:                         │
│  ✓ Deployment with security context                     │
│  ✓ Service (ClusterIP/LoadBalancer)                     │
│  ✓ Ingress with TLS                                     │
│  ✓ HorizontalPodAutoscaler                              │
│  ✓ PodDisruptionBudget                                  │
│  ✓ NetworkPolicy                                        │
│  ✓ ServiceMonitor (Prometheus)                          │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

- Baseline AKS cluster deployed (see `baseline-clusters/`)
- KRO installed on the cluster
- NGINX Ingress Controller
- Cert-Manager for TLS certificates
- Prometheus for monitoring

## Quick Start

### 1. Install KRO ResourceGroup

```bash
kubectl apply -f kro-definitions/application-resourcegroup.yaml
```

### 2. Deploy an Application

```bash
kubectl apply -f examples/simple-web-app.yaml
```

### 3. Verify Deployment

```bash
# Check the Application resource
kubectl get applications

# Check created resources
kubectl get deployment,service,ingress -l app.kubernetes.io/managed-by=kro

# Access the application
kubectl get ingress my-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## Application DSL Reference

### Simple Example

```yaml
apiVersion: platform.example.com/v1alpha1
kind: Application
metadata:
  name: my-web-app
  namespace: dev-team-a
spec:
  image: myregistry.azurecr.io/my-app:v1.0.0
  replicas: 3
  port: 8080
  domain: my-app.example.com
  resources:
    cpu: 500m
    memory: 512Mi
```

### Advanced Example

```yaml
apiVersion: platform.example.com/v1alpha1
kind: Application
metadata:
  name: api-service
  namespace: dev-team-a
spec:
  # Container specification
  image: myregistry.azurecr.io/api-service:v2.1.0
  replicas: 5
  port: 8080
  
  # Resource requirements
  resources:
    cpu: 1000m
    memory: 2Gi
  
  # Networking
  domain: api.example.com
  serviceType: ClusterIP  # ClusterIP, LoadBalancer, NodePort
  
  # Auto-scaling
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPU: 70
    targetMemory: 80
  
  # Environment variables
  env:
    - name: DATABASE_URL
      value: "postgresql://db.example.com:5432/mydb"
    - name: LOG_LEVEL
      value: "info"
  
  # Secrets (mounted from existing Kubernetes secrets)
  secrets:
    - name: api-credentials
      mountPath: /etc/secrets
  
  # Health checks
  healthCheck:
    livenessPath: /healthz
    readinessPath: /ready
    initialDelaySeconds: 30
    periodSeconds: 10
  
  # Security settings
  security:
    runAsNonRoot: true
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
  
  # Ingress configuration
  ingress:
    enabled: true
    tls: true
    annotations:
      nginx.ingress.kubernetes.io/rate-limit: "100"
```

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `spec.image` | string | Yes | Container image with tag |
| `spec.replicas` | int | No | Number of replicas (default: 3) |
| `spec.port` | int | Yes | Container port |
| `spec.domain` | string | No | Domain name for ingress |
| `spec.resources.cpu` | string | No | CPU request/limit (default: 500m) |
| `spec.resources.memory` | string | No | Memory request/limit (default: 512Mi) |
| `spec.serviceType` | string | No | Service type (default: ClusterIP) |
| `spec.autoscaling.enabled` | bool | No | Enable HPA (default: false) |
| `spec.autoscaling.minReplicas` | int | No | Min replicas for HPA |
| `spec.autoscaling.maxReplicas` | int | No | Max replicas for HPA |
| `spec.env` | array | No | Environment variables |
| `spec.secrets` | array | No | Secret volume mounts |
| `spec.healthCheck` | object | No | Liveness/readiness probes |
| `spec.security` | object | No | Security context settings |
| `spec.ingress.enabled` | bool | No | Create ingress resource |
| `spec.ingress.tls` | bool | No | Enable TLS with cert-manager |

## Security & Governance

The platform automatically enforces:

### 1. Security Policies
- Containers run as non-root user
- Read-only root filesystem
- No privilege escalation
- Dropped Linux capabilities
- Security context constraints

### 2. Resource Governance
- CPU and memory limits enforced
- Pod disruption budgets for high availability
- Network policies for isolation
- Ingress rate limiting

### 3. Compliance
- All images must come from approved registries
- Mandatory labels for cost tracking
- Audit logging enabled
- Vulnerability scanning required

### 4. Observability
- Automatic Prometheus metrics scraping
- Log aggregation to central system
- Distributed tracing headers
- Health check endpoints required

## Examples

See the `examples/` directory for:
- Simple web application
- REST API service
- Background worker
- Multi-container application
- Database-backed application

## Troubleshooting

### Application not deploying

```bash
# Check Application status
kubectl describe application my-app

# Check KRO controller logs
kubectl logs -n kro-system -l app=kro-controller

# Check generated resources
kubectl get all -l app.kubernetes.io/name=my-app
```

### Ingress not accessible

```bash
# Check ingress status
kubectl get ingress my-app
kubectl describe ingress my-app

# Check cert-manager certificate
kubectl get certificate
kubectl describe certificate my-app-tls
```

## Next Steps

1. Review the [KRO ResourceGroup Definition](./kro-definitions/application-resourcegroup.yaml)
2. Deploy the [example applications](./examples/)
3. Customize the DSL for your organization's needs
4. Set up [policies and governance](./policies/)
5. Configure [monitoring and alerting](./monitoring/)

## Related Documentation

- [KRO Documentation](https://kro.run/docs)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Azure AKS Security](https://learn.microsoft.com/en-us/azure/aks/security-baseline)
