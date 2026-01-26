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

        stage('Python Tests') {
  steps {
    sh '''
      set -euxo pipefail

      # Create a virtualenv inside the workspace
      python3 -m venv .venv
      . .venv/bin/activate

      # Use venv python/pip (NOT system pip)
      python -m pip install -U pip
      python -m pip install pytest

      # Run tests + write JUnit XML for Jenkins to record
      mkdir -p test-results
      pytest python/ -q --junitxml=test-results/pytest.xml
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
