#i/bin/sh

ps -ef | grep 'trigger.py thread'

pid1=`ps -ef|grep 'trigger.py thread' | grep  'python3'|awk '{print($2)}'`

#pid2=`ps -ef|grep 'trigger.py thread' | grep  'grep'|awk '{print($2)}'`

echo "kill process $pid1"

kill -9 ${pid1}

#kill -9 ${pid2}
