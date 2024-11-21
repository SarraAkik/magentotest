pipeline {
    agent any

    environment {
environment {
    VENV_PATH = 'venv/bin'
    TEST_DIR = 'tests'
    EDGE_DRIVER_PATH = 'C:\\Users\\hamza\\Downloads\\edgedriver_win64\\msedgedriver.exe'
    PATH = "$PATH:venv/bin"
}
steps {
    sh 'git config --global http.postBuffer 524288000'
}

  
        stages {
        stage('Checkoutscm') {
            steps {
                // Checkout the source code from the repository
                checkout scm
            }
        }

        stage('build') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install selenium pytest'
            }
        

       
            steps {
                sh "./${VENV_PATH}/pip install selenium pytest"
            }
      
       
            steps {
                sh "cp ${EDGE_DRIVER_PATH} venv/bin/"
                sh 'chmod +x venv/bin/msedgedriver'
                sh 'ls -l venv/bin'
            }
        }

        stage('Test') {
            steps {
                sh "./${VENV_PATH}/pytest ${TEST_DIR}/"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            echo 'Les tests ont échoué. Vérifiez les captures d\'écran.'
        }
    }
}
