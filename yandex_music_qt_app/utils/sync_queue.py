from yandex_music import ClientAsync


async def _sync_queue(client: ClientAsync):
    queues = await client.queues_list()
    synced_queue = await client.queue(queue_id=queues[0].id)
    return synced_queue
