

class sar_adc_cs:
    def __init__(self,Vref=1.0,bits=3,Cu=1e-15):
        self.Vref=Vref
        self.bits=bits
        self.Cu=Cu
        self.Cth=2**(bits-1)*Cu
        self.c=[]
        for i in range(self.bits-1):
            self.c.append(2**i*self.Cu)
    def convert(self,Vin,return_dac=0):
        out=0
        Qth=self.Cth*Vin
        Qtotal=Qth
        Ctotal=self.Cth
        Vdac=Vin
        Etot=sum(self.c)*(self.Vref)**2
        for k in range(self.bits-2,-1,-1):
            if Vdac>0:
                out=out+2**(k+1)
                Qtotal=Qtotal-self.c[k]*self.Vref
                Ctotal=Ctotal+self.c[k]
            else:
                Qtotal=Qtotal+self.c[k]*self.Vref
                Ctotal=Ctotal+self.c[k]
            Vdac=Qtotal/Ctotal
        if Vdac>0:
            out=out+2**0
        return out,Etot


        

