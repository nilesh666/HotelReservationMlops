pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning github repo to Jenkins'){
            steps{
                script{
                    echo '.......Cloning github repo to Jenkins.......'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/nilesh666/HotelReservationMlops.git']])
                }
            }
        }
    }

        stages{
        stage('Setting venv and installing dependencies'){
            steps{
                script{
                    echo '.......Setting venv and installing dependencies.......'
                    sh '''

                    python -m venv ${VENV_DIR}
                    .${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}
