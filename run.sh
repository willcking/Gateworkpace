#!/bin/bash

# 检查是否已经有相同名称的进程在运行
if pgrep -f "/root/gtchainprice/project/multi2.py" > /dev/null; then
    echo "Another instance of multi2.py is already running. Exiting."
    exit 1
else
    echo "No duplicate process found. Proceeding with execution."
    # 这里可以放置启动multi2.py的代码
    cd /root/gtchainprice/ && PYTHONPATH=$PYTHONPATH:/root/gtchainprice/ /root/venv39/bin/python /root/gtchainprice/project/multi2.py
fi
