import aiosqlite

DB_NAME = "posts.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            message_id INTEGER,
            text TEXT
        )
        """)
        await db.commit()

async def save_post(message_id: int, text: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO posts (message_id, text) VALUES (?, ?)",
            (message_id, text)
        )
        await db.commit()

async def search_posts(query: str):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT message_id FROM posts WHERE text LIKE ?",
            (f"%{query}%",)
        )
        return await cursor.fetchall()
