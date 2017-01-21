#!/bin/bash

set -e

dir="$(pwd)"

zip -ru piggydash.zip ./*.py secrets.yml

source ~/.virtualenvs/piggydash/bin/activate
pip install -r requirements.txt
deactivate

pushd ~/.virtualenvs/piggydash/lib/python2.7/site-packages
zip -ru $dir/piggydash.zip ./*
popd

aws lambda update-function-code \
  --profile=bjacobel \
  --function-name piggydash \
  --zip-file fileb://$dir/piggydash.zip
