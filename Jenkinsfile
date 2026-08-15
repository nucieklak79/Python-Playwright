pipeline {
    agent any

    stages {
        stage('Pobranie kodu') {
            steps {
                checkout scm
            }
        }

        stage('Przygotowanie środowiska') {
            steps {
                // Aktywujemy środowisko i instalujemy pakiety
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Instalacja przeglądarek Playwright') {
            steps {
                // Instalujemy Chromium ze wszystkimi zależnościami systemowymi Linuksa
                sh '''
                    . venv/bin/activate
                    playwright install --with-deps chromium
                '''
            }
        }

        stage('Uruchomienie testów E2E') {
            steps {
                // Uruchamiamy testy i generujemy raport XML dla Jenkinsa
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=test-results/results.xml
                '''
            }
        }
    }

    post {
        always {
            // Ten krok wykona się zawsze, rysując wykresy z wynikami testów
            junit 'test-results/results.xml'
        }
    }
}
