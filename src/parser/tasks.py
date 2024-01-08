import asyncio

from dependency_injector.wiring import inject, Provide

from config_celery.celery import celery_app
from src.parser.containers import ParserContainer
from src.parser.services.block_parser import ParserService


@celery_app.task(name="parsing")
@inject
def parsing(block, parser_service: ParserService = Provide[ParserContainer.parser_service]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser_service.parse_block(block))
    return "Async task completed"

