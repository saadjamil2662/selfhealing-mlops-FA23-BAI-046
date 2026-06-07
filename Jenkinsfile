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
        stage('Build and Run') {
            steps {
                sh 'docker build -t ${DOCKERHUB_USER}/sentiment-api:unstable .'
                sh 'docker rm -f sentiment-app || true'
                sh 'docker run -d --name sentiment-app -p 5000:5000 ${DOCKERHUB_USER}/sentiment-api:unstable'
                // Wait for the app to start
                sh 'sleep 15'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'docker exec sentiment-app pytest tests/test_api.py'
            }
        }
        stage('UI Test') {
            steps {
                sh 'docker exec sentiment-app pytest tests/test_ui.py'
            }
        }
        stage('Build and Push') {
            steps {
                script {
                    withDockerRegistry(credentialsId: DOCKERHUB_CREDENTIALS_ID, url: '') {
                        sh 'docker push ${DOCKERHUB_USER}/sentiment-api:unstable'
                        // Switch to stable-fallback branch and build stable image
                        sh 'git fetch origin'
                        sh 'git checkout origin/stable-fallback'
                        sh 'docker build -t ${DOCKERHUB_USER}/sentiment-api:stable .'
                        sh 'docker push ${DOCKERHUB_USER}/sentiment-api:stable'
                        // Revert back to main to deploy
                        sh 'git checkout main'
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
