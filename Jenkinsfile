pipeline {
  agent any

    environment {
        PYTHON_VERSION = '/venv/bin/python'  // Chemin vers l'interpréteur Python de l'environnement virtuel
        PYTHON_ENV = '/venv/bin/activate'   // Activation de l'environnement virtuel Python
        ALLURE_RESULTS = 'allure-results'   // Répertoire pour les résultats des tests
        ALLURE_REPORT = 'allure-report'     // Répertoire pour le rapport Allure
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Créer un environnement virtuel Python et installer les dépendances nécessaires
                    sh """
                    . $PYTHON_ENV && pip install --upgrade pip && pip install selenium pytest allure-pytest
                    """
                }
            }
        }

        stage('Run Selenium Test') {
            steps {
                script {
                    // Exécuter les tests avec pytest et générer les résultats Allure
                    sh """
                    . $PYTHON_ENV && pytest --alluredir=${ALLURE_RESULTS} tests/test_magento.py
                    """
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    // Générer le rapport Allure à partir des résultats des tests
                    sh 'allure generate ${ALLURE_RESULTS} --clean -o ${ALLURE_REPORT}'
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    includeProperties: true,
                    jdk: '',
                    results: [[path: "${ALLURE_REPORT}"]],
                    reportBuildPolicy: 'ALWAYS'
                ])
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
