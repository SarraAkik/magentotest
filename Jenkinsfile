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
        PHP_BIN_PATH = "/path/to/php"  // Update this to your PHP binary location
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone Magento repository
                checkout scm
            }
        }

        stage('Install PHP and Composer') {
            steps {
                script {
                    // Download PHP Binary if not already available
                    sh '''
                        if [ ! -f ${PHP_BIN_PATH}/php ]; then
                            echo "PHP binary not found, downloading..."
                            curl -LO https://www.php.net/distributions/php-8.1.0.tar.gz
                            tar -xzf php-8.1.0.tar.gz
                            cd php-8.1.0
                            ./configure --prefix=${PHP_BIN_PATH} --enable-fpm --with-openssl --with-curl --enable-mbstring --with-mysqli
                            make
                            make install
                        fi
                    '''
                }
                // Install Composer globally
                sh '''
                    curl -sS https://getcomposer.org/installer | php
                    mv composer.phar /usr/local/bin/composer
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install Magento dependencies via Composer
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
                    ${PHP_BIN_PATH}/bin/magento setup:install \
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
                sh '${PHP_BIN_PATH}/bin/magento setup:static-content:deploy -f'
            }
        }

        stage('Reindex Data') {
            steps {
                sh '${PHP_BIN_PATH}/bin/magento indexer:reindex'
            }
        }

        stage('Set Permissions Again') {
            steps {
                sh 'chmod -R 777 var/ pub/ generated/'
            }
        }

        stage('Cache Flush') {
            steps {
                sh '${PHP_BIN_PATH}/bin/magento cache:flush'
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
