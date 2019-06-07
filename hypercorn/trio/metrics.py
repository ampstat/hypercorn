from pathlib import Path
import statistics

import numpy
import trio


async def collect_metrics(config, receive_channel, metrics):
    async with receive_channel:
        async for data in receive_channel:
            if not config.metrics_tmppath:
                continue
            conn_id, req_id, start_end, counter = data
            if start_end == 'start':
                metrics['total_requests'] += 1
                metrics['request_start'][(conn_id, req_id)] = counter
            elif start_end == 'end':
                start = metrics['request_start'].pop((conn_id, req_id))
                end = counter
                duration = end - start
                metrics['request_duration'].append(duration)
            else:
                raise Exception('Unrecognised collect_metrics message')


async def log_metrics(config, metrics):
    if not config.metrics_tmppath:
        return
    while True:
        start = metrics['total_requests']
        await trio.sleep(config.metrics_period)
        end = metrics['total_requests']
        reqps = end - start

        request_duration = metrics['request_duration']

        if request_duration:
            # do calc on copy so that list does not change under you
            # potentially a large copy, so there should be a better way to do this
            li = request_duration.copy()
            request_duration.clear()
            mean = statistics.mean(li)
            median = statistics.median(li)
            if len(li) > 1:
                stdev = statistics.stdev(li)
                q5, q95, q99 = numpy.quantile(li, [0.5,0.95,0.99])
            else:
                stdev, q5, q95, q99 = 0, 0, 0, 0
        else:
            mean = 0
            median = 0
            stdev = 0
            q5, q95, q99 = 0, 0, 0

        fp = Path(config.metrics_tmppath) / 'quartmetrics' / 'metrics.txt'
        with fp.open('w') as f:
            log_metric_value(f, 'reqps', reqps, 'float', 'requests per second')
            log_metric_value(f, 'request_duration_mean', mean, 'float', 'requests per second')
            log_metric_value(f, 'request_duration_median', median, 'float', 'requests per second')
            log_metric_value(f, 'request_duration_stdev', stdev, 'float', 'requests per second')
            log_metric_value(f, 'request_duration_q5', q5, 'float', 'requests per second')
            log_metric_value(f, 'request_duration_q95', q95, 'float', 'requests per second')
            log_metric_value(f, 'request_duration_q99', q99, 'float', 'requests per second')
            log_metric_value(f, 'metrics_period', config.metrics_period, 'int', 'seconds')

def log_metric_value(f, name, value, type_str, unit):
    f.write(f'# NAME {name} TYPE {type_str} UNIT {unit}\n')
    f.write(f'{name} {value}\n')
