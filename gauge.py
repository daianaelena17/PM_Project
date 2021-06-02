from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.text import Label
from kivy.uix.label import Label as Label1
from kivy.lang.builder import Builder
from kivy.graphics import Line, Rectangle, Color
from kivy.clock import Clock
from kivy.utils import get_color_from_hex as rgb
from collections.abc import Iterable
from math import ceil
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy_garden.graph import Graph, MeshLinePlot, MeshStemPlot, LinePlot, SmoothLinePlot, ContourPlot
from kivy.app import App
from kivy.uix.popup import Popup
from math import sin
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from playsound import playsound
import random


from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

# This constant enforces the cap argument to be one of the caps accepted by the kivy.graphics.Line class
_ACCEPTED_BAR_CAPS = {"round", "none", "square"}

# Declare the defaults for the modifiable values
_DEFAULT_THICKNESS = 10
_DEFAULT_CAP_STYLE = 'round'
_DEFAULT_PRECISION = 10
_DEFAULT_PROGRESS_COLOUR = (1, 0, 0, 1)
_DEFAULT_BACKGROUND_COLOUR = (0.26, 0.26, 0.26, 1)
_DEFAULT_MAX_PROGRESS = 100
_DEFAULT_MIN_PROGRESS = 0
_DEFAULT_WIDGET_SIZE = 200
_DEFAULT_TEXT_LABEL = Label(text="{}%", font_size=40)

# Declare the defaults for the normalisation function, these are used in the textual representation (multiplied by 100)
_NORMALISED_MAX = 1
_NORMALISED_MIN = 0

_MAX_PERCENT_MQ_135 = 125
_MAX_PERCENT_MQ_7 = 200
_MAX_PERCENT_MQ_5 = 700
_MAX_PERCENT_MQ_Z14A = 1450

_MIN_ABNORMAL_MQ135 = 1000
_MIN_ABNORMAL_MQ5 = 450
_MIN_ABNORMAL_MQ7 = 200
_MIN_ABNORMAL_MQZ14A = 2000



_labelCO2 = Label(text="\nValoare MQ135\nAir quality:{}%\n", font_size=15, halign="center")
_labelV2 =  Label(text="\nValoare MQ7\n{}%\n",font_size=15, halign="center")
_labelV3 =  Label(text="\nValoare MQ5\nGas detection:{}%\n",font_size=15, halign="center")
_labelV4 = Label(text="\nValoare MH-Z14A\n{}%\n",font_size=15, halign="center")




def getPercent(x, MAX_ADMISSION, liniar = 0):
    if liniar == 0 :
        if x == 0:
            return 0
        else:
            return min(100 - (x - MAX_ADMISSION) / 10, 99)
    elif liniar == 1:
        if x == 0:
            return 0
        else:
            return min(x / (10 * MAX_ADMISSION), 0.99) * 100




class SensorsGraph(BoxLayout):
    def __init__(self, **kwargs):
        super(SensorsGraph, self).__init__(**kwargs)
        self.layout = FloatLayout()
        data = pd.read_csv("data.csv")
        x = data['Id']
        y1 = data['value1']
        y2 = data['value2']
        plt.cla()
        plt.xlabel("Numar valori masurate")
        plt.plot(x, y1, label='value1')
        plt.plot(x, y2, label='value2')
        plt.legend(loc='upper left')
        plt.tight_layout()
        self.figure = plt.gcf()
        self.plot = FigureCanvasKivyAgg(figure=self.figure)
        self.layout.add_widget(self.plot)
        self.add_widget(self.layout)
        self.last_data = []
    
    def animate(self, i):
        data = pd.read_csv("data.csv")
        x = data['Id']
        y1 = data['Value1']
        y2 = data['Value2']
        plt.cla()
        plt.xlabel("Numar valori masurate")
        plt.plot(x, y1, label='Value1')
        plt.plot(x, y2, label='Value2')

        plt.legend(loc='upper left')
        plt.tight_layout()


    def plot_data(self):
        ani = FuncAnimation(plt.gcf(), self.animate, interval = 500)
        plt.tight_layout()
        plt.show()

    def get_last_data(self):
        return self.last_data

    def update_axis(self):
        self.layout.remove_widget(self.plot)
        plt.clf()
        data = pd.read_csv("data.csv")
        x = data['Id']
        y1 = data['value1']
        y2 = data['value2']
        y3 = data['value3']
        y4 = data['value4']
        plt.cla()
        plt.plot(x, y1, label='MQ135')
        plt.plot(x, y2, label='MQ7')
        plt.plot(x, y3, label='MQ5')
        plt.plot(x, y4, label='MH-Z14A')
        plt.legend(loc="upper left")
        plt.tight_layout()
        self.last_data = [y4.iloc[-1], y3.iloc[-1], y2.iloc[-1], y1.iloc[-1]]
        self.plot = FigureCanvasKivyAgg(figure=self.figure)
        self.layout.add_widget(self.plot)

    



