# Scenario 4: ML/AI Workload Platform

## Overview

This scenario provides a specialized platform for machine learning and AI workloads with GPU support, experiment tracking, model serving, and data processing capabilities.

## Problem Statement

Data science teams need:
- GPU-enabled compute for training
- Jupyter notebooks for experimentation
- MLflow for experiment tracking
- Model serving infrastructure
- Scalable data processing
- Cost-effective resource usage

## Solution

Using KRO, we create an `MLPlatform` abstraction that:
1. Provisions GPU-enabled node pools
2. Deploys JupyterHub for interactive notebooks
3. Sets up MLflow for experiment tracking
4. Configures model serving with KServe
5. Implements auto-scaling based on workload
6. Provides data access to Azure storage

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  ML/AI Platform Cluster                                   │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ JupyterHub                                          │ │
│  │ - User notebooks with GPU access                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ MLflow Tracking Server                              │ │
│  │ - Experiment tracking                               │ │
│  │ - Model registry                                    │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ KServe / Model Serving                              │ │
│  │ - Inference endpoints                               │ │
│  │ - A/B testing                                       │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                            │
│  GPU Node Pools: Training | CPU Node Pools: Serving       │
└──────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install KRO ResourceGroup

```bash
kubectl apply -f kro-definitions/mlplatform-resourcegroup.yaml
```

### 2. Deploy ML Platform

```bash
kubectl apply -f examples/ml-platform.yaml
```

## MLPlatform DSL Reference

```yaml
apiVersion: platform.example.com/v1alpha1
kind: MLPlatform
metadata:
  name: datascience-platform
spec:
  # GPU configuration
  gpu:
    enabled: true
    nodePoolSize: Standard_NC6s_v3  # NVIDIA V100
    minNodes: 0
    maxNodes: 10
  
  # JupyterHub configuration
  jupyterhub:
    enabled: true
    userResources:
      cpu: "4"
      memory: "16Gi"
      gpu: "1"
  
  # MLflow configuration
  mlflow:
    enabled: true
    storage: azure-blob
    storageAccount: mlflowstorage
  
  # Model serving
  modelServing:
    enabled: true
    framework: kserve
