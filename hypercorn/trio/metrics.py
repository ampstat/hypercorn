import trio


async def collect_metrics(receive_channel, metrics):
    async with receive_channel:
        async for value in receive_channel:
            metrics['total_requests'] += 1


async def log_metrics(metrics):
    prev = 0
    while True:
        total_requests = metrics['total_requests']
        reqps = total_requests - prev
        print(f'requests/s {reqps}')
        print(f'total requests {total_requests}')
        prev = total_requests
        await trio.sleep(1)
