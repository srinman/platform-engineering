# Azure Policies for AKS Platform Engineering

This directory contains Azure Policy definitions and assignments for governing AKS clusters.

## Policy Categories

### 1. Security Policies
- Enforce pod security standards
- Require container image scanning
- Mandate RBAC
- Enforce network policies

### 2. Compliance Policies
- Require specific tags
- Enforce naming conventions
- Audit resource configurations
- Track compliance status

### 3. Cost Management Policies
- Enforce resource limits
- Require budget tags
- Alert on cost thresholds
- Prevent oversized resources

### 4. Operational Policies
- Require monitoring agents
- Enforce backup policies
- Mandate update schedules
- Require disaster recovery

## Policy Assignments

### baseline-cluster1-policies.json
Policies for standard AKS cluster (baseline-cluster1)

### baseline-cluster2-policies.json
Policies for AKS Automatic (baseline-cluster2)

### application-policies.json
Policies for application workloads

## Applying Policies

### Using Azure CLI

```bash
# Create policy assignment
az policy assignment create \
  --name "aks-security-policies" \
  --policy-set-definition "baseline-cluster1-policies" \
  --scope "/subscriptions/<subscription-id>/resourceGroups/rg-baseline-cluster1"
```

### Using Terraform

```hcl
resource "azurerm_policy_assignment" "aks_security" {
  name                 = "aks-security-policies"
  scope                = azurerm_resource_group.main.id
  policy_definition_id = azurerm_policy_set_definition.aks_security.id
}
```

## Gatekeeper Policies

For runtime Kubernetes policy enforcement, we use OPA Gatekeeper.

### Example: Require resource limits

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredResources
metadata:
  name: require-resources
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet"]
  parameters:
    limits: ["cpu", "memory"]
    requests: ["cpu", "memory"]
```

## Policy Testing

Test policies before deployment:

```bash
# Test with Azure Policy Guest Configuration
az policy state trigger-scan \
  --resource-group rg-baseline-cluster1
```

## Compliance Reporting

View compliance status:

```bash
# List policy compliance
az policy state list \
  --resource-group rg-baseline-cluster1 \
  --filter "ComplianceState eq 'NonCompliant'"
```

## Custom Policies

Create custom policies for your organization:

1. Define the policy rule
2. Create parameters
3. Test thoroughly
4. Document the policy
5. Assign to appropriate scope
