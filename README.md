# Availability checker daemon

A tool for checking availability of web services

# NB!
This is the alfa version!

# Usage
```python
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
```

# Result
```python
{'status': 'online', 'response_code': 200, 'url': 'https://knst.me:443/pub/', 'method': 'GET', 'content_type': 'text/html', 'content_length': None}
{'status': 'online', 'response_code': 200, 'url': 'http://knst.me:80/', 'method': 'GET', 'content_type': 'text/html', 'content_length': None}
{'status': 'offline', 'response_code': 0, 'url': 'https://knst.me:80/', 'method': '', 'content_type': '', 'content_length': ''}
```

# Requirements
- aiohttp