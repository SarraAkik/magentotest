pipeline {
    agent any

    environment {
        PYTHON_VERSION = "python3"
    }

    stages {
        stage('Check and Install Python') {
            steps {
                script {
                    // Vérifie si Python est installé
                    def pythonInstalled = sh(script: 'which python3 || true', returnStdout: true).trim()

                    if (pythonInstalled == '') {
                        echo 'Python3 not found. Installing Python...'

                        // Utiliser curl pour télécharger et installer Python
                        sh '''
                        curl -O https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
                        tar -xzf Python-3.9.6.tgz
                        cd Python-3.9.6
                        ./configure --prefix=$HOME/python
                        make
                        make install
                        export PATH=$HOME/python/bin:$PATH
                        '''
                    } else {
                        echo 'Python3 is already installed.'
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Créer un environnement virtuel et installer les dépendances nécessaires
                    sh "${PYTHON_VERSION} -m venv venv"
                    sh ". venv/bin/activate && pip install --upgrade pip && pip install selenium pytest allure-pytest"
                }
            }
        }

        stage('Run Selenium Test') {
            steps {
                script {
                    // Exécute les tests avec pytest et génère les résultats Allure
                    sh """
                    . venv/bin/activate
                    ${PYTHON_VERSION} -m pytest --alluredir=allure-results tests/test_magento.py
                    """
                }
            }
        }

        stage('Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Tests completed successfully!'
        }
        failure {
            echo 'Tests failed. Check the Allure report for details.'
        }
    }
}
