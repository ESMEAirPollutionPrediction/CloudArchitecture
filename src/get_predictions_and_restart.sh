#!/bin/bash
aws s3 cp s3://esme-pollution-bucket/predictions/ ~/data/predictions/ --recursive --profile ESMEAdmin
supervisorctl restart Flask