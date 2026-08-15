pipeline {
    agent any

    stages {
        stage('Downloading the code') {
            steps {
                checkout scm
            }
        }

        stage('Preparing the environment') {
            steps {
                
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Installing Playwright browsers') {
            steps {
                
                sh '''
                    . venv/bin/activate
                    playwright install --with-deps chromium
                '''
            }
        }

        stage('Running E2E tests') {
            steps {
                
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=test-results/results.xml
                '''
            }
        }
    }

    post {
        always {
            
            junit 'test-results/results.xml'
        }
    }
}
