import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from info import FSUB_DB_URL, DATABASE_NAME, AUTH_CHANNEL

client = AsyncIOMotorClient(FSUB_DB_URL)
mydb = client[DATABASE_NAME]

class FsubDatabase:
    def __init__(self):
        self.misc = mydb.misc
        self.req = mydb.requests
        # Ensure unique index on 'id' field to prevent duplicate user IDs
        self.req.create_index("id", unique=True)

    async def set_rfsub_id(self, rfsub_id, limit=None):
        """Set global rfsub_id and optional limit."""
        data = {'_id': 'rfsub_id', 'rfsub_id': rfsub_id}
        if limit is not None:
            data['limit'] = int(limit)
            data['join_count'] = 0
        await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': data}, upsert=True)

    async def get_rfsub_id(self):
        """Get global rfsub_id, return AUTH_CHANNEL if not set."""
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        return doc.get('rfsub_id', AUTH_CHANNEL) if doc else AUTH_CHANNEL

    async def remove_rfsub_id(self):
        """Remove global rfsub_id, resetting to AUTH_CHANNEL."""
        await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': {'rfsub_id': AUTH_CHANNEL, 'limit': None, 'join_count': 0}}, upsert=True)

    async def find_join_req(self, id, username=None):
        """Check if user has a join request by id and optionally username."""
        query = {'id': id}
        if username:  # Only include username in query if provided
            query['username'] = username
        return bool(await self.req.find_one(query, {'_id': 0}))

    async def add_join_req(self, id, username=None):
        """Add user to join requests and increment join count only if new."""
        # Check if user already exists
        if await self.find_join_req(id, username):
            return await self.get_join_count()  # Return current count if user exists

        # Insert new document with id and optional username
        try:
            doc = {'id': id}
            if username:  # Only include username if provided
                doc['username'] = username
            await self.req.insert_one(doc)
            # Increment join_count
            doc = await self.misc.find_one({'_id': 'rfsub_id'})
            if doc and 'join_count' in doc:
                new_count = doc['join_count'] + 1
                await self.misc.update_one({'_id': 'rfsub_id'}, {'$set': {'join_count': new_count}})
                return new_count
            return 0
        except DuplicateKeyError:
            return await self.get_join_count()  # Handle duplicate id

    async def del_join_req(self):
        """Delete all join requests."""
        await self.req.drop()

    async def get_rfsub_limit(self):
        """Get the current join request limit."""
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        return doc.get('limit', None) if doc else None

    async def get_join_count(self):
        """Get the current join request count."""
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        return doc.get('join_count', 0) if doc else 0

    async def check_rfsub_limit(self):
        """Check if join request limit is reached, reset if necessary."""
        doc = await self.misc.find_one({'_id': 'rfsub_id'})
        if doc and 'limit' in doc and doc['limit'] is not None:
            if doc['join_count'] >= doc['limit']:
                await self.remove_rfsub_id()
                return True
        return False

    async def clean_duplicate_users(self):
        """Remove duplicate user IDs, keeping the most recent document."""
        async for doc in self.req.find({}).sort([('_id', -1)]):  # Sort by _id (newest first)
            user_id = doc['id']
            # Check for duplicates
            duplicates = await self.req.find({'id': user_id}).to_list(None)
            if len(duplicates) > 1:
                # Keep the most recent document (first in sorted list)
                for dup in duplicates[1:]:
                    await self.req.delete_one({'_id': dup['_id']})

fsub_db = FsubDatabase()
