pipeline {
    agent any
    stages {
        stage("Deployment") {
            agent {
                docker {
                    args '-p 8888:8888'
                    image 'python:3.7.11'
                }
            }
            steps {
                retry(3) {
                    sh 'pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --timeout 60'
                }
                sh 'nohup python -u run.py > ./logs/nohup.out 2>&1 &'
            }
        }
    }
}
