#! /usr/bin/env python

#reference:
#Luis Ardila 	leardilap@unal.edu.co 	22/03/15

#Liejian Chen   

import sys,time
import numpy
from PyQt5 import QtGui, QtCore, uic, QtWidgets

tctEnable = True
if tctEnable:
    import pymotor
    import VitualDevice as vitual_dev

testpass = False



class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        ################################################
        #initialize the device information,search usable device
        self.EmumDevice()

        self.uiFile = "GUI/XYZWidget.ui"
        self.ui = uic.loadUi(self.uiFile)
        self.Title = "XYZ Motor"
        ##############################################################
        self.timer = QtCore.QTimer()
        
        #Declaring Device
        self.SetMotor()
            

        #Move
        self.ui.MoveButton.clicked.connect(lambda:self.ClickMove(int(self.ui.SetPosX.text()), int(self.ui.SetPosY.text()), int(self.ui.SetPosZ.text())))

        #Step move X
        self.ui.XPlus.clicked.connect(lambda:self.MoveStep("X",1,self.ui.StepMoveX.value()))
        self.ui.XMinus.clicked.connect(lambda:self.MoveStep("X",-1,self.ui.StepMoveX.value()))

        #Step move Y
        self.ui.YPlus.clicked.connect(lambda:self.MoveStep("Y",1,self.ui.StepMoveY.value()))
        self.ui.YMinus.clicked.connect(lambda:self.MoveStep("Y",-1,self.ui.StepMoveY.value()))

        #Step move Z
        self.ui.ZPlus.clicked.connect(lambda:self.MoveStep("Z",1,self.ui.StepMoveZ.value()))
        self.ui.ZMinus.clicked.connect(lambda:self.MoveStep("Z",-1,self.ui.StepMoveZ.value()))

        #Home
        self.ui.ResetPosX.clicked.connect(lambda:self.Home("X"))
        self.ui.ResetPosY.clicked.connect(lambda:self.Home("Y"))
        self.ui.ResetPosZ.clicked.connect(lambda:self.Home("Z"))

        #scan
        self.ui.ScanBut.clicked.connect(self.Scan)

        #set motor
        self.ui.SetMotor.clicked.connect(self.SetMotor)

         # Var
        self.currentPosX = 0
        self.currentPosY = 0
        self.currentPosZ = 0

        #####################
        # Initializing Widget
        self.UpdateDesiredPos()
        self.ui.setWindowTitle(self.Title)
        self.timer.timeout.connect(self.UpdateDesiredPos)

       
        self.ui.show()

    def ClickMove(self,px,py,pz):
        self.new_thread = ControlThread(self.setdevice)
        self.new_thread.operation_num = 3
        self.new_thread.px = px
        self.new_thread.py = py
        self.new_thread.pz = pz
        self.new_thread.start()

    def MoveStep(self,motor,direction,steps):
        self.new_thread = ControlThread(self.setdevice)
        self.new_thread.operation_num = 4
        self.new_thread.mv = direction*steps
        if motor == "X":
            self.new_thread.motor = self.new_thread.laser_stage.Xaxis
        elif motor == "Y":
            self.new_thread.motor = self.new_thread.laser_stage.Yaxis
        elif motor == "Z":
            self.new_thread.motor = self.new_thread.laser_stage.Zaxis
        else:
            print("\n\n\nError!!!!!!!\n\n\n")
        self.new_thread.start()
    def Home(self,motor):
        self.new_thread = ControlThread(self.setdevice)
        self.new_thread.operation_num = 1
        if motor == "X":
            self.new_thread.motor = self.new_thread.laser_stage.Xaxis
        elif motor == "Y":
            self.new_thread.motor = self.new_thread.laser_stage.Yaxis
        elif motor == "Z":
            self.new_thread.motor = self.new_thread.laser_stage.Zaxis
        else:
            print("\n\n\nError!!!!!!!\n\n\n")
        self.new_thread.start()
    def Scan(self):
        self.new_thread = ControlThread(self.setdevice)
        self.new_thread.operation_num = 5
        self.new_thread.po = [self.ui.x0.value(),self.ui.y0.value(),self.ui.z0.value()]
        self.new_thread.dp = [self.ui.dx.value(),self.ui.dy.value(),self.ui.dz.value()]
        self.new_thread.Np = [self.ui.Nx.value(),self.ui.Ny.value(),self.ui.Nz.value()]
        self.new_thread.start()

    def SetMotor(self):
        self.setdevice = numpy.empty(3,dtype=object)
        self.setdevice[0] = self.device[self.ui.X_Motor_Num.value()-1]
        self.setdevice[1] = self.device[self.ui.Y_Motor_Num.value()-1]
        self.setdevice[2] = self.device[self.ui.Z_Motor_Num.value()-1]

    
    def EmumDevice(self):
        pymotor.enum_device()
        print('\nemum complete!\n')
        self.devenum ,self.dev_count = pymotor.enum_device()
        self.device = numpy.empty(5,dtype=object)
        if self.dev_count == 0:
            print("\nNo finding of device.")
            print("\nUse the vitual device:\n")
            self.device_name = ["testxmotor","testymotor","testzmotor"]
            self.i = 0
            for self.str_device in self.device_name:
                print('str_device:'+self.str_device)
                self.device[self.i] = vitual_dev.VitualDevice(self.device_name[self.i])
                print('device[]' + str(self.device[self.i]))
                #self.testmotor = pymotor.Motor(vitual_dev.VitualDevice(self.str_device).open_name)
                #self.testmotor.move(10)
                self.i = self.i + 1
        else:
            for self.dev_ind in range(0,self.dev_count):
                self.device[self.dev_ind] =pymotor.Motor(pymotor.Motor.get_name(self,self.devenum,self.dev_ind))
        
            
        
    
    def CurrentPosition(self):
        if tctEnable:
            self.currentPosX = self.setdevice[0].get_status_position()
            self.currentPosY = self.setdevice[1].get_status_position()
            self.currentPosZ = self.setdevice[2].get_status_position()

    def UpdateDesiredPos(self):
        if tctEnable:
            self.CurrentPosition()
            self.ui.CurrentPosX.display(self.currentPosX)
            self.ui.CurrentPosX_2.display(self.currentPosX)
            self.ui.CurrentPosY.display(self.currentPosY)
            self.ui.CurrentPosY_2.display(self.currentPosY)
            self.ui.CurrentPosZ.display(self.currentPosZ)
            self.ui.CurrentPosZ_2.display(self.currentPosZ)
            self.timer.start(500)


