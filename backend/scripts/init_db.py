#!/usr/bin/env python3
"""Bootstrap local SQLite development database."""
import asyncio

from app.core.db import init_db


async def main():
    print("Initializing DClaw Video development database...")
    await init_db()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
