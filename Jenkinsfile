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

    stage('Java Build + Test (JUnit / Maven)') {
      steps {
        sh '''
          set -euxo pipefail
          cd java
          mvn -B clean test
        '''
      }
    }

    stage('SonarQube Static Analysis') {
      steps {
        dir('java') {
          // Jenkins: Manage Jenkins -> System -> SonarQube servers
          // Name must match what's configured there, e.g. "SonarQube"
          withSonarQubeEnv('SonarQube') {
            sh '''
              set -euxo pipefail
              mvn -B verify sonar:sonar \


