# Scenario 3: Multi-Tenant Application Platform

## Overview

This scenario demonstrates how to build a multi-tenant platform where multiple application teams share infrastructure while maintaining isolation, security boundaries, and resource quotas.

## Problem Statement

Platform teams need to:
- Host multiple teams on shared AKS infrastructure
- Provide isolation between teams
- Enforce resource quotas and cost allocation
- Maintain security boundaries
- Enable team self-service within guardrails

## Solution

Using KRO, we create a `Tenant` abstraction that:
1. Creates a dedicated namespace per team
2. Sets up RBAC for team members
3. Enforces resource quotas
4. Applies network policies for isolation
5. Configures cost tracking labels
6. Provides monitoring dashboards per tenant

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Shared AKS Cluster                                       │
│                                                            │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │ Tenant: Team A  │  │ Tenant: Team B  │               │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │               │
│  │ │ Namespace   │ │  │ │ Namespace   │ │               │
│  │ │ - Apps      │ │  │ │ - Apps      │ │               │
│  │ │ - Quotas    │ │  │ │ - Quotas    │ │               │
│  │ │ - RBAC      │ │  │ │ - RBAC      │ │               │
│  │ │ - NetPol    │ │  │ │ - NetPol    │ │               │
│  │ └─────────────┘ │  │ └─────────────┘ │               │
│  └─────────────────┘  └─────────────────┘               │
│                                                            │
│  Shared Services: Ingress, Monitoring, Logging            │
└──────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install KRO ResourceGroup

```bash
kubectl apply -f kro-definitions/tenant-resourcegroup.yaml
```

### 2. Onboard a Team

```bash
kubectl apply -f examples/team-a-tenant.yaml
```

### 3. Team Deploys Applications

```bash
# Team members use their namespace
kubectl config set-context --current --namespace=team-a
kubectl apply -f my-app.yaml
```

## Tenant DSL Reference

### Example

```yaml
apiVersion: platform.example.com/v1alpha1
kind: Tenant
metadata:
  name: team-a
spec:
  # Team information
  displayName: "Team Alpha"
  contactEmail: team-a@example.com
  costCenter: "CC-1234"
  
  # Resource quotas
  quota:
    cpu: "20"
    memory: "40Gi"
    pods: "100"
    services: "20"
    persistentVolumeClaims: "10"
    storage: "500Gi"
  
  # Team members (Azure AD integration)
  members:
    - email: alice@example.com
      role: admin
    - email: bob@example.com
      role: developer
  
  # Network policies
  networking:
    allowedNamespaces:
      - team-b  # Allow traffic from team-b
    egressRules:
      - to: internet
        ports: [80, 443]
      - to: azure-services
  
  # Ingress configuration
  ingress:
    enabled: true
    baseDomain: team-a.apps.example.com
    tls: true
  
  # Monitoring and alerts
  monitoring:
    enabled: true
    alertEmail: team-a-oncall@example.com