class ControlThread(QtCore.QThread):
    def __init__(self,device):
        super(ControlThread,self).__init__()
        self.laser_stage = Stage(device)
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

    def run(self):
        if self.operation_num == 1:
            self.laser_stage.Home(self.motor)
        elif self.operation_num == 2:
            self.laser_stage.Stop(self.motor)
        elif self.operation_num == 3:
            self.laser_stage.MoveAB(self.px,self.py,self.pz)
        elif self.operation_num == 4:
            self.laser_stage.MoveRE(self.motor,self.mv)
        elif self.operation_num == 5:
            self.laser_stage.Scan(self.po,self.dp,self.Np)
        else:
            time.sleep(1)


class Stage():
    def __init__(self,device):
        self.Xaxis = device[0]
        self.Yaxis = device[1]
        self.Zaxis = device[2]

    

    def Home(self,motor):
            if tctEnable:
                motor.home()

    def Stop(self,motor):
        if tctEnable:
            motor.stop()

    '''
    def Limits(self):
        self.Limits = Limits(self)
    '''
    def MoveAB(self,pos_X,pos_Y,pos_Z):
        if tctEnable:
            self.Xaxis.move(pos_X)
            self.Yaxis.move(pos_Y)
            self.Zaxis.move(pos_Z)

    def MoveRE(self,motor,movement):
        UpperLimit = 100     
        LowerLimit = -100    
        currentPos = motor.get_status_position()
        if currentPos + movement > UpperLimit:
            movement = UpperLimit - currentPos
        elif currentPos + movement < LowerLimit:
            movement = LowerLimit - currentPos

        if tctEnable:
            motor.forward(movement)
        time.sleep(0.1)

    
    def Scan(self,pos_o,dp,Np):
        self.x0 = pos_o[0] 
        self.y0 = pos_o[1]
        self.z0 = pos_o[2]
        self.dx = dp[0]
        self.dy = dp[1]
        self.dz = dp[2]
        self.Nx = Np[0]
        self.Ny = Np[1]
        self.Nz = Np[2]
        
        self.MoveAB(self.x0,self.y0,self.z0)
        #delay 1 second for motor moving to (x0,y0.z0)
        time.sleep(2)
    
        # # scan step by step
        # self.flag1 = self.flag2 = -1
        # for self.i in range(0, self.Nz):
        #     self.MoveRE(self.Zaxis, self.dz)
        #     self.flag1 = self.flag1 * (-1)
        #     for self.j in range(0, self.Nx):
        #         self.MoveRE(self.Xaxis, self.flag1 * self.dx)
        #         self.flag2 = self.flag2 * (-1)
        #         for self.k in range(0, self.Ny):
        #             self.MoveRE(self.Yaxis, self.flag2 * self.dy)
        #             #print(self.Xaxis.get_status_position(),self.Yaxis.get_status_position(),self.Zaxis.get_status_position())
        #             print(self.ui.CurrentPosX_2.value(),self.ui.CurrentPosY_2.value(),self.ui.CurrentPosZ_2.value())
        #             self.timer.timeout.connect(self.UpdateDesiredPos)
        #             self.timer.start(100)
        #             #self.UpdateDesiredPos() 
                    

        for self.PZ in range(self.z0, self.z0 + ((self.Nz + 1) * self.dz) , self.dz):
            for self.PX in range(self.x0, self.x0 + ((self.Nx + 1) * self.dx) , self.dx):
                for self.PY in range(self.y0, self.y0 + ((self.Ny + 1) * self.dy) , self.dy):
                    self.MoveAB(self.PX, self.PY, self.PZ)
                    print(self.Xaxis.get_status_position(),self.Yaxis.get_status_position(),self.Zaxis.get_status_position())
                    #self.timer.timeout.connect(self.UpdateDesiredPos)
                    #self.timer.start(100)
                    #time.sleep(0.1)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MainWidget()

    sys.exit(app.exec_())
