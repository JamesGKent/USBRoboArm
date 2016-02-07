#!/usr/bin/env python3

#import the USB and Time librarys into Python
import usb.core, usb.util, time

class Arm():
    def __init__(self):
        """This class tries to take control of the robot arm and exposes several methods
of moving it, the first method is timed (it will stop that movement when the time expires)
this method is blocking i.e. it can only do one type of movement at once.
the second method requires one call to start the movement and another call to stop the movement.
if the arm is plugged in through a USB hub the communication delay may be longer,
if you get lost of timeout errors try increasing the property command_timeout from 50"""
        self.arm = usb.core.find(idVendor=0x1267, idProduct=0x000)
        if not self.arm:
            raise ValueError("Arm not found")

        self.command_timeout = 50

        # store the last sent command
        self.current_command = [0,0,0]
        # this allows us to "add" movements together
        # so instead of only going up and then right
        # both can be done at the same time

    def _send_command(self):
        """internal command, do not use"""
        try:
            self.arm.ctrl_transfer(0x40,6,0x100,0,self.current_command,self.command_timeout)
        except usb.core.USBError:
            print("Timed Out")
            
    def _build_command(self,
                      shoulder_down=None,
                      shoulder_up=None,
                      elbow_down=None,
                      elbow_up=None,
                      wrist_down=None,
                      wrist_up=None,
                      grip_open=None,
                      grip_closed=None):
        """internal command, do not use"""
        num = self.current_command[0]
        # get the current settings
        c_shoulder_down, rem        = divmod(num, 128)
        c_shoulder_up, rem          = divmod(rem, 64)
        c_elbow_down, rem           = divmod(rem, 32)
        c_elbow_up, rem             = divmod(rem, 16)
        c_wrist_down, rem           = divmod(rem, 8)
        c_wrist_up, rem             = divmod(rem, 4)
        c_grip_open, c_grip_closed  = divmod(rem, 2)
        if shoulder_down:
            c_shoulder_down = shoulder_down
        if shoulder_up:
            c_shoulder_up = shoulder_up
        if elbow_down:
            c_elbow_down = elbow_down
        if elbow_up:
            c_elbow_up = elbow_up
        if wrist_down:
            c_wrist_down = wrist_down
        if wrist_up:
            c_wrist_up = wrist_up
        if grip_open:
            c_grip_open = grip_open
        if grip_closed:
            c_grip_closed = grip_closed
        self.current_command[0] = c_shoulder_down*128 + c_shoulder_up*64 + c_elbow_down*32 + c_elbow_up*16 + c_wrist_down*8 + c_wrist_up*4 + c_grip_open*2 + c_grip_closed

    def light_on(self, duration=None):
        self.current_command[2] = 1
        self._send_command()
        if duration:
            time.sleep(duration)
            self.light_off()

    def light_off(self, duration=None):
        self.current_command[2] = 0
        self._send_command()
        if duration:
            time.sleep(duration)
            self.light_on()

    def base_left(self, duration=None):
        self.current_command[1] = 2
        self._send_command()
        if duration:
            time.sleep(duration)
            self.base_stop()

    def base_right(self, duration=None):
        self.current_command[1] = 1
        self._send_command()
        if duration:
            time.sleep(duration)
            self.base_stop()

    def base_stop(self):
        self.current_command[1] = 0
        self._send_command()

    def grip_open(self, duration=None):
        self._build_command(grip_open=1, grip_closed=0)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.grip_stop()

    def grip_close(self, duration=None):
        self._build_command(grip_open=0, grip_closed=1)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.grip_stop()

    def grip_stop(self):
        self._build_command(grip_open=0, grip_closed=0)
        self._send_command()

    def wrist_up(self, duration=None):
        self._build_command(wrist_up=1, wrist_down=0)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.wrist_stop()

    def wrist_down(self, duration=None):
        self._build_command(wrist_up=0, wrist_down=1)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.wrist_stop()

    def wrist_stop(self):
        self._build_command(wrist_up=1, wrist_down=0)
        self._send_command()

    def elbow_up(self, duration=None):
        self._build_command(elbow_up=1, elbow_down=0)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.elbow_stop()

    def elbow_down(self, duration=None):
        self._build_command(elbow_up=0, elbow_down=1)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.elbow_stop()

    def elbow_stop(self):
        self._build_command(elbow_up=0, elbow_down=0)
        self._send_command()

    def shoulder_up(self, duration=None):
        self._build_command(shoulder_up=1, shoulder_down=0)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.shoulder_stop()

    def shoulder_down(self, duration=None):
        self._build_command(shoulder_up=0, shoulder_down=1)
        self._send_command()
        if duration:
            time.sleep(duration)
            self.shoulder_stop()

    def shoulder_stop(self):
        self._build_command(shoulder_up=0, shoulder_down=0)
        self._send_command()

    def stop_moving(self):
        self.current_command[0] = 0
        self.current_command[1] = 0
        self._send_command()
