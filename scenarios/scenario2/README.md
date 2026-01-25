# Scenario 2: 3rd Party Tool Platform

## Overview

This scenario demonstrates how to provision dedicated AKS clusters for running 3rd party tools that require Kubernetes API access. These tools are isolated in their own environments with specific security and networking configurations.

## Problem Statement

Platform teams need to:
- Deploy external tools (monitoring, security scanning, CI/CD platforms) that require K8s API access
- Isolate these tools from application workloads
- Provide proper RBAC and service accounts
- Maintain security boundaries while allowing tool functionality
- Make it easy to spin up new tool environments on demand

## Solution

Using KRO, we create a `ToolPlatform` abstraction that:
1. Provisions a dedicated AKS cluster via Azure Service Operator (ASO) or Crossplane
2. Configures networking and firewall rules
3. Sets up RBAC and service accounts
4. Deploys the tool with appropriate configurations
5. Provides access endpoints and credentials

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Platform Team declares ToolPlatform                      │
│  (Tool name, version, requirements)                       │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│  KRO ResourceGroup: ToolPlatform                          │
│  - Provisions AKS cluster                                 │
│  - Configures RBAC                                        │
│  - Deploys tool                                           │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│  Dedicated AKS Cluster                                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Tool Deployment (e.g., GitLab Runner, Argo CD)    │  │
│  │ - K8s API access                                   │  │
│  │ - Service Account with RBAC                        │  │
│  │ - Ingress for web UI                               │  │
│  │ - Persistent storage                               │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
│  Network Policies | RBAC | Azure AD Integration           │
└──────────────────────────────────────────────────────────┘
```

## Use Cases

1. **GitLab Runner Platform**: Isolated environment for CI/CD job execution
2. **Argo CD Platform**: GitOps deployment controller with cluster access
3. **Security Scanner Platform**: Tools like Trivy, Falco requiring K8s access
4. **Monitoring Platform**: Prometheus, Grafana with cluster-wide visibility
5. **Development Environments**: Temporary clusters for testing

## Prerequisites

- Control plane AKS cluster with CAPZ or Crossplane
- Azure credentials configured
- KRO installed
- Sufficient Azure quota for AKS clusters

## Quick Start

### 1. Install KRO ResourceGroup

```bash
kubectl apply -f kro-definitions/toolplatform-resourcegroup.yaml
```

### 2. Deploy a Tool Platform

```bash
# Example: Deploy GitLab Runner platform
kubectl apply -f examples/gitlab-runner-platform.yaml

# Example: Deploy Argo CD platform
kubectl apply -f examples/argocd-platform.yaml
```

### 3. Access the Tool

```bash
# Get cluster credentials
kubectl get toolplatform gitlab-runner -o jsonpath='{.status.kubeconfig}' | base64 -d > gitlab-runner-kubeconfig

# Access the tool
export KUBECONFIG=gitlab-runner-kubeconfig
kubectl get pods -n gitlab-runner
```

## ToolPlatform DSL Reference

### Simple Example

```yaml
apiVersion: platform.example.com/v1alpha1
kind: ToolPlatform
metadata:
  name: gitlab-runner
  namespace: platform-tools
spec:
  tool: gitlab-runner
  version: "16.5.0"
  clusterSize: small
```

### Advanced Example

```yaml
apiVersion: platform.example.com/v1alpha1
kind: ToolPlatform
metadata:
  name: argocd-platform
  namespace: platform-tools
spec:
  # Tool configuration
  tool: argocd
  version: "2.9.0"
  
  # Cluster configuration
  cluster:
    size: medium  # small, medium, large
    nodeCount: 3
    nodeSize: Standard_D4s_v3
    kubernetesVersion: "1.28.3"
    enableAutoUpgrade: true
    
    # Network configuration
    network:
      vnetAddressSpace: "10.2.0.0/16"
      subnetAddressSpace: "10.2.0.0/24"
      enablePrivateCluster: false
  
  # RBAC configuration
  rbac:
    - serviceAccount: argocd-application-controller
      clusterRole: cluster-admin  # Requires cluster-wide access
    - serviceAccount: argocd-server
      role: argocd-server
      namespace: argocd
  
  # Storage requirements
  storage:
    - name: argocd-repo-server
      size: 50Gi
      storageClass: managed-premium
  
  # Ingress configuration
  ingress:
    enabled: true
    domain: argocd.platform.example.com
    tls: true
    allowedIPs:
      - "10.0.0.0/8"      # Internal network
      - "203.0.113.0/24"  # Office IP range
  
  # Tool-specific configuration
  config:
    repositories:
      - url: https://github.com/myorg/gitops-repo
        type: git
    ssoEnabled: true
    ssoProvider: azure-ad
