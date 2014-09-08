# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 14:44:52 2014

@author: nick

Pyserial interface for communicating with mini usb Analog IO board

Usage: Send plaintext commands, separated by newline/cr or semicolon.
       An eventual reply comes terminated with cr+lf.

Important commands:

*IDN?     Returns device identifier
*RST      Resets device, outputs are 0V.
OUT  <channel> <value>
          Sets <channel> (ranging from 0 to 2) to
          the voltage <value>. Use 2.5 as value, not 2.5E0
IN?  <channel>
          Returns voltage of input <channel> (ranging from 0 to 3).                     
ALLIN?    Returns all voltages                                                          
HELP      Print this help text.                                                         
ON /OFF   Switches the analog unit on/off.                                              
DIGOUT <value>                                                                          
          Sets the digital outputs to the                                               
          binary value (ranging from 0..3).                                             
                                                                                        
REMARK:                                                                                 
Output ranges from 0V to 4.095V. Input is capacitive and ranges                         
from 0V to 4.095V. 

"""

import serial


class Anlogcomm(object):
# Module for communicating with the mini usb IO board
    baudrate = 115200
    
    def __init__(self, port):
        self.serial = self._open_port(port)
        self._serial_write('a')# flush io buffer
        print self._serial_read() #will read unknown command

        
    def _open_port(self, port):
        ser = serial.Serial(port, timeout=5)
        #ser.readline()
        #ser.timeout = 1 #causes problem with nexus 7
        return ser
    
    def _serial_write(self, string):
        self.serial.write(string + '\n')
    
    def _serial_read(self):
        msg_string = self.serial.readline()
        # Remove any linefeeds etc
        msg_string = msg_string.rstrip()
        return msg_string
    
    def reset(self):
        self._serial_write('*RST')
        return self._serial_read()
        
    def get_voltage(self,channel):
        self._serial_write('IN?' + str(channel))
        voltage = self._serial_read()
        return voltage
        
    def get_voltage_all(self):
        self._serial_write('ALLIN?')
        allin = self._serial_read()
        return allin
    
    
    def set_voltage(self,channel,value):
        self._serial_write('OUT'+ str(channel) + str(value))
        return 
    
    def set_digitout(self,value):
         self._serial_write('DIGOUT' + str(value))
         return
    
    def serial_number(self):
        self._serial_write('*IDN?')
        return self._serial_read()