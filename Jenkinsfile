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
                stash(name: 'output_x86', includes: 'dist/__main__/**')
            }
        }
    }
}
