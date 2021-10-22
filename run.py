# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring

import os

import click

from eventador.consumer import Consumer
from eventador.publisher import Publisher

EVENT_HUB_DSN = os.getenv("EVENT_HUB_DSN")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
BLOB_STORAGE_DSN = os.getenv("BLOB_STORAGE_DSN")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")


@click.group()
def cli():
    pass


@cli.command()
def publish():
    last_event = ""
    with Publisher(EVENT_HUB_DSN, EVENT_HUB_NAME) as publisher:
        while True:
            event = click.prompt("Enter event to send", type=str, default=last_event)

            if not event and last_event:
                event = last_event

            publisher.send(event)
            click.secho(f"Sent {event}", fg="green")
            last_event = event


@cli.command()
def consume():
    with Consumer(
        BLOB_STORAGE_DSN, BLOB_CONTAINER_NAME, EVENT_HUB_DSN, EVENT_HUB_NAME
    ) as consumer:
        consumer.consume()


if __name__ == "__main__":
    cli()
