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
  
  # Cost management
  cost:
    budgetAlert:
      enabled: true
      monthlyLimit: "5000"  # USD
      alertThresholds: [50, 80, 100]  # Percentage of budget
    showbackEnabled: true
    costAllocationTags:
      environment: "production"
      businessUnit: "engineering"
```

## Cost Optimization and Tracking

### Overview

Scenario 3 includes comprehensive cost management features:
- **Cost Allocation**: Tag all resources for accurate cost tracking
- **Budget Alerts**: Notify teams when approaching budget limits
- **Showback/Chargeback**: Report costs per tenant for billing
- **Cost Optimization**: Identify and eliminate waste

### Cost Tracking Implementation

#### 1. Resource Labeling

All resources created by the Tenant ResourceGroup are automatically labeled:

```yaml
metadata:
  labels:
    platform.example.com/tenant: team-a
    platform.example.com/cost-center: CC-1234
    platform.example.com/environment: production
    platform.example.com/managed-by: kro
```

These labels enable:
- Filtering in Prometheus queries
- Cost allocation in cloud billing
- Resource ownership tracking

#### 2. OpenCost Integration

Deploy OpenCost to track Kubernetes costs:

```bash
# Install OpenCost
helm install opencost opencost/opencost \
  --namespace opencost --create-namespace \
  --set opencost.prometheus.internal.serviceName=prometheus-server \
  --set opencost.cloudProviderApiKey=$AZURE_API_KEY
```

**Query Costs by Tenant**:

```bash
# Get cost for team-a namespace
curl "http://opencost:9003/allocation/compute?window=7d&aggregate=namespace&filter=namespace:team-a"
```

**Sample Response**:
```json
{
  "team-a": {
    "cpuCost": 245.32,
    "memoryCost": 189.45,
    "pvCost": 67.80,
    "networkCost": 23.15,
    "totalCost": 525.72,
    "cpuCoreHours": 1680.5,
    "ramGBHours": 3360.0
  }
}
```

#### 3. Budget Alerts

Configure budget alerts using Azure Cost Management:

```hcl
# Terraform configuration
resource "azurerm_consumption_budget_resource_group" "team_a" {
  name              = "team-a-budget"
  resource_group_id = azurerm_resource_group.aks.id

  amount     = 5000
  time_grain = "Monthly"

  time_period {
    start_date = "2026-01-01T00:00:00Z"
  }

  notification {
    enabled   = true
    threshold = 50.0
    operator  = "GreaterThan"

    contact_emails = [
      "team-a@example.com",
    ]
  }

  notification {
    enabled   = true
    threshold = 80.0
    operator  = "GreaterThan"

    contact_emails = [
      "team-a@example.com",
      "platform-team@example.com",
    ]
  }

  notification {
    enabled   = true
    threshold = 100.0
    operator  = "GreaterThan"

    contact_emails = [
      "team-a@example.com",
      "platform-team@example.com",
      "finance@example.com",
    ]
  }

  filter {
    tag {
      name = "platform.example.com/tenant"
      values = ["team-a"]
    }
  }
}
```

#### 4. Cost Dashboard (Grafana)

Create tenant-specific cost dashboards:

**Grafana Dashboard JSON** (simplified):
```json
{
  "dashboard": {
    "title": "Team A - Cost Dashboard",
    "panels": [
      {
        "title": "Monthly Cost Trend",
        "targets": [{
          "expr": "sum(opencost_allocation_total{namespace=\"team-a\"}) by (resource_type)"
        }]
      },
      {
        "title": "Cost by Resource Type",
        "targets": [{
          "expr": "sum(opencost_allocation_cpu_cost{namespace=\"team-a\"}) + sum(opencost_allocation_memory_cost{namespace=\"team-a\"}) + sum(opencost_allocation_pv_cost{namespace=\"team-a\"})"
        }]
      },
      {
        "title": "Budget vs Actual",
        "targets": [{
          "expr": "(sum(opencost_allocation_total{namespace=\"team-a\"}) / 5000) * 100"
        }]
      },
      {
        "title": "Top 10 Expensive Workloads",
        "targets": [{
          "expr": "topk(10, sum by (pod) (opencost_allocation_total{namespace=\"team-a\"}))"
        }]
      }
    ]
  }
}
```

Access dashboard:
```bash
# Port-forward to Grafana
kubectl port-forward -n monitoring svc/grafana 3000:80

