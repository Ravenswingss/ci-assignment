node {
  try {
    stage('Checkout') {
      checkout scm
    }

    stage('Python Tests') {
      sh '''#!/bin/bash
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

    stage('Java Build + Test (JUnit / Maven)') {
      sh '''#!/bin/bash
        set -euxo pipefail
        cd java
        mvn -B clean test
      '''
    }

stage('SonarQube Static Analysis') {
  catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
    dir('java') {
      withSonarQubeEnv('SonarQube') {
        sh '''#!/bin/bash
          set -euxo pipefail
          mvn -B verify sonar:sonar \
            -Dsonar.projectKey=mathutils-java \
            -Dsonar.projectName=mathutils-java
        '''
      }
    }
  }
}
  

    stage('Quality Gate') {
      timeout(time: 5, unit: 'MINUTES') {
        waitForQualityGate abortPipeline: true
      }
    }

    stage('Package Artifact (JAR)') {
      dir('java') {
        sh '''#!/bin/bash
          set -euxo pipefail
          mvn -B -DskipTests package
        '''
      }
    }

  } finally {
    stage('Publish Reports + Notify') {
      // Publish test results
      junit 'test-results/pytest.xml'
      junit 'java/target/surefire-reports/*.xml'

      // Archive artifacts + coverage
      archiveArtifacts artifacts: '''
        test-results/*.xml,
        java/target/surefire-reports/*.xml,
        java/target/*.jar,
        java/target/site/jacoco/**
      ''', allowEmptyArchive: true, fingerprint: true

      // Email (non-fatal)
      try {
        emailext(
          to: 'lahc.vrc.ponce@gmail.com',
          subject: "${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
          body: """Build result: ${currentBuild.currentResult}

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
"""
        )
      } catch (err) {
        echo "Email failed (not failing build): ${err}"
      }
    }
  }
}

