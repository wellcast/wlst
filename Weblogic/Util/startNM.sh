#!/bin/bash
if test "$USER" != "user"; then
        echo "INVALID!"
        echo
        exit
fi

dt = `date +%d%m%Y_%H%M%S`

nohup /oracle/wlserver_10.3/server/bin/startNodeManager.sh > /log/nodemanager/startNodemanager_${dt}.out 2>&1 &

echo
echo tail -500f /log/nodemanager/startNodemanager_${dt}.out
echo

