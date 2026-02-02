pipeline {
  agent any

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Python Tests') {
      steps {
        sh '''
          set -euxo pipefail

          python3 --version

          # Create Python virtual environment
          python3 -m venv .venv
          . .venv/bin/activate

          python -m pip install -U pip
          python -m pip install pytest

          mkdir -p test-results
          pytest python/ -q --junitxml=test-results/pytest.xml
        '''
      }
    }

    stage('Java Tests (JUnit / Maven)') {
      steps {
        sh '''
          set -euxo pipefail
          cd java
          mvn -B clean test
        '''
      }
    }
  }

  post {
    always {
      // Publish test results in Jenkins UI
      junit 'test-results/pytest.xml'
      junit 'java/target/surefire-reports/*.xml'

      // Archive reports (optional but nice for grading)
      archiveArtifacts artifacts: 'test-results/*.xml, java/target/surefire-reports/*.xml',
                       allowEmptyArchive: true,
                       fingerprint: true
    }
  }
}

