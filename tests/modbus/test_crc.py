from collections.abc import Iterable

from motor_tuner.modbus.crc import checksum_bytes


def checksum_hex(data: Iterable[int]) -> str:
    return checksum_bytes(data).hex(" ")


def test_crc() -> None:
    assert checksum_hex([0]) == "bf 40"
    assert checksum_hex([1]) == "7e 80"
    assert checksum_hex([0, 1]) == "c0 70"
    assert checksum_hex([0, 1, 2, 3, 4]) == "85 0f"
