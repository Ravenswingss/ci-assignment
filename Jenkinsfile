
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

          # Create venv in workspace (fixes PEP 668)
          python3 -m venv .venv
          . .venv/bin/activate

          python -m pip install -U pip
          python -m pip install pytestpipeline {
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

          # Create venv in workspace (fixes PEP 668)
          python3 -m venv .venv
          . .venv/bin/activate

          python -m pip install -U pip
          python -m pip install pytest

          mkdir -p test-results
          pytest python/ -q --junitxml=test-results/pytest.xml
        '''
      }
    }

    // ✅ ADD THIS STAGE RIGHT HERE
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
      // Publish BOTH Python + Java results
      junit 'test-results/pytest.xml'
      junit 'java/target/surefire-reports/*.xml'

      // Optional: archive reports so they’re downloadable
      archiveArtifacts artifacts: 'test-results/*.xml, java/target/surefire-reports/*.xml', allowEmptyArchive: true, fingerprint: true
    }
  }
}

          mkdir -p test-results
          pytest python/ -q --junitxml=test-results/pytest.xml
        '''
      }
    }
  }

  post {
  always {
    junit allowEmptyResults: true, testResults: 'test-results/pytest.xml'
    junit allowEmptyResults: true, testResults: 'java/target/surefire-reports/*.xml'
  }
}

    
 


