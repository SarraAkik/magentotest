pipeline {
    agent any

    environment {
        VENV_PATH = 'venv/bin'
        TEST_DIR = 'tests'
        ALLURE_RESULTS = 'allure-results'
        EDGE_DRIVER_PATH = '/usr/local/bin/msedgedriver.exe'
        PATH = "$PATH:venv/bin"
    }

    stages {
        stage('Cloner le dépôt') {
            steps {
                // Cloner le dépôt Git
                git url: 'https://github.com/SarraAkik/magentotest.git', branch: 'main'
            }
        }

        stage('Configurer l\'environnement virtuel Python') {
            steps {
                // Créer un environnement virtuel
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
            }
        }

        stage('Installer les dépendances Python') {
            steps {
                // Installer les dépendances nécessaires (selenium, pytest, allure-pytest)
                sh "./${VENV_PATH}/pip install selenium pytest allure-pytest"
            }
        }

        stage('Configurer WebDriver Edge') {
            steps {
                // Copier le fichier msedgedriver.exe dans le répertoire venv/bin
                sh "cp ${EDGE_DRIVER_PATH} venv/bin/msedgedriver.exe"

                // Donner les permissions d'exécution au WebDriver
                sh 'chmod +x venv/bin/msedgedriver.exe'

                // Vérifier si le driver est bien copié
                sh 'ls -l venv/bin'
            }
        }

        stage('Exécuter les tests') {
            steps {
                // Exécuter les tests avec pytest et générer des résultats Allure
                sh "./${VENV_PATH}/pytest ${TEST_DIR}/test_magento.py --alluredir=${ALLURE_RESULTS}"
            }
        }
    }

    post {
        always {
            // Nettoyer l'espace de travail après chaque exécution
            cleanWs()
        }
        failure {
            // Message en cas d'échec du test
            echo 'Les tests ont échoué. Vérifiez les rapports Allure.'
        }
    }
}
