import time
from machine import Pin, PWM
from debug import dbgprint


#channels
CH1 = 0
CH2 = 1
CH3 = 2

SERVO_1 = "srv1"
SERVO_2 = "srv2"
SERVO_3 = "srv3"


# Class that wil interface with our Servos
class SERVOModule:
    def __init__(self, pwm_pins, MIN_DUTY=300000, MAX_DUTY=2300000, freq=50):
        self.pwms = [PWM(Pin(pwm_pins[CH1])),
                     PWM(Pin(pwm_pins[CH2])),
                     PWM(Pin(pwm_pins[CH3]))]
        self.MIN_DUTY = MIN_DUTY
        self.MAX_DUTY = MAX_DUTY
        self.init_pwms(freq)
    
    # Initialize PWM Pins
    def init_pwms(self, freq):
        for pwm in self.pwms:
            pwm.freq(freq)
    
    # Deinitialize PWM fins
    def deinit_pwms(self):
        self.turn_off_servo()
        for pwm in self.pwms:
            pwm.deinit()
    
    # Map degree values from 0-180 to duty cycle in ns
    def map_range(self, deg):
      if deg < 0:
          deg = 0
      elif deg > 180:
          deg = 180
      duty_ns = int(self.MAX_DUTY - (deg * (self.MAX_DUTY - self.MIN_DUTY)/180))
      return duty_ns

    # Turn off servos
    def turn_off_servo(self):
        duty_ns = self.map_range(int(90))
        self.pwms[CH1].duty_ns(duty_ns)
        self.pwms[CH2].duty_ns(duty_ns)
        self.pwms[CH3].duty_ns(duty_ns)
        time.sleep(0.01)
    
    # Set servo position
    def set_servo_pos(self, degval):
        dbgprint(degval)
        duty_ns  = self.map_range(int(degval[SERVO_1]))
        dbgprint("Dutycycle CH1 in ns " + str(duty_ns))
        self.pwms[CH1].duty_ns(duty_ns)
        duty_ns  = self.map_range(int(degval[SERVO_2]))
        dbgprint("Dutycycle CH2 in ns " + str(duty_ns))
        self.pwms[CH2].duty_ns(duty_ns)
        duty_ns  = self.map_range(int(degval[SERVO_3]))
        dbgprint("Dutycycle CH3 in ns " + str(duty_ns))
        self.pwms[CH3].duty_ns(duty_ns)


def servoaction(servos, ujdata):
    ans = None
    if "wpg" in ujdata:
        if ujdata["wpg"] is "2": # websocket for servo page ready
            servos.set_servo_pos({'srv1': '90', 'srv2': '90', 'srv3': '90'})
            ans = "init"
        else:
            ans = "err"
    elif "srv1" and "srv2" and "srv3" in ujdata: # update servos
        servos.set_servo_pos(ujdata)
        ans = "ok"
    else:
        ans = "err"
            
    return ans