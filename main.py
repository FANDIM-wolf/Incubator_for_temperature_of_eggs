
import numpy as np
import csv
import random
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from scipy.interpolate import CubicSpline

from convert import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pprint import pformat

      

import time
from pyfiglet import figlet_format

import sys
from PyQt5.QtCore import pyqtSignal , Qt , QTimer ,  QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow , QDialog , QVBoxLayout, QWidget, QSizePolicy , QTableWidgetItem ,  QMessageBox , QLabel , QSplashScreen ,QMessageBox
from PyQt5.QtGui import QMouseEvent , QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from main_window import Ui_MainWindow
    
input1 = ctrl.Antecedent(np.arange(0, 10.28, 0.01), 'input1')
input2 = ctrl.Antecedent(np.arange(38, 64, 0.01), 'input2')
input3 = ctrl.Antecedent(np.arange(36.3, 38, 0.01), 'input3')
output = ctrl.Consequent(np.arange(36.3, 38, 0.01), 'output')

input1['Q1'] = fuzz.zmf(input1.universe , 0.07443  , 0.3246)
input1['Q2'] = fuzz.gbellmf(input1.universe, 0.146, 2.54, 0.3508)
input1['Q3'] = fuzz.gbellmf(input1.universe, 0.641 , 2.47 , 1.328)
input1['Q4'] = fuzz.gbellmf(input1.universe, 2.58 , 2.5 , 4.558)
input1['Q5'] = fuzz.smf(input1.universe, 4.286 , 9.97)

input2['H1'] = fuzz.smf(input2.universe, 51.55, 62.8)
input2['H2_3'] = fuzz.gbellmf(input2.universe, 8 , 3.01 , 49.56)
input2['H4_5'] = fuzz.zmf(input2.universe, 38.1 , 44.9)

input3['T1_C'] = fuzz.smf(output.universe, 37.58 , 38)
input3['T2_3_C'] = fuzz.gbellmf(input3.universe, 0.1717 , 2.61 , 37.6)
input3['T4_C'] = fuzz.gbellmf(input3.universe, 0.211 , 3 , 37.2)
input3['T5_C'] = fuzz.zmf(input3.universe, 36.68 , 37.32)

output['T1'] = fuzz.smf(output.universe, 37.58 , 38)
output['T2_3'] = fuzz.gbellmf(output.universe, 0.1717 , 2.61 , 37.6)
output['T4'] = fuzz.gbellmf(output.universe,0.211 , 3 , 37.2)
output['T5'] = fuzz.zmf(output.universe, 36.68 , 37.32)

rule1 = ctrl.Rule(input1['Q1'] & input2['H1'] & input3['T1_C'], output['T1'])
rule2 = ctrl.Rule(input1['Q1'] & input2['H2_3'] & input3['T2_3_C'], output['T2_3'])
rule3 = ctrl.Rule(input1['Q1'] & input2['H4_5'] & input3['T4_C'], output['T4'])
rule4 = ctrl.Rule(input1['Q1'] & input2['H4_5'] & input3['T5_C'], output['T5'])
rule5 = ctrl.Rule(input1['Q2'] & input2['H1'] & input3['T1_C'], output['T1'])
rule6 = ctrl.Rule(input1['Q2'] & input2['H2_3'] & input3['T2_3_C'], output['T2_3'])
rule7 = ctrl.Rule(input1['Q2'] & input2['H4_5'] & input3['T4_C'], output['T4'])
rule8 = ctrl.Rule(input1['Q2'] & input2['H4_5'] & input3['T5_C'], output['T5'])
rule9 = ctrl.Rule(input1['Q3'] & input2['H1'] & input3['T1_C'], output['T1'])
rule10 = ctrl.Rule(input1['Q3'] & input2['H2_3'] & input3['T2_3_C'], output['T2_3'])
rule11 = ctrl.Rule(input1['Q3'] & input2['H4_5'] & input3['T4_C'], output['T4'])
rule12 = ctrl.Rule(input1['Q3'] & input2['H4_5'] & input3['T5_C'], output['T5'])
rule13 = ctrl.Rule(input1['Q4'] & input2['H1'] & input3['T1_C'], output['T1'])
rule14 = ctrl.Rule(input1['Q4'] & input2['H2_3'] & input3['T2_3_C'], output['T2_3'])
rule15 = ctrl.Rule(input1['Q4'] & input2['H4_5'] & input3['T4_C'], output['T4'])
rule16 = ctrl.Rule(input1['Q4'] & input2['H4_5'] & input3['T5_C'], output['T5'])
rule17 = ctrl.Rule(input1['Q5'] & input2['H1'] & input3['T1_C'], output['T1'])
rule18 = ctrl.Rule(input1['Q5'] & input2['H2_3'] & input3['T2_3_C'], output['T2_3'])
rule19 = ctrl.Rule(input1['Q5'] & input2['H4_5'] & input3['T4_C'], output['T4'])
rule20 = ctrl.Rule(input1['Q5'] & input2['H4_5'] & input3['T5_C'], output['T5'])
anfisctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5,rule6, rule7, rule8, rule9, rule10,
                                rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20])
