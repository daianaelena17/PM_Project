# SCSS2020--Monitoring-Air-Quality

### Members of the project: Radu Nichita && Diana Popescu

The project aims at taking data from sensors and displaying them in a GUI interface,
so the user can control if there is some problem where the sensor is located. The
data is collected via a server and is stored locally in a CSV File, as a log file.
The data visualization script can open only the CSV file to display the log file or
can connect to the server and take the new data directly.

We have measured some of the most important parameters of the air quality, such as:
-> CO2
-> CO
-> town-gas/smoke

The data is displayed both in graphic format (PPM on the y-axis) and via gauge charts,
just to compare current values with the actual standard. If there is some abnormal behaviour,
an alarm will start to show there is a problem where the sensors are placed. 

Installation requirements:  
  1.pip3 install selenium  
  2.pip install pyaudio / sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio
  3.sudo apt-get install gcc python-dev  
  4.sudo apt-get install python3-kivy    
  5.pip install kivy-garden  
  6.pip install matplotlib  
  7.pip install beautifulsoup4  
  8.pip install setuptools  
  9.pip install selenium  
  10.pip install kivy-garden.graph  
