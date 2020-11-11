"""
Database stuff.
"""

import asyncpg

CONNECTION_PARAMS = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'database': 'postgres',
    'password': 'postgres'
}


async def init():
    async def _init():
        conn = await get_connection()
        await conn.execute("""
            DROP TABLE IF EXISTS documents
        """)
        await conn.execute("""
            CREATE TABLE documents(
                id serial PRIMARY KEY,
                name TEXT,
                recipients TEXT[],
                url TEXT,
                is_signed BOOLEAN
            )
        """)
        await conn.close()

    import asyncio
    asyncio.get_event_loop().run_until_complete(_init())


async def get_connection():
    return await asyncpg.connect(**CONNECTION_PARAMS)
