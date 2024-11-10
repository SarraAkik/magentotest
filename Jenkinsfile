pipeline {
    agent any

    environment {
        PYTHON_VERSION = "python3"  // Utilise python3 comme version par défaut
    }

    stages {
        // Étape de vérification et installation de Python
        stage('Check and Install Python') {
            steps {
                script {
                    // Vérifie si Python est installé en essayant de récupérer la version
                    def pythonInstalled = sh(script: 'which python3 || true', returnStdout: true).trim()

                    if (pythonInstalled == '') {
                        echo 'Python3 not found. Installing Python...'
                        // Installe Python si ce n'est pas déjà fait (sur Ubuntu/Debian)
                        sh '''
                        sudo apt-get update
                        sudo apt-get install -y python3 python3-pip
                        '''
                    } else {
                        echo 'Python3 is already installed.'
                    }
                }
            }
        }

        // Étape de checkout pour récupérer le code source
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Étape pour configurer l'environnement Python et installer les dépendances
        stage('Setup Python Environment') {
            steps {
                script {
                    // Créer un environnement virtuel et installer les dépendances nécessaires
                    sh "${PYTHON_VERSION} -m venv venv"
                    sh ". venv/bin/activate && pip install --upgrade pip && pip install selenium pytest allure-pytest"
                }
            }
        }

        // Étape pour exécuter les tests Selenium
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

        // Étape pour générer le rapport Allure
        stage('Allure Report') {
            steps {
                // Génère et publie le rapport Allure
                allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            // Nettoie l'environnement de travail après chaque exécution
            cleanWs()
        }
        success {
            // Affiche un message en cas de succès
            echo 'Tests completed successfully!'
        }
        failure {
            // Affiche un message en cas d'échec
            echo 'Tests failed. Check the Allure report for details.'
        }
    }
}
