# Observability Implementation

## Overview

Observability is a foundational capability of the platform, providing visibility into application and infrastructure health, performance, and behavior. This document outlines the complete observability stack implementation and best practices.

## The Three Pillars of Observability

### 1. Metrics (Prometheus + Grafana)
**What**: Time-series numerical data  
**Use For**: Performance monitoring, alerting, capacity planning

### 2. Logs (Loki + Fluent Bit)
**What**: Structured event data  
**Use For**: Debugging, audit trails, compliance

### 3. Traces (Tempo + OpenTelemetry)
**What**: Request flow across services  
**Use For**: Distributed system debugging, latency analysis

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│  Applications & Platform Services                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  App A   │  │  App B   │  │ Ingress  │                 │
│  │          │  │          │  │          │                 │
│  │ /metrics │  │ /metrics │  │ /metrics │                 │
│  │  logs    │  │  logs    │  │  logs    │                 │
│  │  traces  │  │  traces  │  │  traces  │                 │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                 │
└───────┼─────────────┼─────────────┼────────────────────────┘
        │             │             │
        ▼             ▼             ▼
┌────────────────────────────────────────────────────────────┐
│  Collection Layer                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Prometheus  │  │  Fluent Bit  │  │  OTEL        │     │
│  │  (Scrape)    │  │  (Collect)   │  │  Collector   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌────────────────────────────────────────────────────────────┐
│  Storage Layer                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Prometheus  │  │     Loki     │  │    Tempo     │     │
│  │  (TSDB)      │  │  (LogStore)  │  │ (TraceStore) │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────┐
│  Visualization & Alerting                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Grafana                             │   │
│  │  - Dashboards (metrics, logs, traces)               │   │
│  │  - Alerting                                         │   │
│  │  - Correlation across signals                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │             Alertmanager                            │   │
│  │  - Alert routing                                    │   │
│  │  - Deduplication                                    │   │
│  │  - Integration (Slack, PagerDuty, Email)           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Metrics Implementation

### Prometheus Stack Deployment

Deploy via ArgoCD:

```yaml
# monitoring/prometheus-stack.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: prometheus-stack
  namespace: argocd
spec:
  project: platform
  source:
    repoURL: https://prometheus-community.github.io/helm-charts
    chart: kube-prometheus-stack
    targetRevision: 55.5.0
    helm:
      values: |
        prometheus:
          prometheusSpec:
            retention: 30d
            storageSpec:
              volumeClaimTemplate:
                spec:
                  accessModes: ["ReadWriteOnce"]
                  resources:
                    requests:
                      storage: 100Gi
            additionalScrapeConfigs:
              - job_name: 'kubernetes-pods'
                kubernetes_sd_configs:
                  - role: pod
                relabel_configs:
                  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
                    action: keep
                    regex: true
        
        grafana:
          enabled: true
          adminPassword: <change-me>
          persistence:
            enabled: true
            size: 10Gi
          dashboardProviders:
            dashboardproviders.yaml:
              apiVersion: 1
              providers:
                - name: 'default'
                  folder: 'Platform'
                  type: file
                  options:
                    path: /var/lib/grafana/dashboards/default
        
        alertmanager:
          enabled: true
          config:
            global:
              resolve_timeout: 5m
            route:
              group_by: ['alertname', 'namespace']
              group_wait: 10s
              group_interval: 10s
              repeat_interval: 12h
              receiver: 'slack'
              routes:
                - match:
                    severity: critical
                  receiver: 'pagerduty'
            receivers:
              - name: 'slack'
                slack_configs:
                  - api_url: ${SLACK_WEBHOOK_URL}
                    channel: '#platform-alerts'
              - name: 'pagerduty'
                pagerduty_configs:
                  - service_key: ${PAGERDUTY_KEY}
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Application Metrics Instrumentation

**Automatic** (via ServiceMonitor created by KRO):

When deploying via Application DSL, metrics are automatically scraped:

```yaml
# Created automatically by KRO
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-app
  namespace: team-a
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

**Manual Instrumentation** (for custom apps):

```python
# Python app with Prometheus client
from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Instrument your code
@http_request_duration_seconds.labels(method='GET', endpoint='/api/users').time()
def get_users():
    # Your logic here
    http_requests_total.labels(method='GET', endpoint='/api/users', status=200).inc()
    return users

# Expose metrics on /metrics
start_http_server(8000)
```

### Key Metrics to Track

#### Platform-Level Metrics

```promql
# Cluster CPU utilization
100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))

# Cluster memory utilization
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Pod success rate
sum(kube_pod_status_phase{phase="Running"}) / sum(kube_pod_status_phase) * 100

# ArgoCD sync success rate
sum(rate(argocd_app_sync_total{phase="Succeeded"}[5m])) / 
sum(rate(argocd_app_sync_total[5m])) * 100
```

#### Application-Level Metrics

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) /
rate(http_requests_total[5m]) * 100

