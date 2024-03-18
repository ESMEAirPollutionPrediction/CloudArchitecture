#!/bin/bash
aws s3 cp s3://esme-pollution-bucket/predictions/ /home/ubuntu/data/predictions/ --recursive --profile ESMEAdmin