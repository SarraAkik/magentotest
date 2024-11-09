pipeline {
    agent any

    environment {
        MAGENTO_BASE_URL = "http://mage2rock.magento.com"
        DB_HOST = "mysql"  // Nom du service MySQL dans Docker
        DB_NAME = "mage2rock"
        DB_USER = "mage2rock"
        DB_PASSWORD = "sarra123"
        ADMIN_USER = "rockadmin"
        ADMIN_PASSWORD = "sarra123"
    }

    stages {
        stage('Configure Git') {
            steps {
                sh 'git config --global http.postBuffer 524288000'
                sh 'git config --global core.compression 0'
                sh 'git config --global http.version HTTP/1.1'
            }
        }

        stage('Checkout') {
            steps {
                // Checkout the source code from the repository
                checkout scm
            }
        }

        stage('MySQL Setup') {
            steps {
                script {
                    def dbHost = "${DB_HOST}"
                    def dbUser = "${DB_USER}"
                    def dbPassword = "${DB_PASSWORD}"
                    def dbName = "${DB_NAME}"

                    // Vérification de la connexion à la base de données sans afficher les tables
                    sh """
                        mysql -h ${dbHost} -u ${dbUser} -p${dbPassword} ${dbName} -e "SELECT 1;"
                    """
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Checking PHP and Composer versions..."
                sh 'php -v' // Vérifie la version de PHP
                sh 'composer -v' // Vérifie la version de Composer

                echo "Installing PHP dependencies with Composer..."
                sh 'composer install --no-interaction -vvv' // Ajoute des détails en cas d’erreur
            }
        }

        stage('Setup Permissions') {
            steps {
                echo "Setting file and directory permissions..."
                // Appliquer les permissions nécessaires aux fichiers et répertoires Magento
                sh '''
                    find var generated vendor pub/static pub/media app/etc -type f -exec chmod g+w {} +
                    find var generated vendor pub/static pub/media app/etc -type d -exec chmod g+ws {} +
                '''
            }
        }

        stage('Magento Setup') {
            steps {
                echo "Setting up Magento..."
                // Exécuter la commande de configuration de Magento
                sh '''
                    php bin/magento setup:install \
                        --base-url="${MAGENTO_BASE_URL}" \
                        --db-host="${DB_HOST}" \
                        --db-name="${DB_NAME}" \
                        --db-user="${DB_USER}" \
                        --db-password="${DB_PASSWORD}" \
                        --admin-firstname="Admin" \
                        --admin-lastname="User" \
                        --admin-email="admin@example.com" \
                        --admin-user="${ADMIN_USER}" \
                        --admin-password="${ADMIN_PASSWORD}" \
                        --language="en_US" \
                        --currency="USD" \
                        --timezone="America/Chicago" \
                        --use-rewrites="1"
                '''
            }
        }

        stage('Build Static Content') {
            steps {
                echo "Deploying static content for Magento..."
                // Déployer les fichiers statiques pour Magento
                sh 'php bin/magento setup:static-content:deploy -f'
            }
        }

        stage('Reindex Data') {
            steps {
                echo "Reindexing Magento data..."
                // Réindexer les données Magento
                sh 'php bin/magento indexer:reindex'
            }
        }

        stage('Set Permissions Again') {
            steps {
                echo "Setting file and directory permissions again after setup..."
                // Appliquer les permissions une nouvelle fois après la configuration de Magento
                sh 'chmod -R 777 var/ pub/ generated/'
            }
        }

        stage('Cache Flush') {
            steps {
                echo "Flushing Magento cache..."
                // Vider le cache Magento
                sh 'php bin/magento cache:flush'
            }
        }
    }

    post {
        success {
            echo 'Magento build and deployment successful!'
        }
        failure {
            echo 'Magento build or deployment failed.'
        }
    }
}
