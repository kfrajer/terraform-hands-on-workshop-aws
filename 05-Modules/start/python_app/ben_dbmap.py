#!/bin/env python3
import re
import sys

from twisted.internet import task

from duo_mysql import dbconn
import duo.dbmap

DATA_TYPES = {
    "customers": "akey",
    "integrations": "ikey",
    "admins": "email",
    "urg_activation": "code",
    "phones": "pkey",
}

async def print_dangling(dbmap):
    all_uuids = dict()
    for table_name in DATA_TYPES:
        all_uuids[table_name] = set(
            row["uuid"]
            for row in await dbmap.map_dbc.rr_query(
                    "SELECT uuid FROM shards_" + table_name))

    for dbc in dbmap.get_all_dbc():
        for table_name, uuids in all_uuids.items():
            uuids.difference_update(await get_shard_uuids(dbc, table_name))
    for table_name, uuids in all_uuids.items():
        sys.stdout.write("Dangling {}: {}\n\n".format(table_name, uuids))

async def get_shard_uuids(dbc, table_name):
    column = DATA_TYPES[table_name]
    return [
        row["uuid"]
        for row in await dbc.rr_query(
                "SELECT {} AS uuid FROM {}".format(column, table_name))]

@task.react
async def main(reactor):
    dbmap = duo.dbmap.DBMap()
    dbmap.startService()
    try:
        await print_dangling(dbmap)
    finally:
        dbmap.stopService()