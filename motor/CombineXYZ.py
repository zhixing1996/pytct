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


class Axis(QtWidgets.QWidget):
    def __init__(self, parent, Title, Device, uiFile):
        super(Axis, self).__init__(parent)

        self.ui = uic.loadUi(uiFile)

        #Declaring Device
        if tctEnable:
            self.Xaxis = Device[0]
            self.Yaxis = Device[1]
            self.Zaxis = Device[2]

        #Move
        self.ui.MoveButton.clicked.connect(self.MoveAB)

        #Step move X
        self.ui.XPlus.clicked.connect(lambda:self.MoveRE(self.Xaxis,self.ui.StepMoveX.value()))
        self.ui.XMinus.clicked.connect(lambda:self.MoveRE(self.Xaxis,-self.ui.StepMoveX.value()))

        #Step move Y
        self.ui.YPlus.clicked.connect(lambda:self.MoveRE(self.Yaxis,self.ui.StepMoveY.value()))
        self.ui.YMinus.clicked.connect(lambda:self.MoveRE(self.Yaxis,-self.ui.StepMoveY.value()))

        #Step move Z
        self.ui.ZPlus.clicked.connect(lambda:self.MoveRE(self.Zaxis,self.ui.StepMoveZ.value()))
        self.ui.ZMinus.clicked.connect(lambda:self.MoveRE(self.Zaxis,-self.ui.StepMoveZ.value()))

        #Home
        self.ui.ResetPosX.clicked.connect(lambda:self.Home(self.Xaxis))
        self.ui.ResetPosY.clicked.connect(lambda:self.Home(self.Yaxis))
        self.ui.ResetPosZ.clicked.connect(lambda:self.Home(self.Zaxis))
         # Var
        self.currentPosX = 0
        self.currentPosY = 0
        self.currentPosZ = 0
        self.Title = Title

        #####################
        # Initializing Widget
        self.UpdateDesiredPos()
        self.ui.setWindowTitle(Title)

       
        #self.lenght = self.ui.DesirePos.maximum()

    def Home(self,motor):
        ret = QtWidgets.QMessageBox.warning(self, "Homming",
                "Please Check the setup!\n\nAre you sure you really want\nto Home the motor?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Escape)
        if ret == QtWidgets.QMessageBox.Yes:
            if tctEnable:
                motor.home()
            else:
                self.ui.StatusLabel.setText("Home")
        self.UpdateDesiredPos()

    def Stop(self):
        if tctEnable:
            self.Xaxis.stop()
        else:
            self.ui.StatusLabel.setText("")

        self.UpdateDesiredPos()
    '''
    def Limits(self):
        self.Limits = Limits(self)
    '''
    def MoveAB(self):

        pos_X = int(self.ui.SetPosX.text())
        pos_Y = int(self.ui.SetPosY.text())
        pos_Z = int(self.ui.SetPosZ.text())
        if tctEnable:
            self.Xaxis.move(pos_X)
            self.Yaxis.move(pos_Y)
            self.Zaxis.move(pos_Z)
        self.UpdateDesiredPos()

    def MoveRE(self,motor,movement):
        UpperLimit = 100 #self.ui.DesirePos.maximum()
        LowerLimit = -100    #self.ui.DesirePos.minimum()
        currentPos = motor.get_status_position()
        if currentPos + movement > UpperLimit:
            movement = UpperLimit - currentPos
        elif currentPos + movement < LowerLimit:
            movement = LowerLimit - currentPos

        if tctEnable:
            motor.forward(movement)
        time.sleep(0.5)
        self.UpdateDesiredPos()

    
    def CurrentPosition(self):
        if tctEnable:
            self.currentPosX = self.Xaxis.get_status_position()
            self.currentPosY = self.Yaxis.get_status_position()
            self.currentPosZ = self.Zaxis.get_status_position()
    def UpdateDesiredPos(self):
        if tctEnable:
            self.CurrentPosition()
            self.ui.CurrentPosX.display(self.currentPosX)
            self.ui.CurrentPosY.display(self.currentPosY)
            self.ui.CurrentPosZ.display(self.currentPosZ)

    def run(self):
        self.ui.show()
'''
class Limits(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)

        # Declaring GUI
        self.ui = uic.loadUi('GUI/Limits.ui')
        self.ui.show()
        self.ui.ButtonBox.accepted.connect(lambda: self.Accepted)
        self.ui.UpperLimit.valueChanged.connect(lambda: self.UpdateUpperLimit)
        self.ui.LowerLimit.valueChanged.connect(lambda: self.UpdateLowerLimit)
        self.ui.setWindowTitle(str(parent.Title + " Limits"))
        self.ui.UpperLimit.setMaximum(parent.lenght*2)
        self.ui.LowerLimit.setMaximum(parent.lenght*2)
        self.ui.UpperLimit.setMinimum(-parent.lenght*2)
        self.ui.LowerLimit.setMinimum(-parent.lenght*2)
        self.ui.UpperLimit.setValue(parent.ui.DesirePos.maximum())
        self.ui.LowerLimit.setValue(parent.ui.DesirePos.minimum())

    def UpdateUpperLimit(self, parent):
        self.UpperLimit = self.ui.UpperLimit.value()
        self.LowerLimit = self.ui.LowerLimit.value()
        if self.UpperLimit - self.LowerLimit > parent.lenght:
            self.ui.LowerLimit.setValue(self.UpperLimit - parent.lenght)
        elif self.UpperLimit <= self.LowerLimit:
            self.ui.LowerLimit.setValue(self.UpperLimit - 1)

    def UpdateLowerLimit(self, parent):
        self.UpperLimit = self.ui.UpperLimit.value()
        self.LowerLimit = self.ui.LowerLimit.value()
        if self.LowerLimit + parent.lenght < self.UpperLimit:
            self.ui.UpperLimit.setValue(self.LowerLimit + parent.lenght)
        elif self.LowerLimit >= self.UpperLimit:
            self.ui.UpperLimit.setValue(self.LowerLimit + 1)

    def Accepted(self, parent):
        parent.ui.DesirePos.setMaximum(self.ui.UpperLimit.value())
        parent.ui.DesirePos.setMinimum(self.ui.LowerLimit.value())
        parent.ui.Scroll.setMaximum(self.ui.UpperLimit.value())
        parent.ui.Scroll.setMinimum(self.ui.LowerLimit.value())
'''
class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.stack = QtWidgets.QStackedWidget()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.stack)

        ################################################
        #initialize the device information,search usable device
        pymotor.enum_device()
        print('\nemum complete!\n')
        self.devenum ,self.dev_count = pymotor.enum_device()
        self.device = numpy.empty(5,dtype=object)
        if self.dev_count == 0:
            print("\nNo finding of device.")
            print("Use the vitual device:")
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
                self.device[self.dev_count] =pymotor.Motor(pymotor.Motor.get_name(self,self.devenum,self.dev_ind))



        ##############################################################
        # DETECTOR
        # X Detector
        XYZD_Title = "XYZ Motor"
        # XD_Device = "testxmotor"
        # YD_Device = "testymotor"
        # ZD_Device = "testzmotor"
        # XYZD_Device = [XD_Device,YD_Device,ZD_Device]
        #XD_Device = "xi-com:///dev/tty.usbmodem00000D81"
        XYZD_uiFile = "GUI/XYZWidget.ui"
        self.XYZDetector = Axis(self, XYZD_Title, self.device, XYZD_uiFile)

        ## Y Detector
        #YD_Title = "Y Detector" 
        #YD_Device = "testydet"
        #YD_uiFile = "GUI/YWidget.ui"
        #self.YDetector = Axis(self, YD_Title, YD_Device, YD_uiFile)

        ## Z Detector
        #ZD_Title = "Z Detector"
        #ZD_Device = "testzdet"
        #ZD_uiFile = "GUI/ZWidget.ui"
        #self.ZDetector = Axis(self, ZD_Title, ZD_Device, ZD_uiFile)

        ################################################################
        # MAIN WINDOW
        self.stack.addWidget(self.XYZDetector)
        #self.stack.addWidget(self.YDetector)
        #self.stack.addWidget(self.ZDetector)

        self.XYZDetector.run()
        #self.YDetector.run()
        #self.ZDetector.run()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MainWidget()

    sys.exit(app.exec_())
