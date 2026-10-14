import asyncio
import aiohttp
from itertools import batched
from load_data import get_all, clean_dict, MAX_REQUESTS
from db import save_people, init_orm



async def main():
    await init_orm()

    async with aiohttp.ClientSession() as session:
        people = await get_all(session)
        print(f'Количество людей: {len(people)}')
        clean_people =[]
        for ids_chunk in batched(people, MAX_REQUESTS):
            coros = [clean_dict(session, person) for person in ids_chunk]
            batch = await asyncio.gather(*coros)
            clean_people.extend(batch)

    await save_people(clean_people)     


if __name__ == '__main__':
    asyncio.run(main())