import redis, json
r = redis.Redis().pubsub()
# Use psubscribe when using pattern matching.
r.subscribe('device.12345678901')

for data_raw in r.listen():
    print json.dumps(data_raw)


