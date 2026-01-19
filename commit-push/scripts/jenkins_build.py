#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import os
import sys

import jenkins
from dotenv import load_dotenv

# ================= 日志配置 =================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, '.env')


def load_config():
    """从 .env 文件加载配置"""
    # 加载 .env 文件
    if os.path.exists(ENV_FILE):
        load_dotenv(ENV_FILE)
        logger.info(f"已加载配置文件: {ENV_FILE}")
    else:
        logger.warning(f"未找到 .env 文件 ({ENV_FILE})，将创建模板文件")
        # 如果 .env 不存在，尝试从 .env.example 创建
        env_example = os.path.join(SCRIPT_DIR, '.env.example')
        if os.path.exists(env_example):
            import shutil
            shutil.copy(env_example, ENV_FILE)
            logger.info(f"已从 {env_example} 创建 {ENV_FILE}")
            logger.warning("请编辑 .env 文件，填写您的 Jenkins API Token")
        load_dotenv(ENV_FILE)

    config = {
        'JENKINS_URL': os.getenv('JENKINS_URL', ''),
        'JENKINS_USERNAME': os.getenv('JENKINS_USERNAME', ''),
        'JENKINS_API_TOKEN': os.getenv('JENKINS_API_TOKEN', ''),
        'COMM_JOB_NAME': os.getenv('JENKINS_COMM_JOB_NAME', ''),
        'BUILD_PARAMS': {
            'BRANCH': os.getenv('JENKINS_BUILD_BRANCH', 'test'),
            'ENV': os.getenv('JENKINS_BUILD_ENV', 'test')
        },
        'TIMEOUT': int(os.getenv('JENKINS_TIMEOUT', '600')),
        'POLL_INTERVAL': int(os.getenv('JENKINS_POLL_INTERVAL', '10'))
    }

    return config


def trigger_build(username=None, with_sonar=False):
    """触发 Jenkins 构建"""
    config = load_config()

    # 使用命令行参数或配置文件中的用户名
    if not username:
        username = config['JENKINS_USERNAME']

    # 获取 API Token
    api_token = config.get('JENKINS_API_TOKEN', '')
    if not api_token or api_token == '请在此处填写您的API_Token':
        logger.error("未配置 Jenkins API Token，请在 .env 文件中设置 JENKINS_API_TOKEN")
        logger.error(f"配置文件路径: {ENV_FILE}")
        return 4

    # 使用配置的 Job 名称
    job_name = config['COMM_JOB_NAME']

    try:
        # 1. 连接 Jenkins
        logger.info("Connecting to Jenkins server...")
        server = jenkins.Jenkins(
            config['JENKINS_URL'],
            username=username,
            password=api_token,
            timeout=30
        )

        # 验证连接
        user = server.get_whoami()
        version = server.get_version()
        logger.info(f"Connected to Jenkins {version} as {user['fullName']}")

        # 2. 获取当前最新构建号
        try:
            last_build_number = server.get_job_info(job_name)['nextBuildNumber']
        except jenkins.NotFoundException:
            logger.error(f"Job '{job_name}' not found!")
            return 1
        except Exception as e:
            logger.error(f"Failed to get job info: {e}")
            return 1

        # 3. 准备构建参数
        final_params = config['BUILD_PARAMS'].copy()
        if with_sonar:
            final_params.update({
                'env.SonarQubeScanner': 'true',
                'SonarQubeScanner': 'true',
            })
            logger.info(f"Triggering build with SonarQube analysis: {job_name}")
        else:
            logger.info(f"Triggering build without SonarQube analysis: {job_name}")

        # 4. 触发构建
        if final_params:
            server.build_job(job_name, parameters=final_params)
            logger.info(f"With parameters: {final_params}")
        else:
            server.build_job(job_name)
        logger.info(f"Build triggered. Expected build number: #{last_build_number}")
        logger.info("Build URL: %s/job/%s/%s/" % (config['JENKINS_URL'], job_name, last_build_number))

        return 0

    except jenkins.JenkinsException as e:
        logger.error(f"Jenkins API error: {e}")
        return 2
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 3


def main():
    parser = argparse.ArgumentParser(description='触发 Jenkins 构建')
    parser.add_argument('-u', '--username', help='Jenkins 用户名（覆盖 .env 中的配置）')
    parser.add_argument('-s', '--sonar', action='store_true', help='启用 SonarQube 分析')
    args = parser.parse_args()

    return trigger_build(
        username=args.username,
        with_sonar=args.sonar
    )


if __name__ == '__main__':
    sys.exit(main())
