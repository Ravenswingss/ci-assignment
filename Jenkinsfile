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
    }

    stage('Java Build + Test (JUnit / Maven)') {
      steps {
        sh '''#!/bin/bash
          set -euxo pipefail
          cd java
          mvn -B clean test
        '''
      }
    }

    stage('SonarQube Static Analysis') {
      steps {
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
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Package Artifact (JAR)') {
      steps {
        dir('java') {
          sh '''#!/bin/bash
            set -euxo pipefail
            mvn -B -DskipTests package
          '''
        }
      }
    }
  }

  post {
    always {
      junit 'test-results/pytest.xml'
      junit 'java/target/surefire-reports/*.xml'

      archiveArtifacts artifacts: '''
        test-results/*.xml,
        java/target/surefire-reports/*.xml,
        java/target/*.jar,
        java/target/site/jacoco/**
      ''',
      allowEmptyArchive: true,
      fingerprint: true
    }

    success {
	script {
	 try {
      // If you have "Email Extension Plugin", this works.
      emailext(
        to: 'lahc.vrc.ponce@gmail.com',
        subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        body: """Build succeeded ✅

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
"""
      )
    }

    failure {
	script {
	 try {
      emailext(
        to: 'lahc.vrc.ponce@gmail.com',
        subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        body: """Build failed ❌

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
"""
      )
    } catch (err) {
	echo "Email failed (not failingbuild): ${err}"
    }	
  }
}

