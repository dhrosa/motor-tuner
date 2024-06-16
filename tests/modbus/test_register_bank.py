from dataclasses import dataclass

from pytest import fixture, raises

from motor_tuner.modbus.framer import Framer
from motor_tuner.modbus.register_bank import RegisterBank


@dataclass
class PduEvent:
    payload: bytes


@dataclass
class PduRead(PduEvent):
    pass


@dataclass
class PduWrite(PduEvent):
    pass


class FakeFramer(Framer):
    def __init__(self) -> None:
        self.events = list[PduEvent]()
        """Ordered list of expected requests and responses."""

    def read_pdu(self, size: int) -> bytes:
        event = self.events.pop(0)
        assert isinstance(event, PduRead)
        return event.payload

    def write_pdu(self, data: bytes) -> None:
        event = self.events.pop(0)
        assert isinstance(event, PduWrite)
        assert list(data) == list(event.payload)


@fixture
def framer() -> FakeFramer:
    return FakeFramer()


@fixture
def events(framer: FakeFramer) -> list[PduEvent]:
    """Fixture for mutable sequence of expected PDU requests and responses."""
    return framer.events


@fixture
def registers(framer: FakeFramer) -> RegisterBank:
    return RegisterBank(framer)


def test_read(registers: RegisterBank, events: list[PduEvent]) -> None:
    events[:] = [
        PduWrite(bytes([63, 3, 0, 7, 0, 1])),
        PduRead(bytes([63, 3, 2, 1, 1])),
    ]
    assert registers[7] == 257


def test_write_success(registers: RegisterBank, events: list[PduEvent]) -> None:
    events[:] = [
        PduWrite(bytes([63, 6, 0, 7, 1, 1])),
        PduRead(bytes([63, 6, 0, 7, 1, 1])),
    ]
    registers[7] = 257


def test_write_response_mismatch(
    registers: RegisterBank, events: list[PduEvent]
) -> None:
    events[:] = [
        PduWrite(bytes([63, 6, 0, 7, 1, 1])),
        PduRead(bytes([63, 6, 0, 7, 1, 2])),
    ]
    with raises(ValueError):
        registers[7] = 257
