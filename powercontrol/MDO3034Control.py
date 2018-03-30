import numpy as np
from struct import unpack
import pylab
import re

try:
    import visa
except ImportError as err:
    print(err)
    exit()

class MDO3034C:
    def __init__(self, resource_name):
        instlist=visa.ResourceManager()
        #print(instlist.list_resources())
        self.my_resource=instlist.open_resource(resource_name)

    def testIO(self):
        message=self.my_resource.ask('*IDN?')
        print("ocsilloscope information:" + repr(message))
		
    def readSet(self,ch):
        self.my_resource.write(":DATA:SOU "+ ch)
        self.my_resource.write(':DATA:START 1')
        self.my_resource.write(':DATA:STOP 10000')
        self.my_resource.write(':WFMOutpre:ENCdg BINARY')
        self.my_resource.write(":WFMOutpre:BYT_Nr 1")
        self.my_resource.write(":HEADer 0")
        self.my_resource.write(":WFMOutpre?")
		
    def readOffset(self):
        ymult = float(self.my_resource.ask('WFMPRE:YMULT?'))
        yzero = float(self.my_resource.ask('WFMPRE:YZERO?'))
        #yoff = float(self.my_resource.ask('WFMPRE:YOFF?'))
        xincr = float(self.my_resource.ask('WFMPRE:XINCR?'))
        xzero = float(self.my_resource.ask('WFMPRE:XZERO?'))
        return ymult,yzero,xincr,xzero

    def readWave(self):
        ymult,yzero,xincr,xzero=self.readOffset()

        self.my_resource.write("CURVE?")
        data=np.array(self.my_resource.read_raw())
        #headerlen=2+int(data[1])
        #header=data[:headerlen]
        #ADC_wave=data[headerlen:-1]
        #ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
        Volts = data * ymult  + yzero
        Time = np.arange(xzero, xzero + xincr * data.size, xincr)
        #Time=Time*1e9 #ns
        #Volts=Volts*1e3 #mV

        return Time, Volts

    def plotWave(self, Time, Volts):
        pylab.plot(Time, Volts)
        pylab.show()

  
if __name__=="__main__":
    rm = visa.ResourceManager()
    print(rm.list_resources())
    list_sources = rm.list_resources()
    for str in list_sources:
        match_result = re.match(r'TCPIP',str)
        if match_result:
            tcpip_resource = str
            print("the TCPIP resource is:" + repr(tcpip_resource))
            break
        else:
            print("no TCPIP resource,please check it!")
            exit()
    scope=MDO3034C(tcpip_resource)
    scope.testIO()
    scope.readSet("CH1")
    
    Time,Volts = scope.readWave()
    scope.plotWave(Time, Volts)
    print(max(Volts)-min(Volts))
