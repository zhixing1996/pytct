import numpy as np
from struct import unpack
import pylab
import re
import time

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

    def write_command(self,command):
        self.my_resource.write(command)
        time.sleep(0.5)
    def testIO(self):
        #self.my_resource.write('*RST')
        self.my_resource.write('*CLS')
        #self.my_resource.query_delay = 10.0
        message=self.my_resource.query('*IDN?')
        time.sleep(1)
        print("ocsilloscope information:" + message)
		
    def readSet(self,ch,point_number):
        self.my_resource.write(":DATA:SOU "+ ch)
        self.my_resource.write(':DATA:START 1')
        self.my_resource.write(':DATA:STOP ' + point_number)
        self.my_resource.write(':WFMOutpre:ENCdg BINARY')
        self.my_resource.write(":WFMOutpre:BYT_Nr 1")
        self.my_resource.write(":HEADer 0")
        self.my_resource.write(":WFMOutpre?")
		
    def readOffset(self):
        self.my_resource.write('WFMPRE:YMULT?')
        time.sleep(1)
        ymult = float(self.my_resource.read_raw())
        print("ymult = " + repr(ymult) + '\n')
        self.my_resource.write('WFMPRE:YZERO?')
        time.sleep(1)
        yzero = float(self.my_resource.read_raw())
        print("yzero = " + repr(yzero) + '\n')
        self.my_resource.write('WFMPRE:YOFF?')
        time.sleep(0.5)
        yoff = float(self.my_resource.read_raw())
        print("yoff = " + repr(yoff) + '\n')
        self.my_resource.write('WFMPRE:XINCR?')
        time.sleep(1)
        xincr = float(self.my_resource.read_raw())
        print("xincr = " + repr(xincr) + '\n')
        self.my_resource.write('WFMPRE:XZERO?')
        time.sleep(1)
        xzero = float(self.my_resource.read_raw())
        print("xzero = " + repr(xzero) + '\n')
        return ymult,yzero,yoff,xincr,xzero

    def readWave(self):
        ymult,yzero,yoff,xincr,xzero=self.readOffset()
        self.my_resource.write('*CLS')
        self.my_resource.write("CURVE?")
        #data=np.array(self.my_resource.read_raw())
        #data = int(self.my_resource.read_raw(),16)\
        file = open('test.txt','w+')

        ##########################################
        # receive data format:
        # #510000<data>\n        receive 10000 data
        # #41000<data>\n         receive 1000 data
        #########################################
        #receive_data = self.my_resource.read_raw()
        data = np.frombuffer(self.my_resource.read_raw(),dtype=np.int8,count=int(POINT_NUMBER),offset=len(POINT_NUMBER) + 2)
        #data = np.empty((len(receive_data) - (len(POINT_NUMBER) + 3)))
        '''
        print(type(receive_data))
        for i in range(len(POINT_NUMBER) + 2, len(receive_data) - 1):
            data[i-(len(POINT_NUMBER) + 2)] = receive_data[i]
            file.write(str(data[i-(len(POINT_NUMBER) + 2)]) + ',')

        print(type(data))
        print(data.size)
        '''       
        #headerlen=2+int(data[1])
        #header=data[:headerlen]
        #ADC_wave=data[headerlen:-1]
        #ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
        print(data.size)
        Volts = (data - 0) * ymult  + yzero
        Time = np.arange(0, data.size, 1)
        Time = Time * xincr + xzero
        #Time=Time*1e9 #ns
        #Volts=Volts*1e3 #mV

        return Time, Volts

    def plotWave(self, Time, Volts):
        pylab.plot(Time, Volts)
        pylab.show()

  
if __name__=="__main__":
    POINT_NUMBER = '10000'
    CHANNEL = 'CH1'
    rm = visa.ResourceManager()
    print(rm.list_resources())
    list_sources = rm.list_resources()
    for resource_name in list_sources:
        match_result = re.match(r'TCPIP',resource_name)
        if match_result:
            tcpip_resource = resource_name
            print("the TCPIP resource is:" + repr(tcpip_resource))
            break
        else:
            print("no TCPIP resource,please check it!")
            exit()
    scope=MDO3034C(tcpip_resource)
    scope.testIO()
    scope.readSet(CHANNEL,POINT_NUMBER)
    
    Time,Volts = scope.readWave()
    scope.plotWave(Time, Volts)
    print(max(Volts)-min(Volts))
