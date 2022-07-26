import asyncio
import time
from availability_checker.checker import AvailabilityChecker


def main():
    while True:
        hosts = [
                    {
                        'server': 'knst.me',
                        'port': 443,
                        'method': 'https',
                        'path': '/'
                    },
                    {
                        'server': 'knst.me',
                        'port': 80,
                        'method': 'http',
                        'path': '/'
                    },
                    {
                        'server': 'knst.me',
                        'port': 80,
                        'method': 'https',
                        'path': '/'
                    },
                ]

        for host in hosts:
            checker = AvailabilityChecker(host).check()
            print(checker)

        time.sleep(5)


if __name__ == '__main__':
    main()