# Request latency (p95, p99)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Saturation (CPU, Memory)
rate(container_cpu_usage_seconds_total[5m])
container_memory_working_set_bytes
```

### Standard Dashboards

Platform provides pre-built dashboards:

1. **Platform Overview**: Cluster health, resource usage
2. **Application Performance**: Requests, errors, latency (RED metrics)
3. **Kubernetes Resources**: Pods, deployments, nodes
4. **Cost Dashboard**: Per-tenant cost breakdown
5. **Security**: Failed auth attempts, policy violations

## Logging Implementation

### Loki + Fluent Bit Deployment

```yaml
# monitoring/loki-stack.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: loki-stack
  namespace: argocd
spec:
  project: platform
  source:
    repoURL: https://grafana.github.io/helm-charts
    chart: loki-stack
    targetRevision: 2.9.11
    helm:
      values: |
        loki:
          enabled: true
          persistence:
            enabled: true
            size: 100Gi
          config:
            schema_config:
              configs:
                - from: 2024-01-01
                  store: boltdb-shipper
                  object_store: azure
                  schema: v11
                  index:
                    prefix: loki_index_
                    period: 24h
            storage_config:
              azure:
                account_name: ${AZURE_STORAGE_ACCOUNT}
                account_key: ${AZURE_STORAGE_KEY}
                container_name: loki-logs
              boltdb_shipper:
                active_index_directory: /loki/index
                shared_store: azure
                cache_location: /loki/cache
            limits_config:
              retention_period: 30d
        
        fluent-bit:
          enabled: true
          config:
            outputs: |
              [OUTPUT]
                  Name loki
                  Match *
                  Host loki
                  Port 3100
                  Labels job=fluentbit, namespace=$kubernetes['namespace_name'], pod=$kubernetes['pod_name']
                  auto_kubernetes_labels on
            filters: |
              [FILTER]
                  Name kubernetes
                  Match kube.*
                  Merge_Log On
                  Keep_Log Off
                  K8S-Logging.Parser On
                  K8S-Logging.Exclude On
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
```

### Structured Logging Best Practices

**JSON format** (recommended):

```json
{
  "timestamp": "2026-01-25T10:30:00Z",
  "level": "INFO",
  "message": "User login successful",
  "userId": "12345",
  "ip": "192.168.1.1",
  "requestId": "req-abc-123",
  "trace_id": "trace-xyz-789"
}
```

**Python Example**:

```python
import json
import logging
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, 'userId'):
            log_data['userId'] = record.userId
        if hasattr(record, 'trace_id'):
            log_data['trace_id'] = record.trace_id
        return json.dumps(log_data)

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
logger.info("User login successful", extra={"userId": "12345"})
```

### Log Queries (LogQL)

```logql
# All logs from team-a namespace
{namespace="team-a"}

# Error logs only
{namespace="team-a"} |= "error"
{namespace="team-a"} | json | level="ERROR"

# Logs for specific pod
{namespace="team-a", pod="my-app-abc123"}

# Failed HTTP requests
{namespace="team-a"} | json | status >= 500

# Calculate error rate
sum(rate({namespace="team-a"} | json | level="ERROR" [5m])) /
sum(rate({namespace="team-a"}[5m]))

# Logs with trace correlation
{namespace="team-a"} | json | trace_id="xyz-789"
```

## Distributed Tracing Implementation

### Tempo + OpenTelemetry Deployment

```yaml
# monitoring/tempo.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: tempo
  namespace: argocd
spec:
  project: platform
  source:
    repoURL: https://grafana.github.io/helm-charts
    chart: tempo
    targetRevision: 1.7.1
    helm:
      values: |
        tempo:
          backend: azure
          azure:
            storage_account_name: ${AZURE_STORAGE_ACCOUNT}
            storage_account_key: ${AZURE_STORAGE_KEY}
            container_name: tempo-traces
          retention: 720h  # 30 days
        
        # OpenTelemetry Collector
        otelCollector:
          enabled: true
          config:
            receivers:
              otlp:
                protocols:
                  grpc:
                    endpoint: 0.0.0.0:4317
                  http:
                    endpoint: 0.0.0.0:4318
            processors:
              batch:
                timeout: 5s
                send_batch_size: 100
            exporters:
              otlp:
                endpoint: tempo:4317
                tls:
                  insecure: true
            service:
              pipelines:
                traces:
                  receivers: [otlp]
                  processors: [batch]
                  exporters: [otlp]
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
```

### Application Tracing Instrumentation

**Python (OpenTelemetry)**:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

# Initialize tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Auto-instrument Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Manual span creation
@app.route('/api/users/<user_id>')
def get_user(user_id):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)
        
        # Call database
        with tracer.start_as_current_span("db.query"):
            user = db.get_user(user_id)
        
        return user
```

## Alerting

### Alert Rules