class CircularProgressBar(Widget):

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        # Initialise the values modifiable via the class properties
        self._thickness = _DEFAULT_THICKNESS
        self._cap_style = _DEFAULT_CAP_STYLE
        self._cap_precision = _DEFAULT_PRECISION
        self._progress_colour = _DEFAULT_PROGRESS_COLOUR
        self._background_colour = _DEFAULT_BACKGROUND_COLOUR
        self._max_progress = _DEFAULT_MAX_PROGRESS
        self._min_progress = _DEFAULT_MIN_PROGRESS
        self._widget_size = _DEFAULT_WIDGET_SIZE
        self._max_local = 0
        self._text_label = _DEFAULT_TEXT_LABEL
        self._dx = 0
        self._type = 0
        self._liniar = 0
        self._received = 0
        self._abnormal = False

        # Initialise the progress value to the minimum - gets overridden post init anyway
        self._value = _DEFAULT_MIN_PROGRESS

        # Store some label-related values to access them later
        self._default_label_text = _DEFAULT_TEXT_LABEL.text
        self._label_size = (0, 0)

        # Create some aliases to match the progress bar method names
        self.get_norm_value = self.get_normalised_progress
        self.set_norm_value = self.set_normalised_progress

    @property
    def abnormal(self):
        return (self._abnormal < self._received)

    
    @property
    def set_limit(self):
        return self._abnormal
    
    @set_limit.setter
    def set_limit(self, value):
        self._abnormal = value

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if type(value) != int:
            raise TypeError("Circular bar thickness only accepts an integer value, not {}!".format(type(value)))
        elif value <= 0:
            raise ValueError("Circular bar thickness must be a positive integer, not {}!".format(value))
        else:
            self._thickness = value


    @property
    def received_value(self):
        return self._received
    
    @received_value.setter
    def received_value(self, value) :
        self._received = value

    @property
    def cap_style(self):
        return self._cap_style
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value

    @cap_style.setter
    def cap_style(self, value):
        if type(value) != str:
            raise TypeError("Bar line cap argument must be a string, not {}!".format(type(value)))
        value = value.lower().strip()
        if value not in _ACCEPTED_BAR_CAPS:
            raise ValueError("Bar line cap must be included in {}, and {} is not!".format(_ACCEPTED_BAR_CAPS, value))
        else:
            self._cap_style = value


    @property
    def dx(self):
        return self._dx
    
    @dx.setter
    def dx(self, value):
        if type(value) != int :
            raise TypeError("Direction should be a integer, not {}!".format(type(value)))
        if value not in [0, 1]:
            raise ValueError("Bar line cap must be included in {}, and {} is not!".format([0,1], value))
        else:
            self._dx = value

    @property
    def cap_precision(self):
        return self._cap_precision

    @cap_precision.setter
    def cap_precision(self, value):
        if type(value) != int:
            raise TypeError("Circular bar cap precision only accepts an integer value, not {}!".format(type(value)))
        elif value <= 0:
            raise ValueError("Circular bar cap precision must be a positive integer, not {}!".format(value))
        else:
            self._cap_precision = value

    @property
    def progress_colour(self):
        return self._progress_colour

    @progress_colour.setter
    def progress_colour(self, value):
        if not isinstance(value, Iterable):
            raise TypeError("Bar progress colour must be iterable (e.g. list, tuple), not {}!".format(type(value)))
        else:
            self._progress_colour = value

    @property
    def background_colour(self):
        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        if not isinstance(value, Iterable):
            raise TypeError("Bar background colour must be iterable (e.g. list, tuple), not {}!".format(type(value)))
        else:
            self._background_colour = value


    @property
    def liniar(self):
        return self._liniar
    
    @liniar.setter
    def liniar(self, value):
        self._liniar = value        

    @property
    def max(self):
        return self._max_progress

    @max.setter
    def max(self, value):
        if type(value) != int:
            raise TypeError("Maximum progress only accepts an integer value, not {}!".format(type(value)))
        elif value <= self._min_progress:
            raise ValueError("Maximum progress - {} - must be greater than minimum progress ({})!"
                             .format(value, self._min_progress))
        else:
            self._max_progress = value

    @property
    def min(self):
        return self._min_progress

    @min.setter
    def min(self, value):
        if type(value) != int:
            raise TypeError("Minimum progress only accepts an integer value, not {}!".format(type(value)))
        elif value > self._max_progress:
            raise ValueError("Minimum progress - {} - must be smaller than maximum progress ({})!"
                             .format(value, self._max_progress))
        else:
            self._min_progress = value
            self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = value
            self._draw()

    @property
    def widget_size(self):
        return self._widget_size

    @property
    def max_local(self):
        return self._max_local
    
    @max_local.setter
    def max_local(self, value):
        self._max_local = value

    @widget_size.setter
    def widget_size(self, value):
        if type(value) != int:
            raise TypeError("Size of this widget must be an integer value, not {}!".format(type(value)))
        elif value <= 0:
            raise ValueError("Size of this widget must be a positive integer, not {}!".format(value))
        else:
            self._widget_size = value

    @property
    def label(self):
        return self._text_label

    @label.setter
    def label(self, value):
        if not isinstance(value, Label):
            raise TypeError("Label must a kivy.graphics.Label, not {}!".format(type(value)))
        else:
            self._text_label = value
            self._default_label_text = value.text

    @property
    def value_normalized(self):
  
        return self.get_normalised_progress()

    @value_normalized.setter
    def value_normalized(self, value):
 
        self.set_normalised_progress(value)

    def _refresh_text(self):
        self._text_label.text = self._default_label_text.format(str(int(self.get_normalised_progress() * 100)))
        self._text_label.refresh()
        self._label_size = self._text_label.texture.size

    def get_normalised_progress(self):
        return _NORMALISED_MIN + (self._value - self._min_progress) * (_NORMALISED_MAX - _NORMALISED_MIN) \
            / (self._max_progress - self._min_progress)

    def set_normalised_progress(self, norm_progress):
        if type(norm_progress) != float and type(norm_progress) != int:
            raise TypeError("Normalised progress must be a float or an integer, not {}!".format(type(norm_progress)))
        elif _NORMALISED_MIN > norm_progress or norm_progress > _NORMALISED_MAX:
            raise ValueError("Normalised progress must be between the corresponding min ({}) and max ({}), {} is not!"
                             .format(_NORMALISED_MIN, _NORMALISED_MAX, norm_progress))
        else:
            self.value = ceil(self._min_progress + (norm_progress - _NORMALISED_MIN) *
                              (self._max_progress - self._min_progress) / (_NORMALISED_MAX - _NORMALISED_MIN))

    def _draw(self):
        with self.canvas:
            self.canvas.clear()
            self._refresh_text()

            # Draw the background progress line
            Color(*self.background_colour)
            Line(circle=(self.pos[0] + self._widget_size / 2, self.pos[1] + self._widget_size / 2,
                         self._widget_size / 2 - self._thickness), width=self._thickness)

            # Draw the progress line
            Color(*self.progress_colour)
            Line(circle=(self.pos[0] + self._widget_size / 2, self.pos[1] + self._widget_size / 2,
                         self._widget_size / 2 - self._thickness, 0, self.get_normalised_progress() * 360),
                 width=self._thickness, cap=self._cap_style, cap_precision=self._cap_precision)

            # Center and draw the progress text
            Color(1, 1, 1, 1)
            Rectangle(texture=self._text_label.texture, size=self._label_size,
                      pos=(self._widget_size / 2 - self._label_size[0] / 2 + self.pos[0],
                           self._widget_size / 2 - self._label_size[1] / 2 + self.pos[1]))


