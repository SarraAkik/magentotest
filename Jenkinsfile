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

      stage('Setup Edge Driver') {
    steps {
        // Téléchargement manuel du driver ou utilisation d'un chemin existant
        sh 'cp /usr/local/bin/msedgedriver venv/bin/'
        sh 'chmod +x venv/bin/msedgedriver'
        sh 'export PATH=$PATH:venv/bin'
        // Vérifier si le driver est bien présent
        sh 'which msedgedriver || echo "msedgedriver not found"'
        sh 'msedgedriver --version || echo "Cannot execute msedgedriver"'
    }
}


        stage('Run Tests') {
            steps {
                // Exécuter les tests avec pytest
                sh "./${VENV_PATH}/pytest ${TEST_DIR}/test_magento.py --alluredir=${ALLURE_RESULTS}"
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
