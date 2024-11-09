pipeline {
    agent any

    environment {
        MAGENTO_BASE_URL = "http://mage2rock.magento.com"
        DB_HOST = "localhost"
        DB_NAME = "mage2rock"
        DB_USER = "mage2rock"
        DB_PASSWORD = "sarra123"
        ADMIN_USER = "rockadmin"
        ADMIN_PASSWORD = "sarra123"
    }

    stages {
        stage('Checkout') {
            steps {
                // Récupère le code source depuis le dépôt Git
               checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installe les dépendances Magento via Composer
                sh 'composer install'
            }
        }

        stage('Set Up Magento') {
            steps {
                // Installe Magento et configure la base de données
                sh '''
                    php bin/magento setup:install \
                        --base-url=${MAGENTO_BASE_URL} \
                        --db-host=${DB_HOST} \
                        --db-name=${DB_NAME} \
                        --db-user=${DB_USER} \
                        --db-password=${DB_PASSWORD} \
                        --admin-user=${ADMIN_USER} \
                        --admin-password=${ADMIN_PASSWORD} \
                        --language=en_US \
                        --currency=USD \
                        --timezone=America/Chicago \
                        --use-rewrites=1
                '''
            }
        }

        stage('Start PHP Built-in Web Server') {
            steps {
                // Démarre le serveur PHP intégré pour l'application Magento
                sh 'php -S 0.0.0.0:8080 -t pub'
            }
        }

        stage('Run Tests with Selenium') {
            steps {
                // Lance les tests Selenium pour vérifier les fonctionnalités de Magento
                // Exemple pour exécuter un script Selenium de test
                sh '''
                    # Commande pour exécuter les tests Selenium (modifiez selon votre configuration)
                    mvn clean test
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Générez le rapport Allure après l'exécution des tests
                allure includeProperties: false, jdk: '', results: [[path: 'target/allure-results']]
            }
        }

        stage('Clean Up') {
            steps {
                // Nettoyage des fichiers temporaires ou autres actions post-test
                sh 'rm -rf var/* pub/* generated/*'
            }
        }
    }

    post {
        success {
            // Actions en cas de succès, comme notifier que les tests ont réussi
            echo 'Tests passed successfully!'
        }
        failure {
            // Actions en cas d'échec, comme envoyer une alerte ou une notification
            echo 'Tests failed! Check the logs for more details.'
        }
    }
}
