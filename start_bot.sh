#!/bin/bash

DATE=`date '+%Y%m%d'`
PWD="$(dirname ${BASH_SOURCE[0]})"
LOG_DIR="${PWD}/logs"

if [ ! -d $LOG_DIR ]
then
	mkdir -p $LOG_DIR
fi

stdbuf -oL python ${PWD}/bot.py >> ${LOG_DIR}/${DATE}.log &