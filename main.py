import asyncio
import time
from availability_checker.checker import AvailabilityChecker


async def main():
    while True:
        hosts = [
                    {
                        'server': 'knst.me',
                        'port': 443,
                        'method': 'https',
                        'path': '/pub/'
                    },
                    {
                        'server': 'knst.me',
                        'port': 80,
                        'method': 'http',
                        'path': '/'
                    },
                    # Intentionally broken
                    {
                        'server': 'knst.me',
                        'port': 80,
                        'method': 'https',
                        'path': '/'
                    },
                ]

        for host in hosts:
            checker = await AvailabilityChecker(host).check()
            print(checker)

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
