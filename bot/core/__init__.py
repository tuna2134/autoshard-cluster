import discord
import requests
from websockets import connect

import time
import asyncio


class MyClient(discord.AutoShardedClient):
    
    def __init__(self, *args, **kwargs):
        self.shard_ok = False
        while not self.shard_ok:
            self.shard_ok = self.check_shard(*args, **kwargs)
            if not self.shard_ok:
                time.sleep(5)
    
    def check_shard(self, *args, **kwargs):
        r = requests.get("http://localhost:8080/shards", timeout=5)
        payload = r.json()
        kwargs["shard_count"] = payload["shard_count"]
        if not payload["full"]:
            kwargs["shard_ids"] = [payload["shard_id"]]
            super().__init__(*args, **kwargs)
            return True
        return False

    async def heartbeat(self):
        self.ws = await connect("ws://localhost:8080/heartbeat")
        while True:
            await self.ws.recv()
            await self.ws.send("ping")
            await asyncio.sleep(2)