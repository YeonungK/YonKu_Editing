import sys

sys.path.append('C:/Users/szkop/Desktop/YonKu')

import numpy as np
import h5py
import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QComboBox, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt, QSize
import pyqtgraph as pg
import pandas as pd

from GUI import ShowHidePlotUi as shp



class plotWidget(QWidget):
    def __init__(self, plot_setting, dataset):
        super().__init__()
        
        # measurements
        self.temperatures = dataset['temperatures']
        self.resistances = dataset['resistances']
        self.lockIn = dataset['lockIn']
        self.lockIn2 = dataset['lockIn2']
        self.fields = dataset['fields']
        self.currents = dataset['currents']
        self.times = dataset['times']
        
        self.dataset = dataset
        
        # # show/hide plot ui
        # self.showHidePlotUi = shp.ShowHidePlotUi()
        
        # self.showlabel = QLabel("Show")
        # self.showlabel.setAlignment(Qt.AlignTop)
        
        # self.layout0 = QVBoxLayout()
        # self.layout0.addWidget(self.showlabel)
        
        # self.showHidePlotUi.setLayout(self.layout0)
        
        # self.plotCheckBoxes = {}
        
        # plots
        self.plots = {}
        self.plot_count = 0
        
        # plot setting values
        self.xAxis = plot_setting[0]
        self.yAxis = plot_setting[1]
        self.xAxisHiLim = plot_setting[2]
        self.xAxisLoLim = plot_setting[3]
        self.yAxisHiLim = plot_setting[4]
        self.yAxisLoLim = plot_setting[5]
        self.ticVal = plot_setting[6]
        self.gridLine = plot_setting[7]
        self.symbol = plot_setting[8]
        
        self.date_axis = pg.DateAxisItem(orientation='bottom',
                                        utcOffset=14400,               # set to your timezone offset if desired
                                        showValues=True,
                                        autoScale=True)
        
        self.title = self.yAxis.upper() + " vs " + self.xAxis.upper()
        
        self.colors = ['r', 'g', 'y', 'c', 'w']
        
        match self.xAxis:
            case "lockIn":
                self.xAxisData = self.lockIn
            case "lockIn2":
                self.xAxisData = self.lockIn2
            case "temperature":
                self.xAxisData = self.temperatures
            case "resistance":
                self.xAxisData = self.resistances
            case "field":
                self.xAxisData = self.fields
            case "current":
                self.xAxisData = self.currents
            case "time":
                self.xAxisData = self.times
        
        match self.yAxis:
            case "lockIn":
                self.yAxisData = self.lockIn
            case "lockIn2":
                self.yAxisData = self.lockIn2
            case "temperature":
                self.yAxisData = self.temperatures
            case "resistance":
                self.yAxisData = self.resistances
            case "field":
                self.yAxisData = self.fields
            case "current":
                self.yAxisData = self.currents
            case "time":
                self.yAxisData = self.times
        
        """create plot widget"""
        
        # labels and buttons
        
        # x axis stuff
        self.xAxisLabel = QLabel("x-Axis")
        self.xAxisLabel.setAlignment(Qt.AlignCenter)
        
        self.xAxisUnitLabel = QLabel(self.xAxis.upper())
        self.xAxisUnitLabel.setAlignment(Qt.AlignCenter)
        
        self.xAxisUnitComboBox = self.create_combo_box('x')
        
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.xAxisLabel)
        self.layout1.addWidget(self.xAxisUnitLabel)
        self.layout1.addWidget(self.xAxisUnitComboBox)
        
        
        # y axis stuff
        self.yAxisLabel = QLabel("y-Axis")
        self.yAxisLabel.setAlignment(Qt.AlignCenter)
        
        self.yAxisUnitLabel = QLabel(self.yAxis.upper())
        self.yAxisUnitLabel.setAlignment(Qt.AlignCenter)
        
        self.yAxisUnitComboBox = self.create_combo_box('y')
        
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.yAxisLabel)
        self.layout2.addWidget(self.yAxisUnitLabel)
        self.layout2.addWidget(self.yAxisUnitComboBox)
        
        
        # buttons
        
        self.settingB = QPushButton()
        self.settingB.setText("Setting")
        self.newPlotB = QPushButton()
        self.newPlotB.setText("Add a new plot")
        # self.showHideB = QPushButton()
        # self.showHideB.setText("Show/Hide plots")
        
        # self.showHideB.clicked.connect(self.showHidePlotUi_show)
        
        self.layout3 = QVBoxLayout()
        self.layout3.addWidget(self.settingB)
        self.layout3.addWidget(self.newPlotB)
        # self.layout3.addWidget(self.showHideB)
        
        # more layouts
        self.layout4 = QHBoxLayout()
        self.layout4.addLayout(self.layout1)
        self.layout4.addLayout(self.layout2)
        self.layout4.addLayout(self.layout3)
        
        self.layout = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        
        
        if self.xAxis == 'time':
            self.plot_widget.setAxisItems(axisItems = {'bottom': self.date_axis})
        
        self.plot_widget.setTitle(self.title)
        self.plot_widget.addLegend(offset = [-1,20])
        self.layout.addLayout(self.layout4)
        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)
        
        # signals
        
        self.newPlotB.clicked.connect(self.create_new_plot)
        
        
        # create plots
        # self.plot = self.plot_widget.plot(pen=pg.mkPen(color='r', width=2), name='CH1')
        
        # # set buffer size and create data dict
        # self.buffer_size = 60 * 60 * 7
        # self.data = {'CH1': {'x': [], 'y': []}}
        
        # # make a data logger
        # self.logger = dt.MultiChannelLogger("multichannel_log.h5", 'CH1')
       
    def create_new_plot(self):
        
        xAxisChannel = self.xAxisUnitComboBox.currentText()
        yAxisChannel = self.yAxisUnitComboBox.currentText()
        
        plot_channels = yAxisChannel + " vs " + xAxisChannel
        
        # self.plots[plot_channels] = self.plot_widget.plot(self.xAxisData[xAxisChannel], 
        #                                                     self.yAxisData[yAxisChannel])
        
        if not plot_channels in self.plots:
            self.plots[plot_channels] = self.plot_widget.plot(self.xAxisData[xAxisChannel], 
                                                                self.yAxisData[yAxisChannel], name = plot_channels, pen = self.colors[self.plot_count % 5])

            # self.plotCheckBoxes[plot_channels] = self.create_check_box(plot_channels, self.colors[self.plot_count % 5], self.plots[plot_channels])
            # self.layout0.addWidget(self.plotCheckBoxes[plot_channels])
            
            self.plot_count += 1
        else:
            pass
        
        
        
        print(self.plots.keys())
     
    def create_combo_box(self, Axis):
        
        combo_box = QComboBox()
        
        
        match Axis:
            case 'x':
                for ch in self.xAxisData.keys():
                    combo_box.addItem(ch)
            case 'y':
                for ch in self.yAxisData.keys():
                    combo_box.addItem(ch)
        
        return combo_box
    
    # def showHidePlotUi_show(self):
    #     self.showHidePlotUi.show()

        
    
    # def create_check_box(self, text, colour, plot):
        
    #     check_box = QCheckBox(text)
    #     # check_box.setIcon(QIcon(f'{colour}_icon.png'))
    #     # check_box.setIconSize(QSize(24,24))
        
    #     check_box.setChecked(True)
    #     # check_box.stateChanged.connect(self.show_hide_plot)
        
        
    #     return check_box

    # def show_hide_plot(self, signal_arg, key):
    #     # if self.plotCheckBoxes[key].isChecked():
    #     #     self.plots[key].show()
    #     # else:
    #     #     self.plots[key].hide()
    #     pass
        
        

    def plot_data(self):

        # if len(self.data['CH1']['x']) > self.buffer_size:
        #         self.data['CH1']['x'] = self.data['CH1']['x'][-self.buffer_size:]
        #         self.data['CH1']['y'] = self.data['CH1']['y'][-self.buffer_size:]
                
        # self.plot.setData(self.data['CH1']['x'], self.data['CH1']['y'])
        
        
        for plt_channels, plts in self.plots.items():
            
            plt_channels = plt_channels.split(" vs ")
            print(plt_channels)
            plts.setData(self.xAxisData[plt_channels[1]],self.yAxisData[plt_channels[0]])
        
        # self.logger.append(now, new_value)
        pass
        


