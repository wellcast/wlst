#!/bin/bash
if test "$USER" != "oracle"; then
        echo "INVALID!"
        echo
        exit
fi

domain_name = ""
admin_name = ""
dt = `date +%d%m%Y_%H%M%S`

nohup /domains/${domain_name}/startWebLogic.sh > /log/${domain_name}/${admin_name}/${admin_name}_${dt}.out 2>&1 &

echo
echo tail -500f /log/${domain_name}/${admin_name}/${admin_name}_${dt}.out
echo
