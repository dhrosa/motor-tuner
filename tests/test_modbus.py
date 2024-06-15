from dataclasses import dataclass
from typing import TypeAlias

from motor_tuner.modbus import Client, Framer


@dataclass
class PduRead:
    payload: bytes


@dataclass
class PduWrite:
    payload: bytes


PduEvent: TypeAlias = PduRead | PduWrite


class FakeFramer(Framer):
    def __init__(self) -> None:
        self.events = list[PduEvent]()

    def read_pdu(self, size: int) -> bytes:
        event = self.events.pop(0)
        assert isinstance(event, PduRead)
        return event.payload

    def write_pdu(self, data: bytes) -> None:
        event = self.events.pop(0)
        assert isinstance(event, PduWrite)
        assert list(data) == list(event.payload)


def test_read() -> None:
    framer = FakeFramer()
    framer.events = [
        PduWrite(bytes([63, 3, 0, 7, 0, 1])),
        PduRead(bytes([63, 3, 2, 1, 1])),
    ]
    client = Client(framer)

    assert client[7] == 257


def test_write_success() -> None:
    framer = FakeFramer()
    framer.events = [
        PduWrite(bytes([63, 6, 0, 7, 1, 1])),
        PduRead(bytes([63, 6, 0, 7, 1, 1])),
    ]
    client = Client(framer)
    client[7] = 257
