#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

URL=$1
if [ -z "$1" ]
  then
    echo "No request url provided."
    exit 2
fi

curl -X POST -H "Content-Type: application/json"  -H "X_EVENT_KEY: repo:push" -d @$BASEDIR/repo-push.json $URL