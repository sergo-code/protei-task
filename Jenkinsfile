pipeline {
    agent any

    stages{
        stage('Docker Build') {
            steps {
                sh 'docker build -t protei_tests . < Dockerfile'
            }
        }
        stage('Tests') {
            steps {
                catchError {
                    sh """docker run --name protei_tests --network selenoid protei_tests"""
                }
            }
        }
        stage('Copy Artefact') {
            steps {
                sh 'docker cp protei_tests:/app/allure-results .'
            }
        }
        stage('Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }
    post {
        always {
            sh 'docker rm protei_tests'
        }
    }
}