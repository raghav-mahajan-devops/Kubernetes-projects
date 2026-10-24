# Kubernetes Projects

A collection of Kubernetes examples and deployment manifests, from core workload
resources to a containerized Django notes application.

## Repository contents

| Directory | Contents |
|---|---|
| [`notes-app/`](./notes-app/) | Django notes application, Dockerfile, and Kubernetes manifests for its namespace, Deployment, Service, and HorizontalPodAutoscaler. See its [README](./notes-app/README.md) for application details and local setup. |
| [`samples/`](./samples/) | Standalone examples of Deployments, ReplicaSets, DaemonSets, Jobs, CronJobs, Services, ConfigMaps, PersistentVolumes, and StatefulSets. |
| [`mysql/`](./mysql/) | MySQL Kubernetes resources, including a StatefulSet, Service, ConfigMap, Secret, namespace, and service account/RBAC examples. |
| [`pods/`](./pods/) | Pod examples demonstrating init containers and sidecar containers. |

## Deploy the notes app

The notes app manifests use the `webapp` namespace. Create it before applying
the remaining resources:

```sh
kubectl apply -f notes-app/namespace.yaml
kubectl apply -f notes-app/
```

The Deployment references the `raghavdevops10/notes-app:latest` image. Make
sure that image is available to your cluster, or update the image in
[`notes-app/deployment.yaml`](./notes-app/deployment.yaml) to one you have
built and published. The HorizontalPodAutoscaler also requires a working
cluster metrics API (commonly provided by Metrics Server).

Check the rollout and service:

```sh
kubectl get all -n webapp
kubectl rollout status deployment/notes-app -n webapp
```

## Explore the examples

Apply an individual sample with `kubectl apply -f <manifest>`. Review each
manifest first: sample resources may reference namespaces or companion
resources (such as Secrets, ConfigMaps, or storage) that must be created
separately. For notes app setup and configuration, see
[`notes-app/README.md`](./notes-app/README.md).