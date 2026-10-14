import asyncio
import asyncpg
import aiohttp
import os
from dotenv import load_dotenv
from itertools import batched

load_dotenv()

URL = 'https://swapi-node.vercel.app'
MAX_REQUESTS = 5

async def get_person(session, person_id):
    url = f'{URL}/api/people/{person_id}'
    async with session.get(url) as response:
        data_person = await response.json()
        if not data_person or 'fields' not in data_person:
            print(f' ID {person_id}: ответ = {data_person}')
            return None
        return data_person['fields']

async def get_all(session):
    all_people = []
    for ids_chunk in batched(range(1, 83), MAX_REQUESTS): #ids_chunk(там у нас 10 переменных за раз)
        coros = [get_person(session, i) for i in ids_chunk] #по этим 10 переменным мы итерируемся и вызываем метод get_person для каждой
        batch = await asyncio.gather(*coros) #запускаем эти 10 корутин и собираем результаты в batch параллельно
        all_people.extend([p for p in batch if p is not None]) #добавляем их в список
    # tasks = [fetch_person(session, i) for i in range(1,83)]
    # people = await asyncio.gather(*tasks)
    return all_people

async def get_name_from_url(session, path):
    url = f'{URL}{path}'
    async with session.get(url) as response:
        data = await response.json()
        if not data or 'fields' not in data or 'name' not in data['fields']:
            print(f' Нет name для {path}: {data}')
            return None
        fields = data['fields']['name']
        return fields.get('name') or fields.get('starship_class')
    
async def get_all_names_from_url(session, paths):
    if not paths:
        return ''
    names_from_urls = [get_name_from_url(session, path) for path in paths]
    names = await asyncio.gather(*names_from_urls)
    return ', '.join(names)

async def clean_dict(session, person):
    person_id = int(person['url'].split('/')[-1])
    return {
        'id': person_id,
        'name': person['name'],
        'birth_year': person['birth_year'],
        'eye_color': person['eye_color'],
        'gender': person['gender'],
        'hair_color': person['hair_color'],
        'height': person['height'],
        'mass': person['mass'],
        'skin_color': person['skin_color'],
        'homeworld': await get_all_names_from_url(session, [person['homeworld']]),
        'films': await get_all_names_from_url(session, person['films']),
        'species': await get_all_names_from_url(session, person['species']),
        'starships': await get_all_names_from_url(session, person['starships']),
        'vehicles': await get_all_names_from_url(session, person['vehicles']),
        'url': person['url'],
    }





    

