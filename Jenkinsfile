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
                zip zipFile: 'relectric_systems_dist_x86.zip', archive: false, dir: 'dist/__main__/'
                archiveArtifacts artifacts: 'relectric_systems_dist_x86.zip', fingerprint: true
            }
        }
    }
}
