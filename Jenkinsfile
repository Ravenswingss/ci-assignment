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

          python3 -m venv .venv
          . .venv/bin/activate

          python -m pip install -U pip
          python -m pip install pytest

          mkdir -p test-results
          pytest python/ -q --junitxml=test-results/pytest.xml
        '''
      }
    }

    stage('Java Tests (JUnit)') {
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
      // publish both test suites in Jenkins UI
      junit allowEmptyResults: true, testResults: 'test-results/pytest.xml'
      junit allowEmptyResults: true, testResults: 'java/target/surefire-reports/*.xml'

      // optional: keep the xmls as downloadable artifacts
      archiveArtifacts artifacts: 'test-results/*.xml, java/target/surefire-reports/*.xml',
                       allowEmptyArchive: true,
                       fingerprint: true
    }
  }
}

