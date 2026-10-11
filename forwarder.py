import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Веб-сервер для поддержания активности на Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

api_id = 34240068
api_hash = 'e2eb01280a3271091b3d88c5e22d447f'
SESSION_STRING = os.environ.get("SESSION_STRING", "")

SOURCE_CHANNELS = [
    'https://t.me/nighttyped_chbb',
    'https://t.me/nighttyped'
]
TARGET_CHANNEL = 'https://t.me/raytmantyp'

if SESSION_STRING:
    client = TelegramClient(StringSession(SESSION_STRING), api_id, api_hash)
else:
    client = TelegramClient('my_forwarder_session', api_id, api_hash)

grouped_messages = {}

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new_message(event):
    try:
        if event.message.grouped_id:
            gid = event.message.grouped_id
            if gid not in grouped_messages:
                grouped_messages[gid] = [event.message]
                await asyncio.sleep(2)
                await client.forward_messages(TARGET_CHANNEL, grouped_messages[gid])
                print('Альбом успешно переслан!')
                del grouped_messages[gid]
            else:
                grouped_messages[gid].append(event.message)
        else:
            await client.forward_messages(TARGET_CHANNEL, event.message)
            print('Сообщение успешно переслано!')
    except Exception as e:
        print(f'Ошибка при пересылке: {e}')

async def main():
    await client.start()
    print('Бот запущен и готов к работе!')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
