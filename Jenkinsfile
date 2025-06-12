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
            sh '''
                git checkout ${git_tag}
            '''
        }

        stage("Build") {
            sh '''
                pyenv activate ${params.VENV_NAME}
                pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --timeout 60
            '''
            echo "pip install done"
        }

        stage("Test") {
            sh '''
                pyenv activate ${params.VENV_NAME}
                pytest -s --cov --report=test_report.html --title=测试报告 --tester=zzs --desc=项目描述 --template=2
            '''
        }

        stage("Deployment") {
            sh '''
                pyenv activate ${params.VENV_NAME}
                python run.py
            '''
        }
    }
}