```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: platform-alerts
  namespace: monitoring
spec:
  groups:
    - name: platform
      interval: 30s
      rules:
        # High error rate
        - alert: HighErrorRate
          expr: |
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (namespace, pod) /
            sum(rate(http_requests_total[5m])) by (namespace, pod) > 0.05
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High error rate in {{ $labels.namespace }}/{{ $labels.pod }}"
            description: "Error rate is {{ $value | humanizePercentage }}"
        
        # Pod crash looping
        - alert: PodCrashLooping
          expr: |
            rate(kube_pod_container_status_restarts_total[15m]) > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
        
        # High memory usage
        - alert: HighMemoryUsage
          expr: |
            container_memory_working_set_bytes / 
            container_spec_memory_limit_bytes > 0.9
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High memory usage in {{ $labels.namespace }}/{{ $labels.pod }}"
            description: "Memory usage is {{ $value | humanizePercentage }}"
        
        # ArgoCD sync failed
        - alert: ArgocdSyncFailed
          expr: |
            argocd_app_sync_total{phase="Failed"} > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "ArgoCD sync failed for {{ $labels.name }}"
```

### Alert Routing

```yaml
# alertmanager-config.yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'default'
  group_by: ['alertname', 'namespace']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  
  routes:
    # Platform-wide critical alerts -> PagerDuty
    - match:
        severity: critical
      receiver: 'pagerduty'
      continue: true
    
    # Team-specific alerts -> Team Slack channels
    - match:
        namespace: team-a
      receiver: 'team-a-slack'
    
    - match:
        namespace: team-b
      receiver: 'team-b-slack'

receivers:
  - name: 'default'
    slack_configs:
      - api_url: ${SLACK_WEBHOOK_URL}
        channel: '#platform-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
  
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: ${PAGERDUTY_SERVICE_KEY}
        severity: '{{ .GroupLabels.severity }}'
  
  - name: 'team-a-slack'
    slack_configs:
      - api_url: ${TEAM_A_SLACK_WEBHOOK}
        channel: '#team-a-alerts'
  
  - name: 'team-b-slack'
    slack_configs:
      - api_url: ${TEAM_B_SLACK_WEBHOOK}
        channel: '#team-b-alerts'
```

## Service Level Objectives (SLOs)

### Define SLOs

```yaml
# slo-definitions.yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: ServiceLevelObjective
metadata:
  name: api-availability
  namespace: team-a
spec:
  service: my-api
  description: "API service availability SLO"
  
  # Target: 99.9% availability
  objectives:
    - name: availability
      target: 0.999
      window: 30d
      sli:
        ratio:
          success:
            metric: http_requests_total{status!~"5.."}
          total:
            metric: http_requests_total
  
  alerting:
    burnRate:
      - severity: critical
        short: 1h
        long: 5m
        factor: 14.4  # 1% error budget burn in 1 hour
      - severity: warning
        short: 6h
        long: 30m
        factor: 6  # 5% error budget burn in 6 hours
```

### Error Budget Tracking

```promql
# Calculate error budget remaining
(1 - (
  sum(rate(http_requests_total{status=~"5..", namespace="team-a"}[30d])) /
  sum(rate(http_requests_total{namespace="team-a"}[30d]))
)) / 0.001  # 0.1% error budget

# Result: 1.0 = 100% budget remaining, 0.0 = budget exhausted
```

## Default Observability per Application

When deploying via Application DSL (Scenario 1), you automatically get:

✅ **Metrics**:
- `/metrics` endpoint scraped every 30s
- ServiceMonitor created
- Basic RED metrics (Rate, Errors, Duration)
- Resource usage (CPU, Memory)

✅ **Logs**:
- Stdout/stderr collected via Fluent Bit
- Indexed in Loki
- Searchable in Grafana
- Retention: 30 days

✅ **Traces**:
- OTEL_EXPORTER_OTLP_ENDPOINT injected as env var
- Trace IDs in logs (if instrumented)
- Distributed tracing via Tempo

✅ **Dashboards**:
- Application overview dashboard
- RED metrics visualization
- Resource usage graphs

✅ **Alerts**:
- High error rate (>5% for 5m)
- High latency (p95 > 1s)
- Pod crashes
- Resource exhaustion

## Access and Permissions

### Grafana RBAC

```yaml
# Team-specific Grafana folders
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-team-permissions
  namespace: monitoring
data:
  permissions.yaml: |
    folders:
      - name: "Team A"
        uid: team-a
        permissions:
          - role: Viewer
            teamId: team-a
          - role: Editor
            teamId: team-a-admins
      
      - name: "Team B"
        uid: team-b
        permissions:
          - role: Viewer
            teamId: team-b
```

Teams can only access:
- Their namespace metrics
- Their namespace logs
- Their traces
- Shared platform dashboards (read-only)

## Resources

- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Loki LogQL](https://grafana.com/docs/loki/latest/logql/)

## Related Documentation

- [Developer Experience](./DEVELOPER-EXPERIENCE.md)
- [Platform Architecture](./PLATFORM-ARCHITECTURE.md)
- [Golden Paths](./GOLDEN-PATHS.md)
