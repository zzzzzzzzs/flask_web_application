pipeline {
    agent {
        node {
            label "ali-node"
        }
    }

    parameters {
        string(name: 'VENV_NAME', defaultValue: 'flask_web_application', description: '同项目名')
    }

    stages {
        stage("Checkout") {
            steps {
                git branch: 'main', url: 'https://github.com/zzzzzzzzs/flask_web_application.git'
            }
        }

        stage("Build") {
            steps {
                sh "pyenv activate ${params.VENV_NAME}"
                sh "pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --timeout 60"
                echo "pip install done"
            }
        }

        stage("Test") {
            steps {
                sh '''
                    pyenv activate ${params.VENV_NAME}
                    pytest -s --cov --report=test_report.html --title=测试报告 --tester=zzs --desc=项目描述 --template=2
                '''
            }
        }

        stage("Deployment") {
            steps {
                sh '''
                    pyenv activate ${params.VENV_NAME}
                    python run.py
                '''
            }
        }
    }
}