```

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `spec.tool` | string | Yes | Tool name (gitlab-runner, argocd, etc.) |
| `spec.version` | string | Yes | Tool version |
| `spec.cluster.size` | string | No | Cluster size preset (default: small) |
| `spec.cluster.nodeCount` | int | No | Number of nodes |
| `spec.cluster.nodeSize` | string | No | Azure VM size |
| `spec.cluster.kubernetesVersion` | string | No | Kubernetes version |
| `spec.cluster.network.vnetAddressSpace` | string | No | VNet CIDR |
| `spec.rbac` | array | No | RBAC configurations |
| `spec.storage` | array | No | Persistent volume requirements |
| `spec.ingress` | object | No | Ingress configuration |
| `spec.config` | object | No | Tool-specific settings |

## Supported Tools

### 1. GitLab Runner
- Executes CI/CD jobs
- Requires: API access for pod creation
- RBAC: Namespace admin in `gitlab-runner` namespace

### 2. Argo CD
- GitOps continuous deployment
- Requires: Cluster-wide read, namespace write
- RBAC: Cluster-admin or custom ClusterRole

### 3. Trivy Operator
- Kubernetes security scanner
- Requires: Read access to all namespaces
- RBAC: Cluster-wide read

### 4. Prometheus + Grafana
- Monitoring and observability
- Requires: Metrics access cluster-wide
- RBAC: Read-only cluster access

### 5. Falco
- Runtime security monitoring
- Requires: Node-level access
- RBAC: DaemonSet privileges

## Cluster Size Presets

### Small
- Nodes: 2
- VM Size: Standard_D2s_v3
- Use Case: Development, lightweight tools

### Medium
- Nodes: 3
- VM Size: Standard_D4s_v3
- Use Case: Production tools, moderate load

### Large
- Nodes: 5
- VM Size: Standard_D8s_v3
- Use Case: Heavy workloads, enterprise tools

## Security Considerations

### 1. Network Isolation
- Dedicated VNet for each tool platform
- VNet peering for controlled access
- Network policies enforced
- Private endpoints for Azure services

### 2. RBAC Best Practices
- Least privilege principle
- Service accounts per component
- Regular RBAC audits
- Azure AD integration for user access

### 3. Secrets Management
- Azure Key Vault integration
- Workload Identity for authentication
- Secrets rotation policies
- No plaintext secrets in Git

### 4. Compliance
- Audit logging enabled
- Azure Policy enforcement
- Defender for Containers
- Regular security scanning

## Examples

### GitLab Runner Platform

```yaml
apiVersion: platform.example.com/v1alpha1
kind: ToolPlatform
metadata:
  name: gitlab-runner
  namespace: platform-tools
spec:
  tool: gitlab-runner
  version: "16.5.0"
  
  cluster:
    size: medium
    nodeCount: 3
  
  rbac:
    - serviceAccount: gitlab-runner
      role: gitlab-runner-manager
      namespace: gitlab-runner
  
  config:
    gitlabUrl: https://gitlab.example.com
    concurrent: 10
    checkInterval: 3
```

### Argo CD Platform

```yaml
apiVersion: platform.example.com/v1alpha1
kind: ToolPlatform
metadata:
  name: argocd
  namespace: platform-tools
spec:
  tool: argocd
  version: "2.9.0"
  
  cluster:
    size: medium
  
  rbac:
    - serviceAccount: argocd-application-controller
      clusterRole: cluster-admin
  
  ingress:
    enabled: true
    domain: argocd.example.com
    tls: true
  
  config:
    ssoEnabled: true
    ssoProvider: azure-ad
```

## Troubleshooting

### Cluster provisioning failed

```bash
# Check ToolPlatform status
kubectl describe toolplatform gitlab-runner

# Check infrastructure provider logs (CAPZ/Crossplane)
kubectl logs -n capz-system -l control-plane=capz-controller-manager
```

### Tool not accessible

```bash
# Verify ingress
kubectl --kubeconfig=tool-kubeconfig get ingress -A

# Check service
kubectl --kubeconfig=tool-kubeconfig get svc -A
```

### RBAC issues

```bash
# Verify service accounts
kubectl --kubeconfig=tool-kubeconfig get sa -A

# Check role bindings
kubectl --kubeconfig=tool-kubeconfig get rolebindings,clusterrolebindings -A
```

## Cleanup

```bash
# Delete the tool platform (removes cluster)
kubectl delete toolplatform gitlab-runner

# Verify Azure resources are cleaned up
az aks list -g <resource-group>
```

## Next Steps

1. Review [KRO ResourceGroup Definition](./kro-definitions/toolplatform-resourcegroup.yaml)
2. Deploy [example platforms](./examples/)
3. Customize [tool configurations](./configs/)
4. Set up [monitoring](./monitoring/)
5. Configure [backup and DR](./backup/)

## Related Documentation

- [KRO Documentation](https://kro.run/docs)
- [Azure Service Operator](https://azure.github.io/azure-service-operator/)
- [Crossplane Azure Provider](https://marketplace.upbound.io/providers/upbound/provider-azure/)
