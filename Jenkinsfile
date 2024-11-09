pipeline {
    agent any

    environment {
        MAGENTO_BASE_URL = "http://mage2rock.magento.com" // Remplacez par l'URL de votre application Magento
        DB_HOST = "localhost"
        DB_NAME = "mage2rock"
        DB_USER = "mage2rock"
        DB_PASSWORD = "sarra123"
        ADMIN_USER = "rockadmin"
        ADMIN_PASSWORD = "sarra123"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                echo "Preparing environment for Magento tests..."
                
                // Assure-toi que PHP est installé et que composer est installé dans ton image
                sh 'php -v'
                sh 'composer -v'
                
                // Installe les dépendances PHP
                sh 'composer install'

                // Lancer le serveur web PHP intégré pour Magento (optionnel)
                sh 'php -S localhost:8000 -t /path/to/magento/root &'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests on Magento..."

                // Exécuter les tests Selenium
                sh 'php bin/phpunit --testsuite SeleniumTests'
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo "Generating Allure report..."
                
                // Générer les rapports avec Allure
                sh 'allure generate --clean'
            }
        }

        stage('Publish Report') {
            steps {
                echo "Publishing Allure report..."
                
                // Publier le rapport Allure dans Jenkins
                allure includeProperties: false, reportBuildPolicy: 'ALWAYS', reportPath: 'allure-report'
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            
            // Arrêter le serveur PHP si nécessaire
            sh 'pkill -f "php -S localhost:8000"'
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}
