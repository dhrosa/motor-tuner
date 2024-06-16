from motor_tuner.modbus.crc import checksum_bytes
from motor_tuner.modbus.rtu_framer import RtuFramer


def test_crc() -> None:
    """Check that the CRC values used in subsequent tests make sense."""
    assert list(checksum_bytes([0, 1, 2])) == [0xF1, 0x91]


def test_read() -> None:
    def read(size: int) -> bytes:
        assert size == 5
        return bytes([0, 1, 2, 0xF1, 0x91])

    framer = RtuFramer(read=read, write=lambda data: None)
    assert list(framer.read_pdu(3)) == [0, 1, 2]


def test_write() -> None:
    def write(data: bytes) -> None:
        assert list(data) == [0, 1, 2, 0xF1, 0x91]

    framer = RtuFramer(read=lambda size: b"", write=write)
    framer.write_pdu(bytes([0, 1, 2]))
