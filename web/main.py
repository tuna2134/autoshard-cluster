from sanic import Sanic, response

import asyncio
import random


app = Sanic(__name__)
shard_count = 5
NOWSHARD = 0
SHARDS = [i for i in range(0, shard_count)]


@app.get("/shards")
async def get_shards(request):
    payload = {
        "shard_count": shard_count
    }
    if len(SHARDS) == 0:
        full = True
    else:
        shard = random.choice(SHARDS)
        SHARDS.remove(shard)
        payload["shard_id"] = shard
        print(f"Shard {shard} is now in use.")
        full = False
    payload["full"] = full
    return response.json(payload)

@app.websocket("/heartbeat")
async def heartbeat(request, ws):
    global NOWSHARD
    NOWSHARD += 1
    while True:
        try:
            await ws.send("ping")
            await asyncio.wait_for(ws.recv(), timeout=5)
        except Exception: # noqa
            NOWSHARD -= 1


if __name__ == "__main__":
    app.run(host="localhost", port=8080)