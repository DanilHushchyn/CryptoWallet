import asyncio
import socketio
from dependency_injector.wiring import inject, Provide
from socketio import AsyncAioPikaManager, AsyncServer
from config.settings import ALLOWED_HOSTS, RABBITMQ_URL
from src.web3.containers import Web3Container
from src.web3.web3_service import WebService
from src.delivery.containers import DeliveryContainer
from src.delivery.services.delivery import DeliveryService

import redis.asyncio as redis

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


async def add_active_user(sid, user_id, room):
    user_data = {'user_id': user_id, 'room': room}
    await redis_client.hmset(f'active_users:{sid}', user_data)


async def get_active_user(sid):
    user_data = await redis_client.hgetall(f'active_users:{sid}')
    if user_data:
        return user_data
    else:
        return None


async def remove_active_user(sid):
    await redis_client.delete(f'active_users:{sid}')


# Function to add a user to a room in Redis
async def add_user_to_room(room, user_id):
    # await redis_client.sadd(f'room:{room}:users', username)
    print(user_id)
    print(1)

    await redis_client.lpush(f'room:{room}:persons', user_id)


# Function to remove a user from a room in Redis
async def remove_user_from_room(room: str, user_id: str):
    # await redis_client.srem(f'room:{room}:users', username)

    await redis_client.lrem(f'room:{room}:persons', 1, user_id)


# Function to get the list of users in a room from Redis
async def get_users_in_room(room):
    # return await redis_client.smembers(f'room:{room}:users')
    lll = await redis_client.lrange(f'room:{room}:persons', 0, -1)
    print(lll)
    return lll


mgr: AsyncAioPikaManager = socketio.AsyncAioPikaManager(RABBITMQ_URL)
sio: AsyncServer = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins='*', namespaces=['*'],
                                        client_manager=mgr)

room_clients = set()


# Функция для отправки сообщения всем участникам комнаты
async def send_message(room, message):
    await sio.emit('message', message, room=room)


async def joined_chat(room, message):
    await sio.emit('message', message, room=room)


# Обработчик подключения клиента к серверу
@sio.event
async def connect(sid, environ):
    print(f'Client connected: {sid}')


@sio.on('join')
async def join_room(sid, data):
    # username = data['username']
    print(data)
    user_id = data['user_id']
    room = data['room']
    await add_active_user(sid, user_id, room)
    await sio.enter_room(sid, room)
    await add_user_to_room(room, user_id)
    room_user_list = await get_users_in_room(room)
    await sio.save_session(sid, session=f'user_id: {room}')
    if room == 'chat':
        await sio.emit('joined_user', {'room': room, 'users': list(room_user_list)}, room=room)


@sio.event
async def disconnect(sid):
    print('x')
    active_users = await get_active_user(sid)
    if active_users is not None:
        room = active_users.get('room')
        user_id = active_users.get('user_id')
        await remove_active_user(sid)
        await remove_user_from_room(user_id, user_id)
        await remove_user_from_room('chat', user_id)

        await sio.emit('disconnect_user', {'room': 'chat', 'user': user_id}, room='chat')
        await sio.leave_room(sid, 'chat')
        await sio.leave_room(sid, user_id)
    room_user_list = await get_users_in_room('chat')
    await sio.emit('joined_user', {'room': 'chat', 'users': list(room_user_list)}, room='chat')


