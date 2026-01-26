
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
          python -m pip install pytest

          mkdir -p test-results
          pytest python/ -q --junitxml=test-results/pytest.xml
        '''
      }
    }
  }

  post {
    always {
      junit 'test-results/pytest.xml'
    }
  }
}

