import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from info import FSUB_DB_URL, DATABASE_NAME, AUTH_CHANNEL

client = AsyncIOMotorClient(FSUB_DB_URL)
mydb = client[DATABASE_NAME]

class FsubDatabase:
    def __init__(self):
        self.misc = mydb.misc
        self.req = mydb.requests

    async def set_rfsub_id(self, rfsub_id, limit=None):
        data = {'_id': 'rfsub_id', 'rfsub_id': rfsub_id}
        if limit is not None:
            data['limit'] = int(limit)
            data['join_count'] = 0
        await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': data}, upsert=True)

    async def get_rfsub_id(self):
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        return doc.get('rfsub_id', AUTH_CHANNEL) if doc else AUTH_CHANNEL

    async def remove_rfsub_id(self):
        await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': {'rfsub_id': AUTH_CHANNEL, 'limit': None, 'join_count': 0}}, upsert=True)

    async def find_join_req(self, id):
        return bool(await self.req.find_one({'id': id}))

    async def add_join_req(self, id):
        await self.req.insert_one({'id': id})
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        if doc and 'join_count' in doc:
            new_count = doc['join_count'] + 1
            await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': {'join_count': new_count}})
            return new_count
        return 0

    async def del_join_req(self):
        await self.req.drop()

    async def get_rfsub_limit(self):
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        return doc.get('limit', None) if doc else None

    async def get_join_count(self):
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        return doc.get('join_count', 0) if doc else 0

    async def check_rfsub_limit(self):
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        if doc and 'limit' in doc and doc['limit'] is not None:
            if doc['join_count'] >= doc['limit']:
                await self.remove_rfsub_id()
                return True
        return False


fsub_db = FsubDatabase()
