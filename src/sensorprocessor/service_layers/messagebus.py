from typing import Union, List

import logging

from sensorprocessor.domain import commands, events
from sensorprocessor.service_layers import handlers, unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]

def handle(message: Message, uow: unit_of_work.AbstractUnitOfWork):
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, commands.Command):
            handle_command(message, queue, uow)
        elif isinstance(message, events.Event):
            handle_event(message, queue, uow)
        else:
            raise Exception(f"{message} was not an event")


def handle_command(
        cmd: commands.Command, 
        queue: List[Message], 
        uow: unit_of_work.AbstractUnitOfWork
        ):
    logger.debug(f"Handling command {cmd}")
    try:
        handler = COMMAND_HANDLERS[type(cmd)] 
        handler(cmd, uow)
        queue.extend(uow.collect_new_events())
    except Exception:
        logger.debug(f"Exception handling command {cmd}")
        raise 


def handle_event(
        event: events.Event, 
        queue: List[Message],
        uow: unit_of_work.AbstractUnitOfWork
        ):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            handler(event, uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.debug(f"Exception handling event {event}")
            continue


COMMAND_HANDLERS = {
        commands.CreateRawData: handlers.create_rawdata
        }

EVENT_HANDLERS = {
        events.RawDataCreated: []
        }
