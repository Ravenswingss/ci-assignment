pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "skulldrag/java-ci-app:latest"
        SONARQUBE_ENV = "SonarQube"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Java Version Tests') {
            parallel {

                stage('Java 8') {
                    steps {
                        sh '''
                            tar -C "$WORKSPACE" -cf - . | docker run --rm -i maven:3.9.6-eclipse-temurin-8 sh -c "
                                mkdir -p /workspace &&
                                tar -xf - -C /workspace &&
                                cd /workspace/java &&
                                mvn clean test
                            "
                        '''
                    }
                }

                stage('Java 11') {
                    steps {
                        sh '''
                            tar -C "$WORKSPACE" -cf - . | docker run --rm -i maven:3.9.6-eclipse-temurin-11 sh -c "
                                mkdir -p /workspace &&
                                tar -xf - -C /workspace &&
                                cd /workspace/java &&
                                mvn clean test
                            "
                        '''
                    }
                }

                stage('Java 17') {
                    steps {
                        sh '''
                            tar -C "$WORKSPACE" -cf - . | docker run --rm -i maven:3.9.6-eclipse-temurin-17 sh -c "
                                mkdir -p /workspace &&
                                tar -xf - -C /workspace &&
                                cd /workspace/java &&
                                mvn clean test
                            "
                        '''
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                dir('java') {
                    withSonarQubeEnv("${SONARQUBE_ENV}") {
                        sh '''
                            mvn clean verify sonar:sonar \
                              -Dsonar.projectKey=java-ci-app \
                              -Dsonar.projectName=java-ci-app
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f deployment.yaml
                    kubectl rollout status deployment/java-app-deployment
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'java/target/surefire-reports/*.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'java/target/*.jar'
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
