from .crc import checksum_bytes
from .framer import Framer

try:
    from collections.abc import Callable
except ImportError:
    pass


class ChecksumError(ValueError):
    pass


class RtuFramer(Framer):
    """Frames Modbus messages for UART transfer.

    Incoming messages verify that the payload has the correct checksum. Outgoing
    messages append the checksum to the paload.
    """

    def __init__(
        self, read: Callable[[int], bytes], write: Callable[[bytes], None]
    ) -> None:
        self.read = read
        self.write = write

    def read_pdu(self, size: int) -> bytes:
        frame = self.read(size + 2)
        payload = frame[:-2]
        reported_checksum = frame[-2:]
        if (actual_checksum := checksum_bytes(payload)) != reported_checksum:
            raise ChecksumError(
                f"Reported checksum is {reported_checksum.hex()}, "
                f"actual checksum is {actual_checksum.hex()}"
            )
        return payload

    def write_pdu(self, data: bytes) -> None:
        self.write(data + checksum_bytes(data))
