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
                checkout scm
            }
        }

        stage('Install PHP and Composer') {
            steps {
                sh '''
                    # Use curl to download PHP (example for PHP 8.1, adjust version as necessary)
                    curl -LO https://www.php.net/distributions/php-8.1.0.tar.bz2
                    tar -xjf php-8.1.0.tar.bz2
                    cd php-8.1.0
                    ./configure --prefix=$HOME/php
                    make
                    make install

                    # Add PHP to the PATH
                    export PATH=$HOME/php/bin:$PATH

                    # Install Composer
                    curl -sS https://getcomposer.org/installer | php
                    mv composer.phar $HOME/bin/composer

                    # Add Composer to the PATH
                    export PATH=$HOME/bin:$PATH
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'composer install'
            }
        }

        stage('Setup Permissions') {
            steps {
                sh '''
                    find var generated vendor pub/static pub/media app/etc -type f -exec chmod g+w {} +
                    find var generated vendor pub/static pub/media app/etc -type d -exec chmod g+ws {} +
                '''
            }
        }

        stage('Magento Setup') {
            steps {
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
                sh 'php bin/magento setup:static-content:deploy -f'
            }
        }

        stage('Reindex Data') {
            steps {
                sh 'php bin/magento indexer:reindex'
            }
        }

        stage('Set Permissions Again') {
            steps {
                sh 'chmod -R 777 var/ pub/ generated/'
            }
        }

        stage('Cache Flush') {
            steps {
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
