pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        VENV = 'venv'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright browsers') {
            steps {
                // --with-deps also installs the OS libraries Chromium needs.
                // This requires apt/root access on the agent. If that's not
                // available on your Jenkins host, run this pipeline on the
                // official Playwright image instead, e.g.:
                //   agent { docker { image 'mcr.microsoft.com/playwright/python:v1.41.0-jammy' } }
                sh '''
                    . ${VENV}/bin/activate
                    playwright install --with-deps chromium
                '''
            }
        }

        stage('Lint') {
            steps {
                // Non-blocking: surfaces style/unused-import issues in the
                // console log without failing the build.
                sh '''
                    . ${VENV}/bin/activate
                    pip install flake8
                    flake8 pages tests utils --max-line-length=120 || true
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    mkdir -p results
                    pytest --junitxml=results/junit.xml -v
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'results/junit.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'results/**', allowEmptyArchive: true
        }
        success {
            echo 'All SauceDemo tests passed.'
        }
        failure {
            echo 'Build failed - check the JUnit report and console output above.'
        }
        cleanup {
            sh 'rm -rf ${VENV}'
        }
    }
}
