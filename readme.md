Installation (hope you have got linux):
1. Please run included shell script './run.sh'
2. You will be prompted to input sudo password
3. Take your time and go get your coffee :-) 
(in meantime script will create minikube cluster, create and upload docker images into it and run deployment scripts)
4. Browse to http://127.0.0.1:2222/


if there is problem with connection please create tunnel to reader pod like:
4. Run 'kubectl get pods' to get [pod_id] of reader
5. Create tunnel to this pod 'kubectl port-forward [pod_id] 2222:2222'

