Installation (hope you have got linux):
1. Please run included shell script './run.sh'
2. You will be prompted to input sudo password
3. Take your time and enjoy your coffee :-) 
(in meantime script will create minikube cluster, build and upload docker images into and run deployment scripts)
4. Browse to http://127.0.0.1:2222/
5. Upload files
6. You can check stored files on 'writer' pod


if there is problem with connection please create tunnel to reader pod like:
7. Run 'kubectl get pods' to get [pod_id] of reader
8. Create tunnel to this pod 'kubectl port-forward [pod_id] 2222:2222'

