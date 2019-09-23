pipeline {
    agent {
        docker {
            image 'antoniocapizzi95/node-python:v1.0'
            args '-p 5002:5002 --name anomaly_detection'
            }
        }
        stages {

            stage('Install Dependencies') {
                         steps {
                             sh 'pip install requests'
                             sh 'pip install sklearn'
                             sh 'pip install slacker'
                             //sh 'pip install gitpython'
                         }
            }
            stage('Prepare Git') {
                         steps {
                             sh 'git config --global user.email ' //insert github email
                             sh 'git config --global user.name' //insert github name
                             sh 'git remote rm origin'
                             sh 'git remote add origin ' //insert origin of this project
                         }
            }

             stage('Deliver') {
                         steps {
                             sh 'python main.py'
                             sh 'git commit -a -m "Dataset Updated"'
                             sh 'git push -f origin HEAD:master'
                             sh 'python runad.py &'
                             input message: 'Click "proceed" to continue with release in production, click "abort" to cancel it', id: ' //insert pipeline job id
                             sh 'python runproduction.py &'
                         }
             }
        }
}