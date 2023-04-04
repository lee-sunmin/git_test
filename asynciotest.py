import asyncio
from signal import SIGINT, SIGTERM


async def main():
    loop = asyncio.get_running_loop()
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)   #1

    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        for i in range(3):
            print('Your app is shutting down...')
            await asyncio.sleep(1)


def handler(sig):
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop=loop):        #2
        task.cancel()
    print(f'Got signal: {sig!s}, shutting down.')
    loop.remove_signal_handler(SIGTERM)              #3
    loop.add_signal_handler(SIGINT, lambda: None)    #4


if __name__ == '__main__':
    asyncio.run(main())