pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat  'docker build -t sampleapp -f SampleApp/Dockerfile .'
            }
        }
        stage('Push image') {
         steps {
           withDockerRegistry([url: "https://536703334988.dkr.ecr.ap-southeast-2.amazonaws.com/test-repository",credentialsId: "ecr:ap-southeast-2:demo-ecr-credentials"]) {
           bat 'docker push sampleapp:latest'
               }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}