class oldPlotWidget(QWidget):
    def __init__(self, plot_setting):
        super().__init__()
        
        # measurements
        
        
        
        self.datasetLink = plot_setting[8]
        self.dataset = pd.read_csv(self.datasetLink, header=[0,1])
        
        self.temperatures = {'ch_A':self.dataset['temperatures']['ch_A'].to_list(), 
                             'ch_B':self.dataset['temperatures']['ch_B'].to_list(), 
                             'ch_C':self.dataset['temperatures']['ch_C'].to_list(), 
                             'ch_D':self.dataset['temperatures']['ch_D'].to_list()}
        self.resistances = {'ch_A':self.dataset['resistances']['ch_A'].to_list(), 
                             'ch_B':self.dataset['resistances']['ch_B'].to_list(), 
                             'ch_C':self.dataset['resistances']['ch_C'].to_list(), 
                             'ch_D':self.dataset['resistances']['ch_D'].to_list()}
        self.lockIn = {'x':self.dataset['lockIn']['x'].to_list(), 
                             'y':self.dataset['lockIn']['y'].to_list(), 
                             'r':self.dataset['lockIn']['r'].to_list(), 
                             'theta':self.dataset['lockIn']['theta'].to_list()}
        
        
        try:
            self.lockIn2 = {'x':self.dataset['lockIn2']['x'].to_list(), 
                             'y':self.dataset['lockIn2']['y'].to_list(), 
                             'r':self.dataset['lockIn2']['r'].to_list(), 
                             'theta':self.dataset['lockIn2']['theta'].to_list()}
            
            self.fields = {'x':self.dataset['fields']['x'].to_list(),
                        'y':self.dataset['fields']['y'].to_list(),
                        'z':self.dataset['fields']['z'].to_list()}
            self.currents = {'current':self.dataset['currents']['current'].to_list()}
            
            self.times = {'time':self.dataset['times']['time'].to_list()}
        
            self.set = {'temperatures':self.temperatures, 'resistances':self.resistances, 'lockIn':self.lockIn, 'fields': self.fields, 'currents':self.currents, 'times':self.times}
        
        except KeyError:
            self.times = {'time':self.dataset['times']['time'].to_list()}
            self.set = {'temperatures':self.temperatures, 'resistances':self.resistances, 'lockIn':self.lockIn, 'times':self.times}
        
        
        
        # plots
        self.plots = {}
        self.plot_count = 0
        
        # show/hide plot ui
        self.showHidePlotUi = shp.ShowHidePlotUi()
        
        self.showlabel = QLabel("Show")
        self.showlabel.setAlignment(Qt.AlignTop)
        
        self.layout0 = QVBoxLayout()
        self.layout0.addWidget(self.showlabel)
        
        self.showHidePlotUi.setLayout(self.layout0)
        
        self.plotCheckBoxes = {}
        
        # plot setting values
        self.xAxis = plot_setting[0]
        self.yAxis = plot_setting[1]
        self.xAxisHiLim = plot_setting[2]
        self.xAxisLoLim = plot_setting[3]
        self.yAxisHiLim = plot_setting[4]
        self.yAxisLoLim = plot_setting[5]
        self.ticVal = plot_setting[6]
        self.gridLine = plot_setting[7]

        self.date_axis = pg.DateAxisItem(orientation='bottom',
                                        utcOffset=14400,               # set to your timezone offset if desired
                                        showValues=True,
                                        autoScale=True)
        
        self.title = self.yAxis.upper() + " vs " + self.xAxis.upper()
        
        self.colors = ['r', 'g', 'y', 'c', 'w']
        
        match self.xAxis:
            case "lockIn":
                self.xAxisData = self.lockIn
            case "lockIn2":
                self.xAxisData = self.lockIn2
            case "temperature":
                self.xAxisData = self.temperatures
            case "resistance":
                self.xAxisData = self.resistances
            case "field":
                self.xAxisData = self.fields
            case "current":
                self.xAxisData = self.currents
            case "time":
                self.xAxisData = self.times
        
        match self.yAxis:
            case "lockIn":
                self.yAxisData = self.lockIn
            case "lockIn2":
                self.yAxisData = self.lockIn2
            case "temperature":
                self.yAxisData = self.temperatures
            case "resistance":
                self.yAxisData = self.resistances
            case "field":
                self.yAxisData = self.fields
            case "current":
                self.yAxisData = self.currents
            case "time":
                self.yAxisData = self.times
        
        """create plot widget"""
        
        # labels and buttons
        
        # x axis stuff
        self.xAxisLabel = QLabel("x-Axis")
        self.xAxisLabel.setAlignment(Qt.AlignCenter)
        
        self.xAxisUnitLabel = QLabel(self.xAxis.upper())
        self.xAxisUnitLabel.setAlignment(Qt.AlignCenter)
        
        self.xAxisUnitComboBox = self.create_combo_box('x')
        
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.xAxisLabel)
        self.layout1.addWidget(self.xAxisUnitLabel)
        self.layout1.addWidget(self.xAxisUnitComboBox)
        
        
        # y axis stuff
        self.yAxisLabel = QLabel("y-Axis")
        self.yAxisLabel.setAlignment(Qt.AlignCenter)
        
        self.yAxisUnitLabel = QLabel(self.yAxis.upper())
        self.yAxisUnitLabel.setAlignment(Qt.AlignCenter)
        
        self.yAxisUnitComboBox = self.create_combo_box('y')
        
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.yAxisLabel)
        self.layout2.addWidget(self.yAxisUnitLabel)
        self.layout2.addWidget(self.yAxisUnitComboBox)
        
        
        # buttons
        
        self.settingB = QPushButton()
        self.settingB.setText("Setting")
        self.newPlotB = QPushButton()
        self.newPlotB.setText("Add a new plot")
        self.showHideB = QPushButton()
        self.showHideB.setText("Show/Hide plots")
        
        self.layout3 = QVBoxLayout()
        self.layout3.addWidget(self.settingB)
        self.layout3.addWidget(self.newPlotB)
        self.layout3.addWidget(self.showHideB)
        
        self.showHideB.clicked.connect(self.showHidePlotUi_show)
        
        # more layouts
        self.layout4 = QHBoxLayout()
        self.layout4.addLayout(self.layout1)
        self.layout4.addLayout(self.layout2)
        self.layout4.addLayout(self.layout3)
        
        self.layout = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        
        if self.xAxis == 'time':
            self.plot_widget.setAxisItems(axisItems = {'bottom': self.date_axis})
        
        self.plot_widget.setTitle(self.title)
        self.plot_widget.addLegend(offset = [-1,20])
        self.layout.addLayout(self.layout4)
        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)
        
        # signals
        
        self.newPlotB.clicked.connect(self.create_new_plot)
        
        
        # create plots
        # self.plot = self.plot_widget.plot(pen=pg.mkPen(color='r', width=2), name='CH1')
        
        # # set buffer size and create data dict
        # self.buffer_size = 60 * 60 * 7
        # self.data = {'CH1': {'x': [], 'y': []}}
        
        # # make a data logger
        # self.logger = dt.MultiChannelLogger("multichannel_log.h5", 'CH1')
       
    def create_new_plot(self):
        
        xAxisChannel = self.xAxisUnitComboBox.currentText()
        yAxisChannel = self.yAxisUnitComboBox.currentText()
        
        plot_channels = yAxisChannel + " vs " + xAxisChannel
        
        # self.plots[plot_channels] = self.plot_widget.plot(self.xAxisData[xAxisChannel], 
        #                                                     self.yAxisData[yAxisChannel])
        

        if not plot_channels in self.plots:
            self.plots[plot_channels] = self.plot_widget.plot(self.xAxisData[xAxisChannel], 
                                                                self.yAxisData[yAxisChannel], name = plot_channels, pen = self.colors[self.plot_count % 5])
            
            self.plotCheckBoxes[plot_channels] = self.create_check_box(plot_channels, self.colors[self.plot_count % 5], self.plots[plot_channels])
            self.layout0.addWidget(self.plotCheckBoxes[plot_channels])

            self.plot_count += 1
        else:
            pass
        print(self.plots.keys())
    
    def showHidePlotUi_show(self):
        self.showHidePlotUi.show()
        
         
    def create_check_box(self, text, colour, plot):
        
        check_box = QCheckBox(text)
        # check_box.setIcon(QIcon(f'{colour}_icon.png'))
        # check_box.setIconSize(QSize(24,24))
        
        check_box.setChecked(True)
        check_box.stateChanged.connect(self.show_hide_plot)
        
        
        return check_box

    def show_hide_plot(self):
        for key, plot in self.plots.items():
            if self.plotCheckBoxes[key].isChecked():
                plot.show()
            else:
                plot.hide()
     
     
    def create_combo_box(self, Axis):
        
        combo_box = QComboBox()
        
        
        match Axis:
            case 'x':
                for ch in self.xAxisData.keys():
                    combo_box.addItem(ch)
            case 'y':
                for ch in self.yAxisData.keys():
                    combo_box.addItem(ch)
        
        return combo_box

        
    
