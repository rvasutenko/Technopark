# ДЗ-6
## Измерения
### Отдача статического документа напрямую через nginx
```
Server Software:        nginx/1.27.3
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /sample.html
Document Length:        3222 bytes

Concurrency Level:      10
Time taken for tests:   0.060 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      3493000 bytes
HTML transferred:       3222000 bytes
Requests per second:    16761.93 [#/sec] (mean)
Time per request:       0.597 [ms] (mean)
Time per request:       0.060 [ms] (mean, across all concurrent requests)
Transfer rate:          57177.17 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:     0    0   0.3      0       3
Waiting:        0    0   0.3      0       2
Total:          0    1   0.4      0       3
ERROR: The median and mean for the total time are more than twice the standard
       deviation apart. These results are NOT reliable.

Percentage of the requests served within a certain time (ms)
  50%      0
  66%      0
  75%      1
  80%      1
  90%      1
  95%      1
  98%      2
  99%      2
 100%      3 (longest request)
```

### Отдача статического документа напрямую через gunicorn
```
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /static/sample.html
Document Length:        3222 bytes

Concurrency Level:      10
Time taken for tests:   0.398 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      3588000 bytes
HTML transferred:       3222000 bytes
Requests per second:    2509.53 [#/sec] (mean)
Time per request:       3.985 [ms] (mean)
Time per request:       0.398 [ms] (mean, across all concurrent requests)
Transfer rate:          8793.16 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     3    4   1.1      3      21
Waiting:        2    3   1.0      3      19
Total:          3    4   1.1      3      21

Percentage of the requests served within a certain time (ms)
  50%      3
  66%      4
  75%      4
  80%      4
  90%      4
  95%      5
  98%      8
  99%      9
 100%     21 (longest request)
```

### Отдача динамического документа напрямую через gunicorn
```
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /
Document Length:        23791 bytes

Concurrency Level:      10
Time taken for tests:   5.053 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      2408800 bytes
HTML transferred:       2379100 bytes
Requests per second:    19.79 [#/sec] (mean)
Time per request:       505.251 [ms] (mean)
Time per request:       50.525 [ms] (mean, across all concurrent requests)
Transfer rate:          465.58 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       0
Processing:   114  463  73.9    480     527
Waiting:      114  463  73.9    479     527
Total:        115  464  73.8    480     528

Percentage of the requests served within a certain time (ms)
  50%    480
  66%    484
  75%    493
  80%    499
  90%    503
  95%    507
  98%    527
  99%    528
 100%    528 (longest request)
```

### Отдача динамического документа через проксирование запроса с nginx на gunicorn
```
Server Software:        nginx/1.27.3
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /
Document Length:        23791 bytes

Concurrency Level:      10
Time taken for tests:   5.000 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      2409200 bytes
HTML transferred:       2379100 bytes
Requests per second:    20.00 [#/sec] (mean)
Time per request:       499.971 [ms] (mean)
Time per request:       49.997 [ms] (mean, across all concurrent requests)
Transfer rate:          470.57 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:   110  451  67.9    471     500
Waiting:      110  451  68.0    471     500
Total:        110  452  67.8    471     500

Percentage of the requests served within a certain time (ms)
  50%    471
  66%    475
  75%    476
  80%    477
  90%    479
  95%    482
  98%    496
  99%    500
 100%    500 (longest request)
```

### Отдача динамического документа через проксирование запроса с nginx на gunicorn, при кэшировние ответа на nginx (proxy cache)
```
Server Software:        nginx/1.27.3
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /
Document Length:        23791 bytes

Concurrency Level:      10
Time taken for tests:   0.272 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      2409200 bytes
HTML transferred:       2379100 bytes
Requests per second:    367.42 [#/sec] (mean)
Time per request:       27.217 [ms] (mean)
Time per request:       2.722 [ms] (mean, across all concurrent requests)
Transfer rate:          8644.42 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:     0    4  25.7      1     258
Waiting:        0    4  25.6      1     257
Total:          1    4  25.7      2     259

Percentage of the requests served within a certain time (ms)
  50%      2
  66%      2
  75%      2
  80%      2
  90%      2
  95%      2
  98%      3
  99%    259
 100%    259 (longest request)
```

## Насколько быстрее отдается статика по сравнению с WSGI?
Статика отдается в 6,6 раз быстрее

## Во сколько раз ускоряет работу proxy_cache?
Он ускоряет работу в 18,5 раз