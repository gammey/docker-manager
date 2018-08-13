#!/bin/bash
cd ./dockerManager/
tar zcvf django.tar.gz ./
mv ./django.tar.gz ../
cd ../
docker rm -f docker-manager
docker build -t docker-manager ./
docker run -d -p 8001:8001 --name=docker-manager docker-manager
rm -rf ./django.tar.gz
