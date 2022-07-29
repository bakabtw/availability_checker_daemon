import asyncio
import os
from pony import orm
import time
from availability_checker.checker import AvailabilityChecker

# Time between checks in seconds
SLEEP_TIMER = 60

if os.getenv('DEBUG'):
    import logging

    orm.set_sql_debug(True)
    logging.basicConfig(level=logging.INFO)

db = orm.Database()
db.bind(provider='sqlite', filename='hosts_sqlite.db', create_db=True)


class Hosts(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    description = orm.Required(str)
    server = orm.Required(str)
    port = orm.Required(int)
    method = orm.Required(str)
    path = orm.Required(str)
    created = orm.Required(int)
    updated = orm.Required(int)


class Statuses(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    status = orm.Required(str)
    response_code = orm.Required(int)
    url = orm.Required(str)
    method = orm.Optional(str)
    content_type = orm.Optional(str)
    content_length = orm.Optional(int)
    server_id = orm.Required(int)
    timestamp = orm.Required(int)


@orm.db_session
def get_hosts():
    output = []
    hosts = Hosts.select()

    for host in hosts:
        output.append(
            {
                'id': host.id,
                'description': host.description,
                'server': host.server,
                'port': host.port,
                'method': host.method,
                'path': host.path
            }
        )

    return output


@orm.db_session
async def write_status(response, server_id):
    status = Statuses(
        status=response['status'],
        response_code=response['response_code'],
        url=response['url'],
        method=response['method'],
        content_type=response['content_type'],
        content_length=response['content_length'],
        server_id=server_id,
        timestamp=int(time.time())
        )

    return db.commit()


async def main():
    db.generate_mapping(create_tables=True)

    while True:
        for host in get_hosts():
            checker = await AvailabilityChecker(host).check()
            await write_status(checker, host['id'])

        await asyncio.sleep(SLEEP_TIMER)


if __name__ == '__main__':
    asyncio.run(main())