# Open http://localhost:3000/d/team-a-costs
```

#### 5. Showback Reports

Generate monthly showback reports:

```bash
#!/bin/bash
# generate-showback-report.sh

TENANT="team-a"
MONTH=$(date -d "last month" +%Y-%m)

# Get costs from OpenCost
COSTS=$(curl -s "http://opencost:9003/allocation/compute?window=month&aggregate=namespace&filter=namespace:${TENANT}")

# Extract values
CPU_COST=$(echo $COSTS | jq -r ".${TENANT}.cpuCost")
MEM_COST=$(echo $COSTS | jq -r ".${TENANT}.memoryCost")
PV_COST=$(echo $COSTS | jq -r ".${TENANT}.pvCost")
NET_COST=$(echo $COSTS | jq -r ".${TENANT}.networkCost")
TOTAL=$(echo $COSTS | jq -r ".${TENANT}.totalCost")

# Generate report
cat > "${TENANT}-${MONTH}-report.md" <<EOF
# Cost Report: ${TENANT}
**Period**: ${MONTH}

## Summary
- **Total Cost**: \$${TOTAL}
- **CPU**: \$${CPU_COST}
- **Memory**: \$${MEM_COST}
- **Storage**: \$${PV_COST}
- **Network**: \$${NET_COST}

## Resource Usage
- CPU Hours: $(echo $COSTS | jq -r ".${TENANT}.cpuCoreHours")
- Memory GB-Hours: $(echo $COSTS | jq -r ".${TENANT}.ramGBHours")

## Top Consumers
$(kubectl top pods -n ${TENANT} --sort-by=cpu | head -10)

## Recommendations
- Consider rightsizing workloads with low utilization
- Review persistent volume usage
- Enable autoscaling for variable workloads
EOF

echo "Report generated: ${TENANT}-${MONTH}-report.md"
```

**Automated Monthly Delivery**:
```yaml
# CronJob to generate and email reports
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cost-report-generator
  namespace: platform-services
spec:
  schedule: "0 0 1 * *"  # First day of each month
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: report-generator
            image: opencost/opencost:latest
            command:
            - /bin/sh
            - -c
            - |
              ./generate-showback-report.sh
              # Email report
              cat report.md | mail -s "Monthly Cost Report" team-a@example.com
          restartPolicy: OnFailure
```

#### 6. Chargeback Model

For organizations requiring chargeback (actual billing):

**Cost Allocation Formula**:
```
Team Cost = (Namespace CPU Cost + Namespace Memory Cost + 
             Namespace Storage Cost + Namespace Network Cost) * 
            Markup Factor
```

**Example Calculation**:
```python
# chargeback.py
import requests
import json

def calculate_chargeback(tenant, markup=1.15):
    """
    Calculate chargeback with 15% platform overhead
    """
    # Get OpenCost data
    response = requests.get(
        f"http://opencost:9003/allocation/compute"
        f"?window=month&aggregate=namespace&filter=namespace:{tenant}"
    )
    data = response.json()
    
    raw_cost = data[tenant]['totalCost']
    platform_overhead = raw_cost * (markup - 1.0)
    total_chargeback = raw_cost * markup
    
    return {
        'tenant': tenant,
        'raw_infrastructure_cost': round(raw_cost, 2),
        'platform_overhead': round(platform_overhead, 2),
        'total_chargeback': round(total_chargeback, 2),
        'markup_percentage': (markup - 1.0) * 100
    }

