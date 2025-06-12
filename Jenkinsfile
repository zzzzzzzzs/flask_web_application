pipeline {
    agent {
        node {
            label "ali-node"
        }
    }

    parameters {
        string(name: 'VENV_NAME', defaultValue: 'flask_web_application', description: '同项目名')
        string(name: 'VENV_PATH', defaultValue: '/root/.pyenv/versions/flask_web_application', description: '虚拟环境目录')
    }

    stages {
        stage("Checkout") {
            steps {
                git branch: 'main', url: 'https://github.com/zzzzzzzzs/flask_web_application.git'
            }
        }

        stage("Build") {
            steps {
                sh "${params.VENV_PATH}/bin/pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --timeout 60"
                echo "pip install done"
            }
        }

        stage("Test") {
            steps {
                sh "${params.VENV_PATH}/bin/python -m pytest -s --cov --report=test_report.html --title=测试报告 --tester=zzs --desc=项目描述 --template=2"
            }
        }

        stage("Deployment") {
            steps {
                sh "${params.VENV_PATH}/bin/python run.py"
            }
        }
    }
}
