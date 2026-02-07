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
        emailext(
          to: 'lahc.vrc.ponce@gmail.com',
          subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
          body: """Build succeeded ✅

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
        echo "Email failed (not failing build): ${err}"
      }
    }
  }
}