# Generate invoice
invoice = calculate_chargeback('team-a', markup=1.15)
print(json.dumps(invoice, indent=2))
```

**Sample Output**:
```json
{
  "tenant": "team-a",
  "raw_infrastructure_cost": 525.72,
  "platform_overhead": 78.86,
  "total_chargeback": 604.58,
  "markup_percentage": 15.0
}
```

### Cost Optimization Strategies

#### 1. Right-Sizing Recommendations

Identify over-provisioned workloads:

```bash
# Find pods with low CPU utilization (<20%)
kubectl top pods -n team-a | awk '{if (NR>1 && $3 < 20) print $0}'

# Recommend smaller resource requests
echo "Consider reducing CPU request from 1000m to 500m for low-usage pods"
```

**Vertical Pod Autoscaler (VPA)**:
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
  namespace: team-a
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"  # Automatically apply recommendations
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2000m
        memory: 4Gi
```

#### 2. Spot/Preemptible Instances

Run non-critical workloads on spot instances:

```yaml
# Node pool for spot instances
apiVersion: v1
kind: Node
metadata:
  labels:
    kubernetes.azure.com/scalesetpriority: spot
spec:
  taints:
  - key: kubernetes.azure.com/scalesetpriority
    value: spot
    effect: NoSchedule

---
# Deploy to spot nodes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
  namespace: team-a
spec:
  template:
    spec:
      tolerations:
      - key: kubernetes.azure.com/scalesetpriority
        operator: Equal
        value: spot
        effect: NoSchedule
      nodeSelector:
        kubernetes.azure.com/scalesetpriority: spot
```

**Savings**: Up to 90% off on-demand pricing

#### 3. Storage Optimization

Identify unused persistent volumes:

```bash
# Find PVCs not attached to any pod
kubectl get pvc -n team-a -o json | jq -r '.items[] | 
  select(.status.phase=="Bound") | 
  select(.metadata.annotations["pv.kubernetes.io/bind-completed"] != null) |
  .metadata.name' | while read pvc; do
    PODS=$(kubectl get pods -n team-a -o json | jq -r --arg pvc "$pvc" 
      '.items[].spec.volumes[]? | select(.persistentVolumeClaim.claimName==$pvc)')
    if [ -z "$PODS" ]; then
      echo "Unused PVC: $pvc"
    fi
  done
```

**Storage Class Tiering**:
```yaml
# Use cheaper storage for non-critical data
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard-cheap
provisioner: disk.csi.azure.com
parameters:
  skuName: StandardSSD_LRS  # Cheaper than Premium_LRS
  kind: Managed
```

#### 4. Idle Resource Detection

Detect workloads running 24/7 that could be scheduled:

```bash
# Prometheus query for low-traffic services
avg_over_time(
  rate(http_requests_total{namespace="team-a"}[24h])
) < 0.1

# Recommendation: Use CronJob or scale to zero during off-hours
```

### Cost Visibility in Developer Portal

Integrate cost data into Backstage:

```yaml
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-api-service
  annotations:
    opencost/namespace: team-a
spec:
  type: service
  lifecycle: production
  owner: team-a
```

Developers see:
- Current month cost
- Cost trend (7d, 30d)
- Budget utilization
- Optimization recommendations

### Monthly Cost Review Process

**Week 1 of Month**:
1. Generate automated showback reports
2. Send to team leads and finance
3. Identify cost anomalies

**Week 2**:
1. Platform team reviews optimization opportunities
2. Meet with high-spend teams
3. Implement quick wins (delete unused resources)

**Week 3-4**:
1. Teams implement optimization recommendations
2. Adjust resource quotas if needed
3. Update budgets for next month

### Metrics to Track

| Metric | Target | Current |
|--------|--------|---------|
| Cost per deployment | < $50/month | $45 |
| Unused resources | < 5% | 8% |
| Budget overruns | 0 teams/month | 1 |
| Cost awareness (survey) | > 80% | 75% |
| Optimization adoption | > 70% | 65% |

## Multi-Tenancy Features
