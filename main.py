# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 12:41:23 2014

@author: nick
"""

"""
Created on Wed Aug 27 11:13:37 2014

@author: nick
"""

from kivy.config import Config
Config.set('graphics', 'width', '1280')# set screen size to nexus 7 dimensions looks ok on PC
Config.set('graphics', 'height', '720')
Config.write()
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty, BoundedNumericProperty,ListProperty, StringProperty
from kivy.clock import Clock
from kivy.utils import platform
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.tabbedpanel import TabbedPanel
import re
import os
import glob


import analogIO as analog



class FloatInput(TextInput): 

    pat = re.compile('[^0-9]')
    multiline = False
    halign = 'center'

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class AnalogIOControl(TabbedPanel):
    voltage = NumericProperty(0.0)
    DAC_0 = BoundedNumericProperty(0, min=0.0, max=4.095,errorhandler=lambda x: 4.095 if x > 4.096 else 0.0)
    DAC_1 = NumericProperty(0.0)
    DAC_2 = NumericProperty(0.0)
    DAC_3 = NumericProperty(0.0)
    voltage_0 = StringProperty('0.0')
    voltage_1 = StringProperty('0.0')
    voltage_2 = StringProperty('0.0')
    voltage_3 = StringProperty('0.0')
    serial = StringProperty('Not connected')
    set_voltage =  BoundedNumericProperty(0.0,min=0.0,max=4.095,errorhandler=lambda x: 4.095 if x > 4.095 else 0.0)
    digital_out = BoundedNumericProperty(0,min=0,max=3,errorhandler=lambda x: 3 if x > 3 else 0)
    connected = BooleanProperty(False)
    logo = 'CQTtools_inverted.png'
    graph = Graph()


    plot = ObjectProperty(None)

    device = None
    
    pm_range = 4
    
    iteration = 0
    
    dt = 0.25
    

    def update(self, dt):
        self.voltage = self.device.get_voltage(0)
        voltages = self.device.get_voltage_all()
        float_voltages = self.all_voltages(voltages)
        print self.ids.DAC_0.text
        self.plot_0.points.append((self.iteration*dt,float_voltages[0]))
        self.plot_1.points.append((self.iteration*dt,float_voltages[1]))
        self.plot_2.points.append((self.iteration*dt,float_voltages[2]))
        self.plot_3.points.append((self.iteration*dt,float_voltages[3]))
        self.iteration += 1*dt
        if self.iteration > 150:
            self.iteration = 0
            self.plot_1.points = []
            self.ids.graph1.remove_plot(self.plot_1)
            
    def connect_to_analogio(self, connection):
        if not self.connected:
            if platform == 'android': #to get access to serial port on android
                os.system("su -c chmod 777 " + connection)#has to run as child otherwise will not work with all su binarys
            self.device = analog.Anlogcomm(connection)
            Clock.schedule_interval(self.update, self.dt)
            self.connected = True
            self.serial = self.device.serial_number()
            plot_0 = MeshLinePlot(color=[1, 1, 1, 1])
            plot_1 = MeshLinePlot(color=[1, 0, 0, 1])
            plot_2 = MeshLinePlot(color=[0, 0, 1, 1])
            plot_3 = MeshLinePlot(color=[0, 1, 0, 1])
            self.ids.graph1.add_plot(plot_0)
            self.ids.graph1.add_plot(plot_1)
            self.ids.graph1.add_plot(plot_2)
            self.ids.graph1.add_plot(plot_3)
            self.plot_0 = plot_0
            self.plot_1 = plot_1
            self.plot_2 = plot_2
            self.plot_3 = plot_3
            
 
    def serial_ports_android(self):
        #Lists serial ports
        ports = glob.glob('/dev/ttyACM*')
        return ports
        
    def all_voltages(self,voltages):
        volt_0 = float(voltages[1:8])
        self.voltage_0 = self.format_voltages(volt_0)
        volt_1 = float(voltages[10:17])
        self.voltage_1 = self.format_voltages(volt_1)
        volt_2 = float(voltages[19:26])
        self.voltage_2 = self.format_voltages(volt_2)
        volt_3 = float(voltages[28:35])
        self.voltage_3 = self.format_voltages(volt_3)
        float_voltages = [volt_0,volt_1,volt_2,volt_3]
        return float_voltages
        
    def format_voltages(self,value):
        value = float(value)
        if 1 < value < 4.1:
            value = round(value,3)
            value = str(value) + ' V'
        else:
            value = round(value,3)
            value = str(value) + ' mV'
        return value
    
    def update_DAC(self,value,channel):
        print 'updated'
        return
        
        
        
class AnalogIOApp(App):
    def build(self):
        control = AnalogIOControl()
      
        return control
    
    def on_pause(self):
        return True
        
    def on_resume(self):
        pass




if __name__ == '__main__':
    AnalogIOApp().run()