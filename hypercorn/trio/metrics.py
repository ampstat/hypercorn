from pathlib import Path
import statistics

import numpy
import trio


async def collect_metrics(receive_channel, metrics):
    async with receive_channel:
        async for data in receive_channel:
            if not config.metric_tmppath:
                continue
            metrics['total_requests'] += 1
            conn_id, req_id, start_end, counter = data
            if start_end == 'start':
                metrics['request_span'][(conn_id, req_id)].append(counter)
            else:
                start, end = metrics['request_span'].pop(conn_id, req_id)
                duration = end - start
                metrics['request_duration'].append(duration)


async def log_metrics(config, metrics):
    if not config.metrics_tmppath:
        return
    while True:
        start = metrics['total_requests']
        await trio.sleep(config.metrics_period)
        end = metrics['total_requests']

        request_duration = metrics['request_duration']

        if request_duration:
            # do calc on copy so that list does not change under you
            # potentially a large copy, so there should be a better way to do this
            li = request_duration.copy()
            request_duration.clear()
            mean = statistics.mean(li)
            median = statistics.median(li)
            stdev = statistics.stdev(li)
            q5, q95, q99 = numpy.quantile(li, [0.5,0.95,0.99])
        else:
            mean = 0
            median = 0
            stdev = 0
            q5, q95, q99 = 0, 0, 0

        fp = Path(config.metrics_tmppath) / 'quartmetrics' / 'metrics.txt'
        with fp.open('w') as f:
            f.write('reqps ' + str(end - start) + ' # req/s')
            f.write('request_duration_mean ' + str(mean) + ' # request_duration_mean period ' + str(config.metrics_period) + 's\n')
            f.write('request_duration_median ' + str(median) + ' # request_duration_median period ' + str(config.metrics_period) + 's\n')
            f.write('request_duration_stdev ' + str(stdev) + ' # request_duration_stdev period ' + str(config.metrics_period) + 's\n')
            f.write('request_duration_q5 ' + str(q5) + ' # request_duration_q5 period ' + str(config.metrics_period) + 's\n')
            f.write('request_duration_q95 ' + str(q95) + ' # request_duration_q95 period ' + str(config.metrics_period) + 's\n')
            f.write('request_duration_q99 ' + str(q99) + ' # request_duration_q99 period ' + str(config.metrics_period) + 's\n')
            f.write('metrics_period ' + str(config.metrics_period) + ' # metrics_period secs\n')
