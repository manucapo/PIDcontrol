# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIDcontrol import PIDcontrol
from PIDcontrol import Process
import matplotlib.pyplot as plot
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

Controller = PIDcontrol()
Process = Process()
Process.mass = 10
Process.damping = 0.3
Process.gravity = 0
Controller.saturation = 1500
Controller.integralstop = 40
Controller.proportionalGain = 50
Controller.integralGain = 0
Controller.differentialGain = 0
Controller.power = 1
Controller.noise = 0.0
Controller.dt = 0.02
Setpoint = 0.0
xLen = 50
figure = plot.figure(figsize=(15, 8))
figure.subplots_adjust(bottom=0.4, left=0.4)
axes1 = figure.add_subplot(2, 1, 2)
axes2 = figure.add_subplot(2, 1, 1)
pax = figure.add_axes([0.01, 0.5, 0.02, 0.3])
iax = figure.add_axes([0.04, 0.5, 0.02, 0.3])
dax = figure.add_axes([0.07, 0.5, 0.02, 0.3])
noiax = figure.add_axes([0.105, 0.5, 0.02, 0.3])
#
pslider = Slider(ax=pax, label="P-gain", valmin=0.0, valmax=100, valinit=Controller.proportionalGain, orientation="vertical")
islider = Slider(ax=iax, label="I-gain", valmin=0.0, valmax=100, valinit=Controller.integralGain, orientation="vertical")
dslider = Slider(ax=dax, label="D-gain", valmin=0.0, valmax=100, valinit=Controller.differentialGain, orientation="vertical")
noislider = Slider(ax=noiax, label="Noise", valmin=0.0, valmax=2, valinit=Controller.noise, orientation="vertical")
#
damax = figure.add_axes([0.5, 0.01, 0.2, 0.02])
gravax = figure.add_axes([0.5, 0.04, 0.2, 0.02])
masax = figure.add_axes([0.5, 0.07, 0.2, 0.02])
damslider = Slider(ax=damax, label="Damping", valmin=0.05, valmax=0.5, valinit=Process.damping, orientation="horizontal")
gravslider = Slider(ax=gravax, label="Gravity", valmin=0.0, valmax=0.5, valinit=Process.gravity, orientation="horizontal")
masslider = Slider(ax=masax, label="Mass", valmin=1.0, valmax=100.0, valinit=Process.mass, orientation="horizontal")
xAxis = list(range(0, xLen))
yAxis1 = [0.0] * xLen
yAxis2 = [0.0] * xLen
yAxis3 = [0.0] * xLen
axes1.set_xlim([0, xLen])
axes1.set_ylim([-10, 20])
axes1.spines['bottom'].set_position('zero')
axes1.spines['top'].set_position('zero')
axes1.set_ylabel("Plant")
axes1.set_xticks([])
axes2.set_xlim([0, xLen])
axes2.set_ylim([-(Controller.saturation + (Controller.saturation / 10)), Controller.saturation + (Controller.saturation / 10)])
axes2.spines['bottom'].set_position('zero')
axes2.spines['top'].set_position('zero')
axes2.set_xticks([])
axes2.set_ylabel("Controller")
line1, = axes1.plot(xAxis, yAxis1)
line2, = axes1.plot(xAxis, yAxis2)
line3, = axes2.plot(xAxis, yAxis3)


def psliderupdate(value):
    Controller.proportionalGain = pslider.val


def isliderupdate(value):
    Controller.integralGain = islider.val


def dsliderupdate(value):
    Controller.differentialGain = dslider.val


def noisliderupdate(value):
    Controller.noise = noislider.val


def damsliderupdate(value):
    Process.damping = damslider.val


def gravsliderupdate(value):
    Process.gravity = gravslider.val


def massliderupdate(value):
    Process.mass = masslider.val


pslider.on_changed(psliderupdate)
islider.on_changed(isliderupdate)
dslider.on_changed(dsliderupdate)
noislider.on_changed(noisliderupdate)
damslider.on_changed(damsliderupdate)
gravslider.on_changed(gravsliderupdate)
masslider.on_changed(massliderupdate)

def animate(i, yaxis1, yaxis2, yaxis3):
    global Setpoint
    if i > 0:
        if (i % (5 * 25)) == 0:   # After 2 seconds
            if Setpoint == 0.0:
                Setpoint = 10.0
            elif Setpoint == 10.0:
                Setpoint = 0.0
    Process.change((Controller.control(Process.value, Setpoint)) * Controller.dt)
    yAxis1.append(Setpoint)
    yAxis2.append(Process.value)
    yAxis3.append(Controller.control(Process.value, Setpoint))
    yaxis1 = yaxis1[-xLen:]
    yaxis2 = yaxis2[-xLen:]
    yaxis3 = yaxis3[-xLen:]

    line1.set_ydata(yaxis1)
    line2.set_ydata(yaxis2)
    line3.set_ydata(yaxis3)
    lines = [line1, line2, line3]
    return lines


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    anim = animation.FuncAnimation(figure, animate, fargs=(yAxis1, yAxis2, yAxis3), interval=20, repeat=False, blit=True)
    plot.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
