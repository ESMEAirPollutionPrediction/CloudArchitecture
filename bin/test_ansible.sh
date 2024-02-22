#!/bin/bash
ansible-playbook --private-key="~/.ssh/ec2" -i ansible/hosts ansible/main.yml