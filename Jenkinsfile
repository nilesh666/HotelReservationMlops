pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "bamboo-strata-467603-q8"
        GCLOUD_PATH = "var/jenkins_home/google-cloud-sdk/bin"
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

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }

        }

        stage('Building and pushing the docker image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'GCP-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo '.........Building and pushing the docker image to GCR.........'
                        sh '''

                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/hotelreservation:latest . 

                        docker push gcr.io/${GCP_PROJECT}/hotelreservation:latest 
                        
                        '''
                    }
                }
            }

        }
        
    }
    
}
