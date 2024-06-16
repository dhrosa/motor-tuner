class Framer:
    """Translates Modbus protocol data units (PDUs) to application data units (ADUs)."""

    def read_pdu(self, size: int) -> bytes:
        raise NotImplementedError

    def write_pdu(self, data: bytes) -> None:
        raise NotImplementedError
