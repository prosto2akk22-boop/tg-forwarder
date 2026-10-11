import asyncio
from telethon import TelegramClient, events

api_id = 34240068
api_hash = 'e2eb01280a3271091b3d88c5e22d447f'

SOURCE_CHANNELS = [
    'https://t.me/nighttyped_chbb',
    'https://t.me/nighttyped'
]
TARGET_CHANNEL = 'https://t.me/raytmantyp'

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
    await client.connect()
    print('Бот запущен и готов к работе!')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
