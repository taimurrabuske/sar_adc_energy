# coding=utf-8

class cap_array:
    def __init__(self):
        self.ct = 0
        self.cb = 0
        self.c = dict([])
        self.v = dict([])
        # Add ground node
        self.v["gnd"] = {"value": 0, "energy": 0}
        self.prev_vout = 0
        self.vout = 0

    # Add a capacitor to the array
    def addC(self, name, value, initial="gnd"):
        self.c[name] = {"value": value, "node": initial, "initial": initial}
        return 0

    # Add a voltage source (reference) to the array.
    def addV(self, name, value, energy=0):
        self.v[name] = {"value": value, "energy": energy}

    # Reset all bottom plates to their initial conditions
    def resetAll(self):
        for cap in self.c:
            self.c[cap]["node"] = self.c[cap]["initial"]

    # Sample a voltage into the top plate
    def sampleTopPlate(self, vin):
        self.vout = vin
        return self.vout


    # Process the charge. The input of this function is a pair of values in the form [C,N], where C is the name of the capacitor to be switched, and N is the node to which it is switched, e.g. Vref or gnd. The method returns the DAC voltage and energy spent in the current cycle.
    def switchC(self, *args):
        # Store previous voltage to the prev_node key in the dictionary.
        for i in self.c:
            self.c[i]["prev_node"] = self.c[i]["node"]
        # Connect capacitances to assigned nodes
        for i in args:
            cap = i[0]
            v = i[1]
            if v not in self.v:
                print("Voltage source does not exist")
            self.c[cap]["node"] = v

        #        Compute the new voltage in the DAC, given by:
        #          x
        #         ___
        #         ╲
        #          ╲   (V_DAC0⋅C0(i) + C(i)⋅V_ref(i) - C0(i)⋅V_ref0(i))
        #          ╱
        #         ╱
        #         ‾‾‾
        #        i = 0
        # V_DAC= ──────────────────────────────────────────────────────
        #                                x
        #                               ___
        #                               ╲
        #                                ╲   C(i)
        #                                ╱
        #                               ╱
        #                               ‾‾‾
        #                              i = 0
        tmp = 0
        # compute the summation in the numerator
        for i in self.c:
            tmp = tmp + self.c[i]["value"] * (
                        self.v[self.c[i]["node"]]["value"] - self.v[self.c[i]["prev_node"]]["value"] + self.vout)
        # compute denominator
        c_total = sum([self.c[j]["value"] for j in self.c])
        # store previous dac voltage
        self.prev_vout = self.vout
        # set output voltage
        self.vout = tmp / c_total

        # Calculate the energy spent in charging the DAC
        E = dict([])
        E_total = 0
        # Enumerate all the capacitors connected to each one of the voltage sources, and calculate all the parameters for each one of them.
        for vs in self.v:
            # c_just_connected is an array with all the capacitors that were connected on the actual clock cycle
            c_just_connected = []
            # c_still is the capacitance that was already connected on previous cycle
            c_still = []
            # find C_just_connected and c_still
            for cap in self.c:
                if self.c[cap]["node"] == vs:
                    if self.c[cap]["prev_node"] == vs:
                        c_still.append(self.c[cap])
                    else:
                        c_just_connected.append(self.c[cap])
            c_still_sum = sum([k["value"] for k in c_still])
            # E_still is the energy required to move the already connected capacitors from V_dac0 to V_dac
            E_still = self.v[vs]["value"] * c_still_sum * (self.prev_vout - (self.vout))
            # E_just_connected is the energy required to charge the bottom plate of the just connected capacitor from the previous voltage (e.g. ground) to the reference voltage.
            E_just_connected = 0
            for j in c_just_connected:
                E_just_connected = E_just_connected - self.v[vs]["value"] * j["value"] * (
                            self.vout - self.v[vs]["value"] - (self.prev_vout - self.v[j["prev_node"]]["value"]))
            E[vs] = E_just_connected + E_still
            # E_total is the total energy drained from all the reference sources.
            E_total = E_total + E[vs]
            self.v[vs]["energy"] = self.v[vs]["energy"] + E[vs]
        return self.vout, E_total
