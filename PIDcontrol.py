import numpy as np
import matplotlib.pyplot as plot
import matplotlib.animation as animation


class PIDcontrol:
    # Represents a PID controller able to output a control signal based on the difference between a measured input and a desired set point
    __previousError = 0.0           # Store error recorded during the last iteration
    __errorSummer = 0.0             # Store running sum of error value

    def __init__(self, power=1, proportionalgain=1, integralgain=0, differentialgain=0, saturation=0, integralstop=10, noise=0, dt=1):
        self._power = power
        self._proportionalGain = proportionalgain
        self._integralGain = integralgain
        self._differentialGain = differentialgain
        self._saturation = saturation
        self._integralstop = integralstop
        self._noise = noise
        self._dt = dt

    def set_power(self, power):
        self._power = power

    def get_power(self):
        return self._power

    def set_pgain(self, pgain):
        self._proportionalGain = pgain

    def get_pgain(self):
        return self._proportionalGain

    def set_igain(self, igain):
        self._integralGain = igain

    def get_igain(self):
        return self._integralGain

    def set_dgain(self, dgain):
        self._differentialGain = dgain

    def get_dgain(self):
        return self._differentialGain

    def set_saturation(self, saturation):
        self._saturation = saturation

    def get_saturation(self):
        return self._saturation

    def set_integralstop(self, value):
        self._integralstop = value

    def get_integralstop(self):
        return self._integralstop

    def set_noise(self, value):       # Must be non-negative
        if self._noise >= 0:
            self._noise = value
        else:
            self._noise = -value

    def get_noise(self):
        return self._noise

    def set_dt(self, dt):
        self._dt = dt

    def get_dt(self):
        return self._dt

    power = property(get_power, set_power)                        # Tunes the overall output power available
    proportionalGain = property(get_pgain, set_pgain)             # Tunes the proportional response of the control output to the measured error between input and set point
    integralGain = property(get_igain, set_igain)                 # Tunes the response of the control output to long term changes in the measured error
    differentialGain = property(get_dgain, set_dgain)             # Tunes the response of the control output to short term changes in the measured error
    saturation = property(get_saturation, set_saturation)         # Sets the absolute maximum magnitude of the control signal output
    integralstop = property(get_integralstop, set_integralstop)   # Caps the error summer value in order to control integrator wind up
    noise = property(get_noise, set_noise)                        # Standard deviation of a gaussian noise source added to the measured error signal
    dt = property(get_dt, set_dt)                                 # Time between iterations

    def control(self, processvalue, setpoint):
        # Output a control signal based on the measured error
        error = (setpoint - processvalue)  + np.random.normal(0, self.noise)   # Calculate difference between measured signal and chosen setpoint and add noise to the measurment
        differror = (error - self.__previousError) / self.dt                   # Differentiate error signal by comparing current error with the error measured during the last iteration
        self.__errorSummer += error * self.dt                                  # Integrate error signal by summing error values over time
        self.__previousError = error                                           # Record current error to be used during diferentiation in next iteration
        output = (error * self.proportionalGain + self.__errorSummer * self.integralGain + differror * self.differentialGain) * self.power  # PID control logic
        # Integral windup stop
        if self.__errorSummer > self.integralstop:
            self.__errorSummer = self.integralstop
        if self.__errorSummer < -self.integralstop:
            self.__errorSummer = -self.integralstop
        # Output saturation
        if self.saturation != 0:
            if output  > self.saturation:
                output = self.saturation
            if output < -self.saturation:
                output = -self.saturation
        # Debug prints
        print("error = " + str(error))
        print("differential error = " + str(differror))
        print("integral error = " + str(self.__errorSummer))
        return output


class Process:
    # Represents a 1-dimensional second order linear system with damping under the influence of an external driving force
    def __init__(self, value=0, mass=1, velocity=0, acceleration=0, damping=0, gravity=0):
        self._value = value
        self._mass = mass
        self._velocity = velocity
        self._acceleration = acceleration
        self._damping = damping
        self._gravity = gravity

    def get_value(self):
        return self._value

    def get_mass(self):
        return self._mass

    def set_mass(self, mass):
        self._mass = mass

    def get_velocity(self):
        return self._velocity

    def get_acceleration(self):
        return self._acceleration

    def get_damping(self):
        return self._damping

    def set_damping(self, damping):
        self._damping = damping

    def get_gravity(self):
        return self._gravity

    def set_gravity(self, gravity):
        self._gravity = gravity

    value = property(get_value)                   # The current value of the process
    mass = property(get_mass, set_mass)           # The inertia ( resistance to change ) of the process value
    velocity = property(get_velocity)             # The velocity ( rate of change ) of the process value
    acceleration = property(get_acceleration)     # The second derivative of the process value
    damping = property(get_damping,set_damping)   # Dissipative force working against the current velocity
    gravity = property(get_gravity, set_gravity)  # Offset driving force

    def change(self, force):
        # Change the process value
        self._acceleration = (force / self.mass) - self.gravity - (self.damping * self.velocity)   # The external forces acting on the process
        self._velocity += self.acceleration                                                         # The acceleration updates the current velocity
        self._value += self.velocity                                                                # The velocity updates the current process value ( Second order system )
        # Debug prints
        print("VALUE = " + str(self.value))
        print("VELOCITY = " + str(self.velocity))
        print("ACCELERATION = " + str(self.acceleration))