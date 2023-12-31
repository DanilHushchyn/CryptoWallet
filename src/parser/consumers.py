from celery.result import AsyncResult
from propan.brokers.rabbit import RabbitQueue
from propan import RabbitRouter
from src.parser.tasks import parsing


parser_router = RabbitRouter('parser/')

queue_parser = RabbitQueue(name='parse_block')


@parser_router.handle(queue_parser)
async def parser_handle(block):
    result: AsyncResult = parsing.apply_async(args=[block])