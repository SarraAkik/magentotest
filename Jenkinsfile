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
stages {
        stage('Setup Edge Driver') {
            steps {
                sh 'mkdir -p venv/bin'
                sh 'cp /usr/local/bin/msedgedriver/msedgedriver.exe venv/bin/'
                sh 'chmod +x venv/bin/msedgedriver.exe'
                sh 'export PATH=$PATH:venv/bin'
            }
        }
        stage('Run Tests') {
            steps {
                sh '../venv/bin/pytest test_magento.py --alluredir=../allure-results'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        failure {
            echo 'Les tests ont échoué. Vérifiez les rapports Allure.'
        }
    }
}
