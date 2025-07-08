import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from info import FSUB_DB_URL, DATABASE_NAME, AUTH_CHANNEL, LOG_CHANNEL

client = AsyncIOMotorClient(FSUB_DB_URL)
mydb = client[DATABASE_NAME]

class FsubDatabase:
    def __init__(self):
        self.misc = mydb.misc
        self.req = mydb.requests

    async def set_rfsub_id(self, rfsub_id, limit=None):
        data = {'_id': 'rfsub_id', 'rfsub_id': rfsub_id, 'join_count': 0}
        if limit is not None:
            data['limit'] = int(limit)
        await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': data}, upsert=True)

    async def get_rfsub_id(self):
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        return doc.get('rfsub_id', AUTH_CHANNEL) if doc else AUTH_CHANNEL

    async def remove_rfsub_id(self):
        await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': {'rfsub_id': AUTH_CHANNEL, 'limit': None, 'join_count': 0}}, upsert=True)

    async def find_join_req(self, id):
        return bool(await self.req.find_one({'id': id}))

    async def add_join_req(self, id):
        # Check for duplicate join request
        if await self.find_join_req(id):
            return await self.get_join_count()  # Return current count without incrementing
        await self.req.insert_one({'id': id})
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        if doc and 'join_count' in doc:
            new_count = doc['join_count'] + 1
            await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': {'join_count': new_count}})
            # Log the current state
            limit = doc.get('limit', None)
            await mydb.client[LOG_CHANNEL].insert_one({
                'type': 'join_req',
                'user_id': id,
                'join_count': new_count,
                'limit': limit,
                'timestamp': datetime.datetime.now()
            })
            return new_count
        # Initialize join_count if document is missing
        await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': {'join_count': 1}}, upsert=True)
        await mydb.client[LOG_CHANNEL].insert_one({
            'type': 'join_req',
            'user_id': id,
            'join_count': 1,
            'limit': await self.get_rfsub_limit(),
            'timestamp': datetime.datetime.now()
        })
        return 1

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
            join_count = doc.get('join_count', 0)
            limit = doc['limit']
            # Log the check
            await mydb.client[LOG_CHANNEL].insert_one({
                'type': 'check_rfsub_limit',
                'join_count': join_count,
                'limit': limit,
                'timestamp': datetime.datetime.now()
            })
            if join_count >= limit:
                await self.remove_rfsub_id()
                return True
        return False

fsub_db = FsubDatabase()
