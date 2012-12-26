class SymbolTable:
    def __init__(self):
        self.symbols = {
                'SP'    : 0x0000,
                'LCL'   : 0x0001,
                'ARG'   : 0x0002,
                'THIS'  : 0x0003,
                'THAT'  : 0x0004,
                'SCREEN': 0x4000,
                'KBD'   : 0x6000,
                }

        for i in range(16):
            self.symbols['R%d' % i] = i

    def addEntry(self, symbol, address):
        self.symbols[symbol] = address

    def contains(self, symbol):
        return symbol in self.symbols

    def GetAddress(self, symbol):
        return self.symbols[symbol]

