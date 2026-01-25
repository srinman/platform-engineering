# Internal Developer Portal (IDP) Integration

## Overview

An Internal Developer Portal (IDP) provides a unified interface for developers to discover services, access documentation, deploy applications, and manage their infrastructure. This guide shows how to integrate our AKS platform with an IDP, specifically using [Backstage](https://backstage.io/).

## What is an Internal Developer Portal?

An IDP is the front door to your platform engineering efforts. It provides:

- **Service Catalog**: Discover all services, APIs, and infrastructure
- **Software Templates**: Scaffold new projects with golden path patterns
- **Documentation Hub**: Centralized, searchable documentation
- **Tech Insights**: View health, compliance, and metrics
- **Self-Service Actions**: Trigger deployments, create resources, etc.

## Why Backstage?

Backstage is the leading open-source IDP, created by Spotify and now a CNCF project:

✅ **Extensible**: Plugin architecture for custom functionality  
✅ **CNCF**: Cloud-native, Kubernetes-friendly  
✅ **Active Community**: 100+ plugins available  
✅ **GitOps Native**: Integrates well with ArgoCD  
✅ **Azure Support**: Official Azure plugins available

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Backstage (Internal Developer Portal)              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Service  │ │ Software │ │   Tech   │           │
│  │ Catalog  │ │ Templates│ │ Insights │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       │            │            │                  │
└───────┼────────────┼────────────┼──────────────────┘
        │            │            │
        ▼            ▼            ▼
┌───────────────────────────────────────────────────┐
│  Platform (AKS Clusters)                          │
│  ┌──────────────┐  ┌──────────────┐              │
│  │   ArgoCD     │  │  Kubernetes  │              │
│  │   (GitOps)   │  │  (KRO DSLs)  │              │
│  └──────────────┘  └──────────────┘              │
│                                                   │
│  ┌──────────────┐  ┌──────────────┐              │
│  │ Prometheus   │  │  Azure APIs  │              │
│  │ (Metrics)    │  │ (Cloud Res.) │              │
│  └──────────────┘  └──────────────┘              │
└───────────────────────────────────────────────────┘
```

## Deployment Options

### Option 1: Backstage on AKS (Recommended)

Deploy Backstage as an application on your platform:

```yaml
# Deploy using Scenario 1 Application DSL
apiVersion: platform.example.com/v1alpha1
kind: Application
metadata:
  name: backstage
  namespace: platform-services
spec:
  image: <your-registry>/backstage:latest
  replicas: 3
  resources:
    requests:
      cpu: "500m"
      memory: "512Mi"
    limits:
      cpu: "2000m"
      memory: "2Gi"
  ingress:
    enabled: true
    hostname: developer-portal.example.com
    tls: true
  env:
    - name: POSTGRES_HOST
      value: backstage-postgresql
    - name: BACKSTAGE_BASE_URL
      value: https://developer-portal.example.com
```

### Option 2: Azure Container Apps

For simplified management outside AKS:

```bash
az containerapp create \
  --name backstage \
  --resource-group platform-rg \
  --environment platform-env \
  --image <your-registry>/backstage:latest \
  --target-port 7007 \
  --ingress external \
  --min-replicas 2 \
  --max-replicas 10
```

## Setting Up Backstage

### 1. Initialize Backstage App

```bash
npx @backstage/create-app@latest

cd backstage

# Install Azure and Kubernetes plugins
yarn add --cwd packages/app \
  @backstage/plugin-azure-devops \
  @backstage/plugin-kubernetes \
  @backstage/plugin-tech-insights \
  @backstage/plugin-cost-insights \
  @roadiehq/backstage-plugin-argo-cd
```

### 2. Configure Service Catalog

**app-config.yaml**:
```yaml
catalog:
  providers:
    # Auto-discover from Git repositories
    github:
      providerId:
        organization: 'your-org'
        catalogPath: '/catalog-info.yaml'
        filters:
          branch: 'main'
          repository: '.*'
      schedule:
        frequency: { minutes: 5 }
        timeout: { minutes: 3 }
    
    # Kubernetes resources
    kubernetes:
      serviceLocatorMethod:
        type: 'multiTenant'
      clusterLocatorMethods:
        - type: 'config'
          clusters:
            - url: https://aks-cluster1.example.com
              name: baseline-cluster1
              authProvider: 'azure'
              serviceAccountToken: ${K8S_TOKEN}

  # Import baseline catalogs
  locations:
    - type: url
      target: https://github.com/your-org/platform-engineering/blob/main/catalog/systems.yaml
    - type: url
      target: https://github.com/your-org/platform-engineering/blob/main/catalog/components.yaml
```

### 3. Create Software Templates

Templates enable developers to create new applications using golden paths:

**templates/application-template.yaml**:
```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: aks-application
  title: Deploy Application on AKS
  description: Create a new application using the Application DSL (Scenario 1)
  tags:
    - kubernetes
    - aks
    - application
spec:
  owner: platform-team
  type: service
  
  parameters:
    - title: Application Details
      required:
        - name
        - namespace
        - image
      properties:
        name:
          title: Application Name
          type: string
          description: Name of your application
          pattern: '^[a-z0-9-]+$'
        namespace:
          title: Namespace
          type: string
          description: Kubernetes namespace
          enum:
            - team-alpha
            - team-beta
            - team-gamma
        image:
          title: Container Image
          type: string
          description: Full image path with tag
          default: myregistry.azurecr.io/my-app:latest
    
    - title: Resource Configuration
      properties:
        replicas:
          title: Initial Replicas
          type: integer
          default: 3
          minimum: 1
          maximum: 10
        cpu:
          title: CPU Request
          type: string
          default: "100m"
        memory:
          title: Memory Request
          type: string
          default: "128Mi"
    
    - title: Ingress Configuration
      properties:
        ingressEnabled:
          title: Enable Ingress
          type: boolean
          default: true
        hostname:
          title: Hostname
          type: string
          description: DNS hostname for the application
  
  steps:
    - id: fetch-base
      name: Fetch Application Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          namespace: ${{ parameters.namespace }}
          image: ${{ parameters.image }}
          replicas: ${{ parameters.replicas }}
          cpu: ${{ parameters.cpu }}
          memory: ${{ parameters.memory }}
          hostname: ${{ parameters.hostname }}
    
    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: Application ${{ parameters.name }}
        repoUrl: github.com?owner=your-org&repo=${{ parameters.name }}
        defaultBranch: main
    
    - id: register
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'
    
    - id: create-argocd-app
      name: Create ArgoCD Application
      action: argocd:create-app
      input:
        appName: ${{ parameters.name }}
        namespace: ${{ parameters.namespace }}
        repoUrl: ${{ steps.publish.output.remoteUrl }}
        path: manifests

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: ArgoCD Application
        url: https://argocd.example.com/applications/${{ parameters.name }}
      - title: View in Catalog
        icon: catalog
        entityRef: ${{ steps.register.output.entityRef }}
```

**templates/application-template/skeleton/manifests/application.yaml**:
```yaml
apiVersion: platform.example.com/v1alpha1
kind: Application
metadata:
  name: ${{ values.name }}
  namespace: ${{ values.namespace }}
spec:
  image: ${{ values.image }}
  replicas: ${{ values.replicas }}
  resources:
    requests:
      cpu: "${{ values.cpu }}"
      memory: "${{ values.memory }}"
  {% if values.ingressEnabled %}
  ingress:
    enabled: true
    hostname: ${{ values.hostname }}
    tls: true
  {% endif %}
  autoscaling:
    enabled: true
    minReplicas: ${{ values.replicas }}
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
```

### 4. Configure Tech Insights

Show compliance and health scores:

**tech-insights-checks.yaml**:
```yaml
apiVersion: techinsights.backstage.io/v1alpha1
kind: Check
metadata:
  name: golden-path-compliance
  title: Golden Path Compliance
spec:
  type: json-rules-engine
  description: Validates application follows golden path patterns
  factIds:
    - has-resource-limits
    - has-ingress-tls
    - has-multiple-replicas
    - has-monitoring
  rule:
    conditions:
      all:
        - fact: has-resource-limits
          operator: equal
          value: true
        - fact: has-ingress-tls
          operator: equal
          value: true
        - fact: has-multiple-replicas
          operator: equal
          value: true
        - fact: has-monitoring
          operator: equal
          value: true
```

### 5. Integrate with ArgoCD

Display ArgoCD sync status in service pages:

```typescript
// packages/app/src/components/catalog/EntityPage.tsx
import { EntityArgoCDContent } from '@roadiehq/backstage-plugin-argo-cd';

const serviceEntityPage = (
  <EntityLayout>
    <EntityLayout.Route path="/" title="Overview">
      <Grid container spacing={3}>
        {/* ... other cards ... */}
        <Grid item md={6}>
          <EntityArgoCDHistoryCard />
        </Grid>
      </Grid>
    </EntityLayout.Route>
    
    <EntityLayout.Route path="/argocd" title="ArgoCD">
      <EntityArgoCDContent />
    </EntityLayout.Route>
  </EntityLayout>
);
```

## Service Catalog Structure

Organize your platform services in the catalog:

**catalog/systems.yaml**:
```yaml
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: aks-platform
  title: AKS Platform Engineering
  description: Internal developer platform on Azure Kubernetes Service
spec:
  owner: platform-team
  domain: platform
---
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: customer-api
  title: Customer API System
  description: Customer-facing API services
spec:
  owner: team-alpha
  domain: customer-experience
```

**catalog/components.yaml**:
```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: api-service
  title: Customer API Service
  description: RESTful API for customer operations
  annotations:
    github.com/project-slug: your-org/api-service
    backstage.io/kubernetes-label-selector: 'app=api-service'
    argocd/app-name: api-service
  tags:
    - api
    - customer
  links:
    - url: https://api.example.com/docs
      title: API Documentation
      icon: docs
spec:
  type: service
  lifecycle: production
  owner: team-alpha
  system: customer-api
  providesApis:
    - customer-api-v1
```

## Key Features for Developers

### 1. Service Discovery
Browse all services, APIs, and infrastructure components with:
- Owner information
- Dependencies
- Documentation links
- Health status
- Deployment info

### 2. Golden Path Templates
One-click application creation:
- Choose template (Application, ToolPlatform, Tenant)
- Fill form with requirements
- Automatic repository creation
- GitOps setup included
- ArgoCD application created

### 3. Documentation Portal
Centralized docs with:
- Search across all documentation
- Version management
- Auto-generated API docs
- Runbooks and guides

### 4. Tech Insights Dashboard
View compliance scores:
- Security posture
- Best practices adherence
- Cost optimization
- Performance metrics

### 5. Self-Service Actions
Trigger platform operations:
- Deploy new version
- Scale application
- Create database
- Request resources

## Cost Insights Integration

Track spending per team/service:

**app-config.yaml**:
```yaml
costInsights:
  engineerCost: 200000  # Annual cost per engineer
  products:
    computeEngine:
      name: Azure Kubernetes Service
      icon: compute
  metrics:
    - kind: COST_TOTAL
    - kind: COST_PER_PRODUCT
  currencies:
    - kind: USD
      label: 'US Dollars'
      unit: '$'
```

## Authentication & Authorization

### Azure AD Integration

```yaml
auth:
  environment: production
  providers:
    microsoft:
      development:
        clientId: ${AUTH_MICROSOFT_CLIENT_ID}
        clientSecret: ${AUTH_MICROSOFT_CLIENT_SECRET}
        tenantId: ${AUTH_MICROSOFT_TENANT_ID}

# RBAC based on Azure AD groups
permission:
  enabled: true
  rbac:
    policies-csv-file: /rbac/policies.csv
```

**rbac/policies.csv**:
```csv
p, role:platform-admin, catalog-entity, read, allow
p, role:platform-admin, catalog-entity, create, allow
p, role:platform-admin, catalog-entity, update, allow
p, role:platform-admin, catalog-entity, delete, allow
p, role:developer, catalog-entity, read, allow
p, role:developer, scaffolder-template, use, allow

g, user:platform-team@example.com, role:platform-admin
g, group:developers, role:developer
```

## Metrics and Monitoring

Track IDP usage:

```yaml
backend:
  plugins:
    - prometheus:
        path: /metrics
        collectDefaultMetrics: true
```

**Key Metrics**:
- Active users per day/week
- Template usage by type
- Service catalog size
- Search queries
- Page load times
- Self-service action success rate

## Deployment Guide

### Build Custom Backstage Image

**Dockerfile**:
```dockerfile
FROM node:18-bullseye-slim as build

WORKDIR /app
COPY package*.json yarn.lock ./
COPY packages packages

RUN yarn install --frozen-lockfile
RUN yarn build:backend

FROM node:18-bullseye-slim

WORKDIR /app
COPY --from=build /app/packages/backend/dist ./
COPY app-config.yaml ./

ENV NODE_ENV production
EXPOSE 7007

CMD ["node", "packages/backend"]
```

### Build and Push

```bash
# Build image
docker build -t myregistry.azurecr.io/backstage:v1.0.0 .

# Push to ACR
az acr login --name myregistry
docker push myregistry.azurecr.io/backstage:v1.0.0
```

### Deploy to AKS

```bash
# Using Application DSL (Scenario 1)
kubectl apply -f - <<EOF
apiVersion: platform.example.com/v1alpha1
kind: Application
metadata:
  name: backstage
  namespace: platform-services
spec:
  image: myregistry.azurecr.io/backstage:v1.0.0
  replicas: 3
  resources:
    requests:
      cpu: "500m"
      memory: "512Mi"
    limits:
      cpu: "2000m"
      memory: "2Gi"
  ingress:
    enabled: true
    hostname: developer-portal.example.com
    tls: true
  env:
    - name: POSTGRES_HOST
      value: backstage-postgresql.platform-services.svc.cluster.local
    - name: BACKSTAGE_BASE_URL
      value: https://developer-portal.example.com
EOF
```

## Best Practices

✅ **Do**:
- Keep service catalog updated automatically
- Use templates for all golden paths
- Integrate with existing tools (ArgoCD, Prometheus)
- Collect user feedback regularly
- Measure adoption metrics
- Provide training and onboarding

❌ **Don't**:
- Make it too complex (start simple)
- Ignore performance (optimize for speed)
- Duplicate documentation (single source of truth)
- Require manual catalog updates
- Block deployments through IDP

## Resources

### Official Documentation
- [Backstage Documentation](https://backstage.io/docs)
- [Backstage Plugins](https://backstage.io/plugins)
- [Backstage on AKS](https://learn.microsoft.com/en-us/azure/architecture/guide/backstage/backstage-azure)

### Community
- [Backstage Discord](https://discord.gg/backstage)
- [CNCF Slack #backstage](https://cloud-native.slack.com)

### Related Platform Docs
- [Golden Paths](./GOLDEN-PATHS.md)
- [Developer Experience](./DEVELOPER-EXPERIENCE.md)
- [Team Topologies](./TEAM-TOPOLOGIES.md)

## Getting Started

1. Deploy Backstage to your platform
2. Import existing services to catalog
3. Create templates for golden paths
4. Integrate with ArgoCD
5. Train teams on IDP usage
6. Collect feedback and iterate

Questions? Join #platform-engineering on Slack!
