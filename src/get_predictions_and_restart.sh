#!/bin/bash
sudo aws s3 cp s3://esme-pollution-bucket/predictions/ ~/data/predictions/ --recursive
sudo supervisorctl restart Flask