import asyncio
import aiohttp
import logging

# logging.basicConfig(level=logging.INFO)


class AvailabilityChecker:
    host = {}
    status = {}

    def __init__(self, host):
        if len(host) > 0:
            self.host = host
        else:
            logging.exception("No host provided")
            raise Exception("No host provided")

    async def check_http(self):
        checking_host = f"{self.host['method']}://{self.host['server']}:{self.host['port']}{self.host['path']}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(checking_host) as response:
                    self.status = {
                        'status': 'online',
                        'response_code': response.status,
                        'url': response.host,
                        'method': response.method,
                        'content_type': response.content_type,
                        'content_length': response.content_length
                    }

                    logging.info(f"Host {checking_host} is online")
                    logging.info(f"Status: {response.status}")
                    logging.info(f"Content-type: {response.headers['content-type']}")
        except aiohttp.ClientConnectionError as e:
            self.status = {
                'status': 'offline',
                'response_code': 0,
                'url': checking_host,
                'method': '',
                'content_type': '',
                'content_length': ''
            }

            # logging.info(f"Connection error to: {checking_host}")
            logging.info(f"{e}")

    async def check_https(self):
        return await self.check_http()

    def check(self):
        if self.host['method'] == 'http':
            asyncio.run(self.check_http())

            return self.status
        elif self.host['method'] == 'https':
            asyncio.run(self.check_https())

            return self.status
        else:
            logging.exception("Unknown check method")
            raise Exception("Unknown check method")
