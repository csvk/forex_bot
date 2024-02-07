class Instrument:

    def __init__(self, name, ins_type, displayName,
                    pipLocation, tradeUnitsPrecision, minimumTradeSize, marginRate):
        self.name = name
        self.ins_type = ins_type
        self.displayName = displayName
        self.pipLocation = pow(10, pipLocation)
        self.tradeUnitsPrecision = tradeUnitsPrecision
        self.minimumTradeSize = minimumTradeSize
        self.marginRate = float(marginRate)

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def FromApiObject(cls, ob):
        return Instrument(
            ob['name'],
            ob['type'],
            ob['displayName'],
            ob['pipLocation'],
            ob['tradeUnitsPrecision'],
            ob['minimumTradeSize'],
            ob['marginRate']
        )