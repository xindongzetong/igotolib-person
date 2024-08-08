#!/bin/bash
echo "开始运行"
memcached -d -u root -p 11211 -m 128M -c 256 -P /tmp/memcached.pid
python main.py