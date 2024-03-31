import aiohttp
import config


async def send_status(sub_id: str, status: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{config.KEITARO_DOMAIN}?subid={sub_id}&status={status}') as response:
                print(await response.text())
    except Exception as e:
        print(str(e))