class _Example(App):

    title = "Monitoring Air Quality"
    data = []
    problems = False

    # Simple animation to show the circular progress bar in action
    def animate(self, dt):
        self.problems = False
        for (index, bar) in enumerate(self.root.children[:-1]):
            if type(bar) is CircularProgressBar:
                if (self.data != []) :
                    bar.max_local = getPercent(self.data[index], bar.type, bar.liniar) 
                    bar.received_value = self.data[index]
                    if (bar.abnormal == True):
                        playsound("alarm.wav")
                        self.problems = True
                        bar.value = 100                 
                if bar.max_local == 0:
                    bar.value = 0.1
                elif bar.dx == 0:
                    if bar.value <= bar.max_local:
                        bar.value += random.randint(1,2)
                    else :
                        bar.dx = 1
                elif bar.dx == 1:
                    if bar.value > bar.max_local and bar.value >= 0:
                        bar.value -= random.randint(1, 2)
                    else :
                        bar.dx = 0
            elif type(bar) is SensorsGraph:
                bar.update_axis()
                self.store_data(bar.get_last_data())
            elif type(bar) is Label1:
                if self.problems == False:
                    bar.text = "Parametrii normali\n"
                elif self.problems == True:
                    bar.text = "Exista o problema. Verifica!\n"
                
         

        # Showcase that setting the values using value_normalized property also works
    # Simple layout for easy example
    def build(self):


        container = FloatLayout()


        c0 = CircularProgressBar()
        c0.pos = (50,50)
        container.add_widget(c0)
        graphG = SensorsGraph(pos = (50,50), size = (50,50))
        graphG.size_hint = (0.4, 1)
        graphG.pos_hint =  {"x":0.5,"y":.5}
        graphG.background_color = (0,0,1,1)
        graphG.width = 10
        graphG.length = 10



        label_alert = Label1(text="\nParametrii normali\n", font_size=20, halign="center", pos = (170, -10))

        container.add_widget(label_alert)

        container.add_widget(graphG)

        c1 = CircularProgressBar(pos = (350,50))
        c1.direction = 0
        c1.min = 0
        c1.max = 100
        c1.max_local = 0
        c1.widget_size = 200
        c1.label = _labelCO2
        c1.cap_style = "Square"
        c1.thickness = 10
        c1.color =  "011"
        c1. progress_colour = (0, 0, 1, 1)
        c1.cap_precision = 100
        c1.type = _MAX_PERCENT_MQ_135
        c1.set_limit = _MIN_ABNORMAL_MQ135


        c2 = CircularProgressBar(pos = (350,350))
        c2.min = 0
        c2.max = 100
        c2.max_local = 0
        c2.progress_colour = (1, 0.65, 0, 1)
        c2.widget_size = 200
        c2.label = _labelV2
        c2.cap_style = "Square"
        c2.thickness = 10
        c2.color =  "011"
        c2.cap_precision = 100
        c2.liniar = 1
        c2.set_limit = _MIN_ABNORMAL_MQ135

        c3 = CircularProgressBar(pos = (600,350))
        c3.min = 0
        c3.max = 100
        c3.max_local = 0
        c3.progress_colour = (0, 1, 0, 1)
        c3.widget_size = 200
        c3.label = _labelV3
        c3.cap_style = "Square"
        c3.thickness = 10
        c3.color =  "011"
        c3.cap_precision = 100
        c3.liniar = 1
        c3.set_limit = _MIN_ABNORMAL_MQ5

        c4 = CircularProgressBar(pos = (600,50))
        c4.min = 0
        c4.max = 100
        c4.max_local = 0
        c4.widget_size = 200
        c4.label = _labelV4
        c4.cap_style = "Square"
        c4.thickness = 10
        c4.color =  "011"
        c4.progress_colour = (1, 0, 0, 1)
        c4.cap_precision = 100
        c4.set_limit = _MIN_ABNORMAL_MQZ14A
        c4.liniar = 1
        c0.type = 20
 
        c2.type = _MAX_PERCENT_MQ_7
        c3.type = _MAX_PERCENT_MQ_5
        c4.type = _MAX_PERCENT_MQ_Z14A



        container.add_widget(c1)
        container.add_widget(c2)
        container.add_widget(c3)
        container.add_widget(c4)
        

        # Animate the progress bar
        Clock.schedule_interval(self.animate, 0.05)
        return container
    
    def store_data(self, data):
        self.data = data


if __name__ == '__main__':
    _Example().run()
