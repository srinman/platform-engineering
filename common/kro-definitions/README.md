# Common KRO Definitions

This directory contains reusable KRO ResourceGroup definitions that can be used across multiple scenarios.

## Available ResourceGroups

### 1. Application
A high-level abstraction for deploying applications with built-in security, governance, and observability.

**Used in**: Scenario 1

### 2. ToolPlatform
Provisions dedicated AKS clusters for 3rd party tools with K8s API access.

**Used in**: Scenario 2

### 3. Tenant
Creates multi-tenant namespaces with resource quotas, RBAC, and network policies.

**Used in**: Scenario 3

### 4. MLPlatform
Specialized platform for ML/AI workloads with GPU support and MLOps tools.

**Used in**: Scenario 4

## Usage

These KRO definitions are referenced by the scenarios. You can:

1. Use them as-is
2. Extend them for your needs
3. Create new custom ResourceGroups

## Installing KRO

```bash
# Install KRO controller
kubectl apply -f https://github.com/kro-run/kro/releases/latest/download/kro.yaml

# Verify installation
kubectl get pods -n kro-system
```

## Creating a Custom ResourceGroup

```yaml
apiVersion: kro.run/v1alpha1
kind: ResourceGroup
metadata:
  name: my-custom-resource
  namespace: kro-system
spec:
  schema:
    apiVersion: platform.example.com/v1alpha1
    kind: MyCustomResource
    spec:
      # Define your schema
      field1: string
      field2: integer
  
  resources:
    # Define resources to create
    - id: resource1
      template:
        # Kubernetes resource template
```

## Best Practices

1. **Version your APIs**: Use versioned API groups (v1alpha1, v1beta1, v1)
2. **Provide defaults**: Make fields optional with sensible defaults
3. **Validate inputs**: Use schema validation where possible
4. **Document fields**: Include descriptions in your CRDs
5. **Test thoroughly**: Test ResourceGroups before deploying to production
