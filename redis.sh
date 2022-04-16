redis-server --loadmodule /home/young/Desktop/code/RedisTimeSeries/bin/redistimeseries.so config/redis.conf

echo 'redis-cli'
echo 'config get maxmemory'
echo 'config set maxmemory 4GB'
echo 'config get maxmemory'

