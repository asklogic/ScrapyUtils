

echo $1

nohup python3 -u trigger.py thread $1 >thread.out 2>&1 &

pid=` ps -ef|grep 'trigger.py thread' | grep  'grep'|awk '{print($2)}'`

echo $pid


