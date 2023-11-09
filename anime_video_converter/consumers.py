import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        active_connections = cache.get('active_connections', 0)
        cache.set('active_connections', active_connections + 1)
        await self.channel_layer.group_add(
        'flask_group',
        self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Decrement the counter for active connections
        active_connections = cache.get('active_connections', 1)
        # Ensure we don't go into negative numbers
        cache.set('active_connections', max(active_connections - 1, 0))
        await self.channel_layer.group_discard(
            'flask_group',
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)
        message_type = text_data_json.get('type')

        if message_type == 'progress':
            # Call the method to handle progress update
            progress = text_data_json.get('progress')
            cache_key = text_data_json.get('video_id')
            # print(f"Cache key from consumer: {cache_key}")
            total_size = text_data_json.get('total_size')
            download_url = text_data_json.get('download_url')
            await self.handle_progress_update(progress, cache_key, total_size, download_url)

    async def handle_progress_update(self, progress, cache_key, total_size, download_url):
        # Update variable or model instance here
        # print(f"Received progress: {progress}")
        cache.set(f"{cache_key}", progress)
        cache.set(f"{cache_key}_total", total_size)
        cache.set(f"{cache_key}_status", "processing")
        cache.set(f"{cache_key}_download_url", download_url)

        if (progress / total_size == 1):
            cache.set(f"{cache_key}_status", "converted")

    async def send_data_to_client(self, data):
        # Send data to the Flask client
        print("Sending data to client")
        await self.send(text_data=json.dumps(data))
        print("Data sent to client")
