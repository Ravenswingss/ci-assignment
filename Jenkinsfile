pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Java') {
            steps {
                dir('java') {
                    sh 'mvn test'
                }
            }
        }

        stage('Build Python') {
            steps {
                dir('python') {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pytest --junitxml=pytest-results.xml
                    '''
                }
            }
        }
    }

    post {
        always {
            junit 'java/target/surefire-reports/*.xml'
            junit 'python/pytest-results.xml'
        }
    }
}