anfissimulation = ctrl.ControlSystemSimulation(anfisctrl)

def set_inputs(day,hours , minutes ,humidity , current_temperature , anfissimulation):
    #convert time 
    hours = hours
    day = day+round(normalize_minutes(convert_hours_in_minutes(hours , minutes)),2)
    Q = convert_day_in_energy(day)
    
    # set main inputs

    anfissimulation.input['input1'] = Q
    anfissimulation.input['input2'] = round(humidity,0)
    anfissimulation.input['input3'] = round(current_temperature,1)                       

    anfissimulation.compute()
    print(Q , " CT :" , current_temperature ,"H :" , humidity)
    return anfissimulation.output['output']

  
    

class MyFourPlots(FigureCanvas):
    def __init__(self, parent, membership_functions, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MyFourPlots, self).__init__(fig)
        self.setParent(parent)

        for mf in membership_functions.terms:
            self.axes.plot(membership_functions.universe, membership_functions[mf].mf, label=mf)
        self.axes.legend()
        self.axes.grid()




class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,  anfissimulation, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.anfissimulation = anfissimulation
        self.pushButton.clicked.connect(self.get_values)
        self.pushButton_2.clicked.connect(self.plot_membership_functions)
        self.pushButton_3.clicked.connect(self.show_elements_for_settings)
        #self.pushButton_4.clicked.connect(self.show_elements_for_expert_estimate)
        self.pushButton_5.clicked.connect(self.estimate_for_certain_time)
        self.widget.hide()
        self.widget_2.hide()
        self.widget_3.hide()
        self.widget_4.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        self.label_11.hide()
        self.pushButton_5.hide()
        

    def error_dialog(self, err_message):
        error_dlg = QMessageBox(self)
        error_dlg.setIcon(QMessageBox.Information)
        error_dlg.setText("An error occurred: " + str(err_message))
        error_dlg.setWindowTitle(" Error ")
        error_dlg.exec()
    def check_for_borderline(self , value , edge_one , edge_two , message):
        if value >= edge_one and  value <= edge_two:
            
            return True
        else:
            return False
    #check data and in case of error call information window with error message
    def validate_data(self, Humidity , Temperature , Day):
        Temperature = float(Temperature)
        Humidity = float(Humidity)
        validation = None
        if int(Day) == 1 or int(Day) == 2:
            print("Day one!")
            #37,7 – 38,2 оптимальные значения
            #38,3 – 38,6 риск перегрев
            #38,6 – 39,4 перегрев
            #37,2 – 37,7 Риск задержки вывода
            #36,1 – 37,2 Задержка вывода
            if((Humidity >= 61 and Humidity <= 64) and (Temperature >= 37.7 and Temperature <= 38.1 )):
                validation = True
                print("Valid data!")
            else:
                validation = False
                if(self.check_for_borderline(Temperature,38.2 ,38.6 , "риск перегрева")== True):
                    self.error_dialog("38,2 – 38,6 риск перегревa")
                    
                if(self.check_for_borderline(Temperature,38.7 ,39.4 , "перегрев")== True):
                    self.error_dialog("38,7 – 39,4 перегрев")
                if(self.check_for_borderline(Temperature,37.2 ,37.7 , "Риск задержки вывода")== True):
                    self.error_dialog("37,2 – 37,7 Риск задержки вывода")
                if(self.check_for_borderline(Temperature,36.1 ,37.1 , "Задержка вывода")== True):
                    self.error_dialog("36,1 – 37,2 Задержка вывода")
                #self.error_dialog("Invalid data !")
                return validation
        elif int(Day) == 3 or int(Day) == 4 or int(Day) == 5:
            #37,5 – 38,2
            if((Humidity >= 50 and Humidity <= 54) and (Temperature >= 37.7 and Temperature <= 38.2 )):
                validation = True
            else:
                validation = False
                if(self.check_for_borderline(Temperature,38.3 ,38.4 , "риск перегрева")== True):
                    self.error_dialog("38,2 – 38,6 риск перегревa")
                    
                if(self.check_for_borderline(Temperature,38.5 ,39.4 , "перегрев")== True):
                    self.error_dialog("38,7 – 39,4 перегрев")
                if(self.check_for_borderline(Temperature,37.3 ,37.4 , "Риск задержки вывода")== True):
                    self.error_dialog("37,2 – 37,7 Риск задержки вывода")
                if(self.check_for_borderline(Temperature,36.1 ,37.2 , "Задержка вывода")== True):
                    self.error_dialog("36,1 – 37,2 Задержка вывода")
                #self.error_dialog("Invalid data !")
                return validation
        elif int(Day) == 6 or int(Day) == 7 or int(Day) == 8 or int(Day) == 9 or int(Day) == 10:
            #37,5 – 38,2
            if((Humidity >= 50 and Humidity <= 54) and (Temperature >= 37.7 and Temperature <= 38.2 )):
                validation = True
            else:
                validation = False
                if(self.check_for_borderline(Temperature,38.3 ,38.4 , "риск перегрева")== True):
                    self.error_dialog("38,2 – 38,6 риск перегревa")
                    
                if(self.check_for_borderline(Temperature,38.5 ,39.4 , "перегрев")== True):
                    self.error_dialog("38,7 – 39,4 перегрев")
                if(self.check_for_borderline(Temperature,37.3 ,37.4 , "Риск задержки вывода")== True):
                    self.error_dialog("37,2 – 37,7 Риск задержки вывода")
                if(self.check_for_borderline(Temperature,36.1 ,37.2 , "Задержка вывода")== True):
                    self.error_dialog("36,1 – 37,2 Задержка вывода")
                #self.error_dialog("Invalid data !")
                return validation
        elif int(Day) == 11 or int(Day) == 12 or int(Day) == 13 or int(Day) == 14 or int(Day) == 15:
            if((Humidity >= 38 and Humidity <= 42) and (Temperature >= 37.7 and Temperature <= 38.2 )):
                validation = True
            else:
                validation = False
                if(self.check_for_borderline(Temperature,38.3 ,38.4 , "риск перегрева")== True):
                    self.error_dialog("38,2 – 38,6 риск перегревa")
                    
                if(self.check_for_borderline(Temperature,38.5 ,39.4 , "перегрев")== True):
                    self.error_dialog("38,7 – 39,4 перегрев")
                if(self.check_for_borderline(Temperature,37.3 ,37.4 , "Риск задержки вывода")== True):
                    self.error_dialog("37,2 – 37,7 Риск задержки вывода")
                if(self.check_for_borderline(Temperature,36.1 ,37.2 , "Задержка вывода")== True):
                    self.error_dialog("36,1 – 37,2 Задержка вывода")
                #self.error_dialog("Invalid data !")
                return validation
        elif int(Day) == 16 or int(Day) == 17 or int(Day) == 18 :
            if((Humidity >= 38 and Humidity <= 42) and (Temperature >= 37.7 and Temperature <= 38.2 )):
                validation = True
            else:
                validation = False
                if(self.check_for_borderline(Temperature,38.3 ,38.4 , "риск перегрева")== True):
                    self.error_dialog("38,2 – 38,6 риск перегревa")
                    
                if(self.check_for_borderline(Temperature,38.5 ,39.4 , "перегрев")== True):
                    self.error_dialog("38,7 – 39,4 перегрев")
                if(self.check_for_borderline(Temperature,37.3 ,37.4 , "Риск задержки вывода")== True):
                    self.error_dialog("37,2 – 37,7 Риск задержки вывода")
                if(self.check_for_borderline(Temperature,36.1 ,37.2 , "Задержка вывода")== True):
                    self.error_dialog("36,1 – 37,2 Задержка вывода")
                #self.error_dialog("Invalid data !")
                return validation
        return validation
    def calculate_data(self , day ,humidity , current_temperature  ):
        day_unchangeable = day # dont change input values for this day
        current_temperature_unchangeable = current_temperature
        humidity_unchangeable = humidity
        # Get the time from the QTimeEdit
        selected_time = self.timeEdit.time()

        # Get the hour and minute from the QTime object
        hour = selected_time.hour()
        minute = selected_time.minute()
        hour_unchangeable = hour  #dont change humidity and current temperature for this hour 
        print("Hours and minutes:", hour, minute, humidity)
        print("Hours and minutes:", hour, minute, humidity)
        #write validation function
        temp_in_incubator = set_inputs(int(day), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation)
        print(temp_in_incubator)
        with open('data.csv', mode='w', newline='') as data_file:
            fieldnames = [ 'day' ,'hours', 'humidity' , 'temperature']
            writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            writer.writeheader()
            for j in range(1):
                for i in range(1, 19):
                    if i == 1 or i == 2:
                        for l in range(0,24):
                            
                            if int(i) == int(day_unchangeable) and int(l) == int(hour_unchangeable):

                                day = i
                                hours = l
                                
                        
                                humidity = humidity_unchangeable
                                current_temperature = current_temperature_unchangeable
                                
                                print("THIS DAY WE DONT CHANGE : " , humidity_unchangeable , current_temperature_unchangeable )
                                print ("SET INPUTS: " , humidity_unchangeable , current_temperature_unchangeable)
                                print(int(i), int(hour), int(minute), float(humidity), float(current_temperature))
                                temperature = round(set_inputs(int(i), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation),1)
                                writer.writerow({'day': i, 'hours':hours  , 'humidity':humidity ,'temperature': temperature   })
                            else:
                                day = i
                                hours = l
                                
                                humidity = random.randint(61, 64)
                                current_temperature = 38
                                
                                print(int(i), int(hour), int(minute), float(humidity), float(current_temperature))
                                temperature = round(set_inputs(int(i), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation),1)
                                writer.writerow({'day': i, 'hours':hours  , 'humidity':humidity ,'temperature': temperature   })
                    elif i == 3 or i == 4 or i == 5:
                        for l in range(0,24):
                                if int(i) == int(day_unchangeable) and int(l) == int(hour_unchangeable):

                                    day = i
                                    hours = l
                                    
                                    humidity = humidity_unchangeable
                                    current_temperature = current_temperature_unchangeable
                                
                                    print ("SET INPUTS: " , humidity_unchangeable , current_temperature_unchangeable)
                                else:
                                    day = i
                                    hours = l
                                    
                                    humidity = random.randint(50, 54)
                                    current_temperature = round(random.uniform(37.6 , 38.0),1)
                                    
                                
                                temperature = round(set_inputs(int(i), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation),1)
                                writer.writerow({'day': i, 'hours':hours  , 'humidity':humidity ,'temperature': temperature   })
                    elif i == 6 or i == 7 or i == 8:
                        for l in range(0,24):
                            if int(i) == int(day_unchangeable) and int(l) == int(hour_unchangeable):

                                day = i
                                hours = l
                                
                                humidity = humidity_unchangeable
                                current_temperature = current_temperature_unchangeable
                
                                print ("SET INPUTS: " , humidity_unchangeable , current_temperature_unchangeable)
                            else:
                                day = i
                                hours = l
                                
                                humidity = random.randint(50, 54)
                                current_temperature = 37.6
                                
                            temperature = round(set_inputs(int(i), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation),1)
                            writer.writerow({'day': i, 'hours':hours  , 'humidity':humidity ,'temperature': temperature   })
                    elif i == 9 or i == 10:
                        for l in range(0,24):
                            if int(i) == int(day_unchangeable) and int(l) == int(hour_unchangeable):

                                day = i
                                hours = l
                                
                                humidity = humidity_unchangeable
                                current_temperature = current_temperature_unchangeable
                                
                                print ("SET INPUTS: " , humidity_unchangeable , current_temperature_unchangeable)
                            else:
                                day = i
                                hours = l
                                
                                humidity = random.randint(50, 54)
                                current_temperature = 37.6
                                
                            temperature = round(set_inputs(int(i), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation),1)
                            writer.writerow({'day': i, 'hours':hours  , 'humidity':humidity ,'temperature': temperature   })
                    elif i == 11 or i == 12 or i == 13 or i == 14 or i == 15:
                        for l in range(0,24):
                            if int(i) == int(day_unchangeable) and int(l) == int(hour_unchangeable):

                                day = i
                                hours = l

                                humidity = humidity_unchangeable
                                current_temperature = current_temperature_unchangeable
                                
                                print ("SET INPUTS: " , humidity_unchangeable , current_temperature_unchangeable)
                            else:
                                day = i
                                hours = l

                                humidity = random.randint(38, 42)
                                current_temperature = round(random.uniform(37.6 , 38.0),1)
                                
                            temperature = round(set_inputs(int(i), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation),1)
                            writer.writerow({'day': i, 'hours':hours  , 'humidity':humidity ,'temperature': temperature   })
                    elif i == 16 or i == 17 or i == 18:
                        for l in range(0,24):
                            if int(i) == int(day_unchangeable) and int(l) == int(hour_unchangeable):
                                day = i
                                hours = l
                        
                                humidity = humidity_unchangeable
                                current_temperature = current_temperature_unchangeable
                                
                                print ("SET INPUTS: " , humidity_unchangeable , current_temperature_unchangeable)
                            else:
                                day = i
                                hours = l
                        
                                humidity = random.randint(38, 42)
                                current_temperature = round(random.uniform(36.8 , 36.9),1)
                                
                            temperature = round(set_inputs(int(i), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation),1)
                            print("Temperature 16,17,18:  " ,   )
                            writer.writerow({'day': i, 'hours':hours  , 'humidity':humidity ,'temperature': temperature   })
                    else:
                        print("end")
        print("Calcuated")  
    def show_elements_for_settings(self):
        self.widget.hide()
        self.widget_2.hide()
        self.widget_3.hide()
        self.widget_4.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_10.hide()
        self.label_9.hide()
        self.label_11.hide()
        self.label.show()
        self.label_2.show()
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.lineEdit.show()
        self.lineEdit_2.show()
        self.lineEdit_3.show()
        self.timeEdit.show()
        self.pushButton.show()
        self.pushButton_5.hide()
    def show_elements_for_expert_estimate(self):
        self.widget.hide()
        self.widget_2.hide()
        self.widget_3.hide()
        self.widget_4.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label.show()
        self.label_2.show()
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.lineEdit.show()
        self.lineEdit_2.show()
        self.lineEdit_3.show()
        self.timeEdit.show()
        self.pushButton.hide()
        self.pushButton_5.show()
        self.label_10.show()
        self.label_11.hide()
    def plot_membership_functions(self):
        self.widget.show()
        self.widget_2.show()
        self.widget_3.show()
        self.widget_4.show()
        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.label_9.show()
        self.label_10.hide()
        self.label_11.hide()
        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.lineEdit_3.hide()
        self.timeEdit.hide()
        self.pushButton.hide()
        self.pushButton_5.hide()
        
        plot_a = MyFourPlots(self.widget, input1, width=3, height=2)
        plot_b = MyFourPlots(self.widget_2, input2, width=3, height=2)
        plot_c = MyFourPlots(self.widget_3, input3, width=3, height=2)
        plot_d = MyFourPlots(self.widget_4, output, width=3, height=2)

        layout_a = QtWidgets.QVBoxLayout(self.widget)
        layout_b = QtWidgets.QVBoxLayout(self.widget_2)
        layout_c = QtWidgets.QVBoxLayout(self.widget_3)
        layout_d = QtWidgets.QVBoxLayout(self.widget_4)

        layout_a.addWidget(plot_a)
        layout_b.addWidget(plot_b)
        layout_c.addWidget(plot_c)
        layout_d.addWidget(plot_d)

        self.widget.setLayout(layout_a)
        self.widget_2.setLayout(layout_b)
        self.widget_3.setLayout(layout_c)
        self.widget_4.setLayout(layout_d)

    def get_values(self ):
        
        humidity = self.lineEdit_2.text()
        current_temperature  = self.lineEdit_3.text()
        day = self.lineEdit.text()
        

        #if(self.validate_data(humidity,current_temperature,day) == True):
        self.calculate_data(day ,humidity , current_temperature )
            
        #else:
        #    self.error_dialog("Data is not calculated!")
    def estimate_for_certain_time(self):
        humidity = self.lineEdit_2.text()
        current_temperature  = self.lineEdit_3.text()
        day = self.lineEdit.text()
        day_unchangeable = day # dont change input values for this day
        current_temperature_unchangeable = current_temperature
        humidity_unchangeable = humidity
        # Get the time from the QTimeEdit
        selected_time = self.timeEdit.time()

        # Get the hour and minute from the QTime object
        hour = selected_time.hour()
        minute = selected_time.minute()
        
        print("Hours and minutes:", hour, minute, humidity)
        print("Hours and minutes:", hour, minute, humidity)
        #write validation function
        temp_in_incubator = set_inputs(int(day), int(hour), int(minute), float(humidity), float(current_temperature), self.anfissimulation)
        self.label_11.setText(str(round(temp_in_incubator , 1)))
        self.label_11.show()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    my_main_window = MyMainWindow(anfissimulation)
    my_main_window.show()
    sys.exit(app.exec_())