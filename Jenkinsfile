pipeline {
    agent any

    environment {
        // AWS credentials configured in Jenkins
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'your-ecr-repo-name'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        AWS_ACCOUNT_ID = '123456789012' // replace with your AWS account ID
        DOCKER_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/yourrepo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        success {
            echo "Docker image pushed to ECR: ${DOCKER_IMAGE}"
        }
        failure {
            echo "Build failed!"
        }
    }
}
