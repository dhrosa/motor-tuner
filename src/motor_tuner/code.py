import time

import board
from busio import UART

from .modbus.register_bank import RegisterBank
from .modbus.rtu_framer import RtuFramer

TX = board.TX  # type: ignore[attr-defined]
RX = board.RX  # type: ignore[attr-defined]

uart = UART(tx=TX, rx=RX)


def uart_read(size: int) -> bytes:
    return uart.read(size) or bytes()


def uart_write(data: bytes) -> None:
    uart.write(data)


framer = RtuFramer(
    read=uart_read,
    write=uart_write,
)

registers = RegisterBank(framer)

print("")
while True:
    for i in range(0, 100):
        print(f"{i:03d} => {registers[i]}")
        time.sleep(1)
