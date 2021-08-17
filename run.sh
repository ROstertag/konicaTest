# install minikube locally
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube

# run minikube cluster
minikube start

# add docker images to minikube
eval $(minikube docker-env)
docker build -t konica-reader -f DockerfileReader .
docker build -t konica-processor -f DockerfileProcessor .
docker build -t konica-writer -f DockerfileWriter .

# run deployments for each part of solution
kubectl apply -f deployment-nats.yaml
kubectl apply -f deployment-reader.yaml
kubectl apply -f deployment-processor.yaml
kubectl apply -f deployment-writer.yaml

# sleep while pods are created
sleep 20s
# creates tunnel to reader flask
kubectl port-forward $(kubectl get pods | grep reader| awk '{print $1}') 2222:2222