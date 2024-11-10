pipeline {
    agent any

    environment {
        VENV_PATH = '/venv/bin'
        TEST_DIR = 'tests'
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Préparer Git') {
            steps {
                sh 'git config --global http.postBuffer 524288000' // 500MB
            }
        }

        stage('Cloner le dépôt') {
            steps {
                git url: 'https://github.com/votre-repository/magento-tests.git', branch: 'main'
            }
        }

        stage('Installer les dépendances') {
            steps {
                sh "${VENV_PATH}/pip install -r requirements.txt"
            }
        }

        stage('Exécuter les tests Selenium') {
            steps {
                dir("${TEST_DIR}") {
                    sh "${VENV_PATH}/pytest --alluredir=${ALLURE_RESULTS}"
                }
            }
        }

        stage('Générer le rapport Allure') {
            steps {
                allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: "${ALLURE_RESULTS}"]]
            }
        }
    }

    post {
        always {
            // Entourer cleanWs avec node
            node {
                cleanWs()
            }
        }
        success {
            echo 'Les tests se sont exécutés avec succès !'
        }
        failure {
            echo 'Les tests ont échoué. Vérifiez les rapports Allure.'
        }
    }
}
