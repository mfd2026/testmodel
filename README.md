# testmodel (starter)
A minimal FastAPI service ready to be containerized with Docker and deployed to Kubernetes.

## Endpoints
- `GET /healthz` → health check
- `POST /predict` → accepts `{ "text": "..." }` and returns a dummy prediction (echo) for now.

## Local (without Docker)
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker (build & run)
```bash
# replace YOUR_DOCKERHUB with your Docker Hub username, e.g., mfd2026
docker build -t YOUR_DOCKERHUB/testmodel:0.1 .
docker run --rm -p 8000:8000 YOUR_DOCKERHUB/testmodel:0.1
# test:
# curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"مرحبا"}'
```

## Kubernetes (Minikube example)
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
# then open:
# http://$(minikube ip):30080/healthz
```
