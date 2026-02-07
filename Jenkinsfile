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

    // Static code analysis (non-fatal for deadline submission)
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

    // Only run Quality Gate if Sonar succeeded
    stage('Quality Gate') {
      if (currentBuild.currentResult == 'SUCCESS') {
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      } else {
        echo "Skipping Quality Gate because Sonar did not succeed (result=${currentBuild.currentResult})"
      }
    }

    // Always attempt to generate the deployable artifact
    stage('Package Artifact (JAR)') {
      catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
        dir('java') {
          sh '''#!/bin/bash
            set -euxo pipefail
            mvn -B -DskipTests package
          '''
        }
      }
    }

  } finally {
    stage('Publish Reports + Notify') {
      // Publish test results in Jenkins UI
      junit 'test-results/pytest.xml'
      junit 'java/target/surefire-reports/*.xml'

      // Archive artifacts + reports for grading
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

