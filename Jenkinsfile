pipeline {
    agent any
    stages {
        stage("Deployment") {
            agent {
                docker {
                    args '-p 8888:8888'
                    image 'python'
                    label '3.7.11'
                }
            }
            steps {
                sh 'pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ –-trusted-host mirrors.aliyun.com --timeout=60'
            }
            steps {
                sh 'python run.py'
            }
        }
    }
}