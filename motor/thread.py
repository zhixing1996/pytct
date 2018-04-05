import pymotor,stage,VitualDevice
import MDO3034Control as MD
import time
from datetime import datetime
import numpy as np
from PyQt5 import QtCore

class ControlThread(QtCore.QThread):
    def __init__(self,device):
        super(ControlThread,self).__init__()
        self.laser_stage = stage.Stage(device)
        #control message initial
        self.operation_num = 0
        self.motor = self.laser_stage.Xaxis
        self.px = 0
        self.py = 0
        self.pz = 0
        self.mv = 0
        self.po = [0,0,0]
        self.dp = [1,1,1]
        self.Np = [0,0,0]
        self.step = [8,8,8]
        self.speed = [0,0,0]

    #############################
    # 1.home 
    # 2.stop
    # 3.move set position
    # 4.move step
    # 5.scan
    # 6.set speed
    ############################
    def run(self):
        if self.operation_num == 1:
            self.laser_stage.Home(self.motor)
        elif self.operation_num == 2:
            self.laser_stage.Stop()
        elif self.operation_num == 3:
            self.laser_stage.MoveAB(self.px,self.py,self.pz)
        elif self.operation_num == 4:
            self.laser_stage.MoveRE(self.motor,self.mv)
        elif self.operation_num == 5:
            self.laser_stage.Scan(self.po,self.dp,self.Np)
        elif self.operation_num == 6:
            self.laser_stage.SetSpeed(self.step,self.speed)
        else:
            time.sleep(1)

class DataCapture(QtCore.QThread):
    def __init__(self):
        super(DataCapture,self).__init__()
        self.resource = 'ASRL1::INSTR'
        self.folder = './'
        self.device = []
        self.frequency = 10
        self.point_num = 10000
        self.timer = QtCore.QTimer()
        self.flag = True

    def run(self):
        self.scope = MD.MDO3034C(self.resource)
        self.info = self.scope.testIO()
        self.capture()
        if self.flag:
            self.timer.timeout.connect(self.capture)

    def capture(self):
        filename = self.folder + '/TCT' + str(datetime.now().isoformat()) + '.csv'
        self.pos = [self.device[0].get_status_position(),self.device[1].get_status_position(),self.device[2].get_status_position()]
        time,voltage = self.scope.readWave(self.point_num)
        myfile = open(filename,'a+')
        myfile.write('oscilloscope,' + self.info + '\n')
        myfile.write(',' + 'x' + self.pos[0] + '\n')
        myfile.write(',' + 'y' + self.pos[1] + '\n')
        myfile.write(',' + 'z' + self.pos[2] + '\n')
        self.scope.save_wave_data(time,voltage,myfile)
        self.timer.start(1000/self.frequency)



class ReadyThread(QtCore.QThread):
    sinOut = QtCore.pyqtSignal(str)
    def __init__(self):
        super(ReadyThread,self).__init__()
        self.resource_name = ''
        self.channel = 1
        self.point_number = 10000
        self.message = 'Nothing has done!'

    def run(self):
        self.scope = MD.MDO3034C(self.resource_name)
        msg = self.scope.testIO()
        self.message = "ocsilloscope information:" + msg
        self.sinOut.emit('send')
        self.scope.readSet(str(self.channel),str(self.point_number))
        self.message = "read set complete!"
        self.sinOut.emit('send')
        # self.scope.readWave()
        # self.message = "read wave complete!"
        # self.sinOut.emit('send')


