pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:3.9'
                }
            }
            steps {
                sh 'python -m pip install poetry'
                sh 'poetry install'
                sh 'poetry run pyinstaller systems/__main__.py --noconfirm'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'dist/__main__/**', fingerprint: true
                }
            }
        }
    }
}
