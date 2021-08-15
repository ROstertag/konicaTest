# install minikube locally
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install -y minikube-darwin-amd64 /usr/local/bin/minikube

# run minikube cluster
minikube start

# add docker images to minikube
cd reader
eval $(minikube docker-env)
docker build -t konica-reader .

cd ../processor
docker build -t konica-processor .

cd ../writer
docker build -t konica-writer .

# run deployments for each part of solution
cd ..
kubectl apply -f deployment-nats.yaml
kubectl apply -f deployment-reader.yaml
kubectl apply -f deployment-processor.yaml
kubectl apply -f deployment-writer.yaml
