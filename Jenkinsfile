pipeline {
    agent any
    environment {
        // You will need to setup this credential in Jenkins
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKERHUB_USER = 'saadjamil1'
    }
    stages {
        stage('Fetch') {
            steps {
                checkout scm
            }
        }
        stage('Debug') {
    steps {
        sh 'pwd'
        sh 'find . -name Dockerfile'
        sh 'cat Dockerfile'
    }
}
        stage('Build and Run') {
            steps {
                sh 'docker build -t ${DOCKERHUB_USER}/sentiment-api:unstable .'
                sh 'docker rm -f sentiment-app || true'
                sh 'docker run -d --name sentiment-app -p 5000:5000 ${DOCKERHUB_USER}/sentiment-api:unstable'
                // Wait for the app to start (model is pre-downloaded now)
                sh 'sleep 5'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'docker exec sentiment-app pytest tests/test_api.py'
            }
        }
        stage('UI Test') {
            steps {
                sh '''
                    docker run --rm \
                        --network host \
                        -v $(pwd)/tests:/tests \
                        --shm-size=2g \
                        selenium/standalone-chrome:latest \
                        bash -c "pip install selenium pytest requests -q && pytest /tests/test_ui.py -v --tb=short" || true
                '''
            }
        }
        stage('Build and Push') {
            steps {
                script {
                    withDockerRegistry(credentialsId: DOCKERHUB_CREDENTIALS_ID, url: '') {
                        sh 'docker push ${DOCKERHUB_USER}/sentiment-api:unstable'
                        // Switch only app.py to stable-fallback branch to perfectly reuse Docker cache
                        sh 'git fetch origin stable-fallback'
                        sh 'git checkout FETCH_HEAD -- app.py'
                        sh 'docker build -t ${DOCKERHUB_USER}/sentiment-api:stable .'
                        sh 'docker push ${DOCKERHUB_USER}/sentiment-api:stable'
                        // Revert back app.py
                        sh 'git checkout HEAD -- app.py'
                    }
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh 'kubectl apply -f k8s/pvc.yaml'
                sh 'kubectl apply -f k8s/blue-deployment.yaml'
                sh 'kubectl apply -f k8s/green-deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
            }
        }
    }
    post {
        always {
            sh 'docker rm -f sentiment-app || true'
        }
    }
}
