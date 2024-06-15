import struct


class Framer:
    def read_pdu(self, size: int) -> bytes:
        return b""

    def write_pdu(self, data: bytes) -> None:
        return


class Client:
    def __init__(self, framer: Framer) -> None:
        self.framer = framer

    def __getitem__(self, key: int) -> int:
        read_command = struct.pack(
            ">BBHH",
            # Address
            63,
            # Read holding registers
            3,
            # Offset
            key,
            # Count
            1,
        )
        self.framer.write_pdu(read_command)
        response_format = ">BBBH"
        response = self.framer.read_pdu(struct.calcsize(response_format))
        address, function, byte_count, value = struct.unpack(response_format, response)
        return value  # type: ignore

    def __setitem__(self, key: int, value: int) -> None:
        write_command = struct.pack(
            ">BBHH",
            # Address
            63,
            # Write holding register
            6,
            # Offset
            key,
            # Value
            value,
        )
        self.framer.write_pdu(write_command)
        response = self.framer.read_pdu(len(write_command))
        if response == write_command:
            return
        raise ValueError(
            f"Expected response: {list(write_command)} Actual response: {list(response)}"
        )
