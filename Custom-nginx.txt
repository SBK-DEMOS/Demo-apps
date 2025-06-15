

    Create a Google Cloud Service Account for Cert-Manager:
    This service account will have permissions to update DNS records.
        Replace YOUR_PROJECT_ID with your actual Google Cloud Project ID.
    Bash

    gcloud iam service-accounts create cert-manager-dns01-solver \
      --display-name "Cert-Manager DNS01 Solver"

    gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member "serviceAccount:cert-manager-dns01-solver@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role "roles/dns.admin"

    gcloud iam service-accounts keys create ./gcp-dns-key.json \
      --iam-account cert-manager-dns01-solver@YOUR_PROJECT_ID.iam.gserviceaccount.com

        This will save a JSON key file (e.g., gcp-dns-key.json) to your current directory.

############# 
Part 2: Kubernetes Application Manifests


# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-secure-app

configmap.yaml

# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: my-secure-app
data:
  default.conf: |
    server {
        listen 8080;
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
        }
    }
  nginx.conf: |
    user  nginx;
    worker_processes  auto;

    error_log  /dev/stderr warn;
    pid        /var/lib/nginx/nginx.pid;

    events {
        worker_connections  1024;
    }

    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /dev/stdout main;

        sendfile        on;
        tcp_nopush      on;
        tcp_nodelay     on;
        keepalive_timeout  65;
        types_hash_max_size 2048;

        client_body_temp_path /var/lib/nginx/client_temp;
        proxy_temp_path       /var/lib/nginx/proxy_temp;
        fastcgi_temp_path     /var/lib/nginx/fastcgi_temp;
        uwsgi_temp_path       /var/lib/nginx/uwsgi_temp;
        scgi_temp_path        /var/lib/nginx/scgi_temp;

        gzip on;

        include /etc/nginx/conf.d/*.conf;
    }
  index.html: |
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Custom NGINX Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #ffffff;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h1 {
                color: #0056b3;
                margin-bottom: 20px;
            }
            p {
                font-size: 1.1em;
                line-height: 1.6;
            }
            .version {
                margin-top: 30px;
                font-size: 0.9em;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello from My Custom NGINX!</h1>
            <p>This page is being served by an NGINX instance deployed on Kubernetes.</p>
            <p>You successfully deployed your application!</p>
            <div class="version">Version: 1.0</div>
        </div>
    </body>
    </html>


# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx-app
  namespace: my-secure-app
  labels:
    app: my-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
  template:
    metadata:
      labels:
        app: my-nginx
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: nginx
        image: nginx:1.28.0-alpine
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
          timeoutSeconds: 3
        readinessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
          timeoutSeconds: 3
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
          runAsNonRoot: true
          runAsUser: 1000
        volumeMounts:
          - name: nginx-conf-dir
            mountPath: /etc/nginx/conf.d
            readOnly: true
          - name: nginx-main-conf
            mountPath: /etc/nginx/nginx.conf
            subPath: nginx.conf
            readOnly: true
          - name: nginx-cache
            mountPath: /var/lib/nginx
          - name: custom-html
            mountPath: /usr/share/nginx/html/index.html
            subPath: index.html
            readOnly: true
      volumes:
        - name: nginx-conf-dir
          configMap:
            name: nginx-config
            items:
            - key: default.conf
              path: default.conf
        - name: nginx-main-conf
          configMap:
            name: nginx-config
            items:
            - key: nginx.conf
              path: nginx.conf
        - name: nginx-cache
          emptyDir: {}
        - name: custom-html
          configMap:
            name: nginx-config
            items:
            - key: index.html
              path: index.html



# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-nginx-pdb
  namespace: my-secure-app
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: my-nginx


# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx-service
  namespace: my-secure-app
spec:
  selector:
    app: my-nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP


# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-nginx-ingress
  namespace: my-secure-app
  annotations:
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod" # Must match ClusterIssuer name
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com # <<< REPLACE WITH YOUR DOMAIN
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-nginx-service
            port:
              number: 80
  tls:
  - hosts:
    - myapp.example.com # <<< REPLACE WITH YOUR DOMAIN
    secretName: myapp-tls-secret

networkpolicy.yaml

    # networkpolicy.yaml
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-nginx-ingress
      namespace: my-secure-app
    spec:
      podSelector:
        matchLabels:
          app: my-nginx
      policyTypes:
        - Ingress
        - Egress
      ingress:
        - from:
          - namespaceSelector:
              matchLabels:
                kubernetes.io/metadata.name: ingress-nginx 
            podSelector:
              matchLabels:
                app.kubernetes.io/name: ingress-nginx 
          ports:
            - protocol: TCP
              port: 8080
      egress:
        - to:
          - ipBlock:
              cidr: 0.0.0.0/0
          ports:
            - protocol: UDP
              port: 53
            - protocol: TCP
              port: 53

Part 3: Installation and Deployment Steps (Commands)

Follow these commands in sequence.

    If you had a previous failed deployment, delete it to ensure a clean start:
    Bash

kubectl delete deployment my-nginx-app -n my-secure-app
kubectl delete service my-nginx-service -n my-secure-app
# If you applied an Ingress before the Ingress Controller was ready:
kubectl delete ingress my-nginx-ingress -n my-secure-app

Apply your Kubernetes application manifests:
Bash

kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f pdb.yaml
kubectl apply -f service.yaml

Verify your pods are running and healthy (they won't be exposed externally yet):
Bash

    kubectl get pods -n my-secure-app -l app=my-nginx
    kubectl rollout status deployment/my-nginx-app -n my-secure-app

    Install NGINX Ingress Controller via Helm:

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer \
  --set controller.service.externalTrafficPolicy=Local
```
*Wait a few minutes for the LoadBalancer to provision.*
*Get the external IP address:*
```bash
kubectl get services -n ingress-nginx
# Look for the 'EXTERNAL-IP' of 'nginx-ingress-controller'
```
**Note down the `EXTERNAL-IP`.**

    Update DNS A Record at Google Domains:
        Go to your DNS provider (Google Domains) settings for myapp.example.com.
        Create an A record mapping myapp.example.com to the EXTERNAL-IP obtained in the previous step.
        Allow time for DNS propagation.

    Install Cert-Manager via Helm:
    Bash

helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --version v1.14.0 \
  --set installCRDs=true

Wait until Cert-Manager pods are running:
Bash

kubectl get pods -n cert-manager

Create Kubernetes Secret for GCP Service Account Key:
(Make sure you are in the directory where gcp-dns-key.json is located.)
Bash

kubectl create secret generic google-cloud-dns-credentials \
  --from-file=gcp-dns-key.json \
  --namespace cert-manager

Create Cert-Manager ClusterIssuer:
(Remember to replace YOUR_PROJECT_ID and your-email@example.com.)
YAML

# clusterissuer-letsencrypt-prod.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com # <<< REPLACE THIS
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - dns01:
        cloudDNS:
          project: YOUR_PROJECT_ID # <<< REPLACE THIS
          serviceAccountSecretRef:
            name: google-cloud-dns-credentials
            key: gcp-dns-key.json


kubectl apply -f clusterissuer-letsencrypt-prod.yaml

kubectl apply -f ingress.yaml

kubectl get certificate -n my-secure-app

# Wait for STATUS to become 'Ready'

kubectl describe certificate my-nginx-ingress -n my-secure-app

 kubectl apply -f networkpolicy.yaml


############################Checks ###############

kubectl describe certificate app1-tls-secret -n my-secure-app

kubectl get order -n my-secure-app # To see Let's Encrypt order status
kubectl logs -n cert-manager -l app.kubernetes.io/instance=cert-manager


###################Other notes #############


gcloud iam service-accounts create cert-manager-dns01-solver --display-name "Cert-Manager DNS01 Solver"

gcloud projects add-iam-policy-binding sbk-app-6809 --member "serviceAccount:cert-manager-dns01-solver@sbk-app-6809.iam.gserviceaccount.com" --role "roles/dns.admin"

gcloud iam service-accounts keys create ./gcp-dns-key.json --iam-account cert-manager-dns01-solver@sbk-app-6809.iam.gserviceaccount.com


kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f pdb.yaml
kubectl apply -f service.yaml


helm install nginx-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=LoadBalancer --set controller.service.externalTrafficPolicy=Local


gcloud container clusters describe gkecluster-1 --format="value(privateClusterConfig.enablePrivateNodes)" --project sbk-app-6809


# Retry the installation with an increased timeout for good measure
helm install nginx-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=LoadBalancer --set controller.service.externalTrafficPolicy=Local


helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.14.0 --set installCRDs=true

kubectl create secret generic google-cloud-dns-credentials --from-file=gcp-dns-key.json --namespace cert-manager

