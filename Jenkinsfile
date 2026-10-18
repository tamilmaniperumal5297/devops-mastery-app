pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'tamilmani5297'
        IMAGE_NAME      = 'devops-mastery-app'
        REGISTRY_CRED   = 'dockerhub-credentials' // ID of credentials stored in Jenkins
    }

    stages {
        stage('1. Code Validation') {
            steps {
                echo 'Checking Python application syntax...'
                sh 'python3 -m py_compile app.py || python -m py_compile app.py'
            }
        }

        stage('2. Build & Tag Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}..."
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest ."
            }
        }

        stage('3. Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CRED}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }

        stage('4. Deploy to Kubernetes Cluster') {
            steps {
                echo 'Applying Kubernetes Manifests...'
                sh 'kubectl apply -f k8s/configmap.yaml'
                sh 'kubectl apply -f k8s/secret.yaml'
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl apply -f k8s/ingress.yaml'
                sh "kubectl rollout restart deployment/devops-app-deployment"
            }
        }

        stage('5. Verify Rollout Status') {
            steps {
                echo 'Waiting for pods to reach Running state...'
                sh 'kubectl rollout status deployment/devops-app-deployment --timeout=60s'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished.'
        }
    }
}