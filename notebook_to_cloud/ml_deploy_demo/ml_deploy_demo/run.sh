#!/usr/bin/env bash
export IS_DEBUG=${DEBUG:-false}
echo PWDPWD $PWD
exec gunicorn --bind 0.0.0.0:5000 --reload --access-logfile - --error-logfile - ml_deploy_demo.run:app
