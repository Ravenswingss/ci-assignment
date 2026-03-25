pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "skulldrag/spring-java-app:latest"
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
                                cd /workspace/spring-java-app &&
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
                                cd /workspace/spring-java-app &&
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
                                cd /workspace/spring-java-app &&
                                mvn clean test
                            "
                        '''
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                dir('spring-java-app') {
                    withSonarQubeEnv("${SONARQUBE_ENV}") {
                        sh '''
                            mvn clean verify sonar:sonar \
                              -Dsonar.projectKey=spring-java-app \
                              -Dsonar.projectName=spring-java-app
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('spring-java-app') {
                    sh 'docker build -t "$DOCKER_IMAGE" .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push "$DOCKER_IMAGE"'
                    sh 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl --kubeconfig=/var/jenkins_home/.kube/config --insecure-skip-tls-verify=true apply --validate=false -f spring-java-app/deployment.yaml
                    kubectl --kubeconfig=/var/jenkins_home/.kube/config --insecure-skip-tls-verify=true rollout restart deployment/spring-java-app-deployment
                    kubectl --kubeconfig=/var/jenkins_home/.kube/config --insecure-skip-tls-verify=true rollout status deployment/spring-java-app-deployment --timeout=180s
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'spring-java-app/target/surefire-reports/*.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'spring-java-app/target/*.jar'
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
