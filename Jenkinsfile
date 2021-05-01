pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'arm64v8/python:3.9-buster'
                }
            }
            steps {
                sh '''
                    echo "[global]
                    extra-index-url=https://www.piwheels.org/simple" > /etc/pip.conf
                '''
                sh 'python -m pip install poetry'
                sh 'poetry install'
                sh 'poetry run pyinstaller systems/__main__.py --noconfirm'
                zip zipFile: 'relectric_systems_dist_x86.zip', archive: false, dir: 'dist/__main__/'
                archiveArtifacts artifacts: 'relectric_systems_dist_x86.zip', fingerprint: true
            }
        }
    }
}
