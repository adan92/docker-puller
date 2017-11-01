#!/bin/bash
scriptDir=`dirname $0`

timestamp() {
  date +"%d/%m/%y %H:%M:%S"
}

echo "[$(timestamp)] $*"  >> $PWD/$scriptDir/logs/testing.log

