from cap_array import cap_array


class sar_adc_mcs:
    def __init__(self, Vref=1.0, bits=3, Cu=1e-15):
        self.Vref = Vref
        self.bits = bits
        self.Cu = Cu
        self.cap_arrayP = cap_array()
        self.cap_arrayN = cap_array()
        self.cap_arrayP.addV("vref", self.Vref)
        self.cap_arrayN.addV("vref", self.Vref)
        self.cap_arrayP.addV("vcm", self.Vref / 2)
        self.cap_arrayN.addV("vcm", self.Vref / 2)
        self.cap_arrayP.addC("dummy", self.Cu, "vcm")
        self.cap_arrayN.addC("dummy", self.Cu, "vcm")
        for i in range(self.bits - 1):
            self.cap_arrayP.addC(i, 2 ** i * self.Cu, "vcm")
            self.cap_arrayN.addC(i, 2 ** i * self.Cu, "vcm")

    def convert(self, Vin):
        self.cap_arrayP.resetAll()
        self.cap_arrayN.resetAll()
        VdacP = self.cap_arrayP.sampleTopPlate(Vin / 2)
        VdacN = self.cap_arrayN.sampleTopPlate(-Vin / 2)
        out = 0
        Etot = 0
        for k in range(self.bits - 2, -1, -1):
            if VdacP - VdacN < 0:
                VdacP, EP = self.cap_arrayP.switchC([k, "vref"])
                VdacN, EN = self.cap_arrayN.switchC([k, "gnd"])
            else:
                out = out + 2 ** (k + 1)
                VdacP, EP = self.cap_arrayP.switchC([k, "gnd"])
                VdacN, EN = self.cap_arrayN.switchC([k, "vref"])
            Etot = Etot + EP + EN
        if VdacP - VdacN > 0:
            out = out + 2 ** 0
        return out, Etot
