#!/usr/bin/env bash

java -jar selenium/selenium-server-standalone-2.43.1.jar \
    -role node \
    -hub http://localhost:4444/grid/register \
    -Dwebdriver.chrome.driver="./selenium/chromedriver" \
    -browser browserName=chrome,maxInstances=1 \
    -browser browserName=firefox,maxInstances=1
