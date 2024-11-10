pipeline {
    agent any

    environment {
        VENV_PATH = 'venv/bin'
        TEST_DIR = 'tests'
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Cloner le dépôt') {
            steps {
                git url: 'https://github.com/SarraAkik/magentotest.git', branch: 'main'
            }
        }

        stage('Configurer l\'environnement virtuel Python') {
            steps {
                // Créer un environnement virtuel dans le répertoire courant
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
            }
        }

        stage('Installer les dépendances Python') {
            steps {
                sh "./${VENV_PATH}/pip install selenium pytest allure-pytest"
            }
        }

stage('Configurer EdgeDriver') {
    steps {
        // Copier tout le contenu du répertoire msedgedriver vers le répertoire bin du venv
        sh 'cp -r /usr/local/bin/msedgedriver/* venv/bin/'
        // Donner les permissions d'exécution
        sh 'chmod +x venv/bin/msedgedriver'
    }
}


        stage('Exécuter les tests Selenium') {
            steps {
                dir("${TEST_DIR}") {
                    sh "../${VENV_PATH}/pytest test_magento.py --alluredir=../${ALLURE_RESULTS}"
                }
            }
        }

        stage('Générer le rapport Allure') {
            steps {
                allure includeProperties: false, reportBuildPolicy: 'ALWAYS', results: [[path: "${ALLURE_RESULTS}"]]
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Les tests se sont exécutés avec succès !'
        }
        failure {
            echo 'Les tests ont échoué. Vérifiez les rapports Allure.'
        }
    }
}
