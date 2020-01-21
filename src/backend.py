import os
import re
import pdb
import matplotlib.pyplot as plt

class BackEnd:
    """BackEnd handles parsing the data and creating coherent graphs from that"""
    def __init__(self):
        self.regex_theme = "<TBODY><TR><TD>(.+?)</TD></TR></TBODY>"
        self.regex_pattern = re.compile(self.regex_theme)

        self.carbonData = {}
        self.temperatureData = {}

        self.carbonAverages = {}
        self.temperatureAverages = {}


    def initializeCarbon(self):
        cData = []
        tempAverage = []

        with open("Co2.html", "r+") as carbonData:
            for lines in carbonData.readlines():
                cData.append(lines)
        
        for data in cData:
            try:
                tempString = re.findall(self.regex_pattern, data)[0].split("</TD><TD>")

                # Setting the carbon data to be year and month specific for all of the values
                self.carbonData[repr([tempString[0], tempString[1]])] = tempString[2:]

                # Adding each months average in order to calculate the average of the year
                tempAverage.append(float(tempString[3]))

                # If the month is 12 then calculate the average
                if tempString[1] == "12" or tempString[0] == "2019" and tempString[1] == "11":
                    tempA = 0
                    for average in tempAverage:
                        tempA += average
                    tempA /= int(tempString[1])
                    self.carbonAverages[int(tempString[0])] = tempA
                    tempAverage = []
            except (IndexError, ValueError):
                tempString = ""
            
    def initializeTemparature(self):
        tData = []

        with open("Temperature.html", "r+") as temperatureData:
            for lines in temperatureData.readlines():
                tData.append(lines)
        
        for data in tData:
            try:
                tempString = re.findall(self.regex_pattern, data)[0].split("</TD><TD>")

                # Setting the temperature data to be year specific for all of the values
                self.temperatureData[tempString[0]] = tempString[1:]

                # Setting the temparature yearly average
                self.temperatureAverages[int(tempString[0])] = float(tempString[1])
            except (IndexError, ValueError):
                tempString = ""

    def initialize(self):
        # Parsing and Initiating all the data for interaction
        self.initializeCarbon()
        self.initializeTemparature()

    def interact(self, year):
        carbonYearExists = False
        temperatureYearExists = False
        
        # The variables to be graphed are stored here
        years = []
        carbonAverage = []
        temperatureAverage = []

        # Checking if the years given exist in the said data collections
        if len(year) == 1:
            # Getting information on only one year
            try:
                if self.carbonAverages[year[0]]:
                    carbonYearExists = True
            except KeyError:
                return "The Given Year Is Out of Range"
        else:
            try:
                if self.carbonAverages[year[0]] and self.carbonAverages[year[1]]:
                    carbonYearExists = True
                if self.temperatureAverages[year[0]] and self.temperatureAverages[year[1]]:
                    temperatureYearExists = True
            except KeyError:
                return "The Given Years Are Out Of Range"
        
        # If both of the years exist in the data continue
        if carbonYearExists and temperatureYearExists:
            difference = year[1]-year[0]
            start = year[0]
            for i in range(difference+1):
                carbonAverage.append(self.carbonAverages[start+i])
                temperatureAverage.append(self.temperatureAverages[start+i])
                years.append(start+i)

            # Create graph
            fig, axs = plt.subplots(2)
            fig.suptitle("Carbon / Temperature")
            axs[0].plot(years, carbonAverage)
            axs[0].set_ylabel("Carbon")
            
            axs[1].plot(years, temperatureAverage)
            axs[1].set_xlabel("Years")
            axs[1].set_ylabel("Temperature")
            plt.show()
        if carbonYearExists and not temperatureYearExists:
            average = []
            months = []
            
            # Range number corrects 2019, since it only records 11 months
            rangeNumber = 12
            if year[0] == 2019:
                rangeNumber = 11
            for i in range(rangeNumber):
                cData = self.carbonData[repr([str(year[0]), str(i+1)])]
                average.append(float(cData[1]))
                months.append(i+1)
            plt.plot(months, average)
            if not year[0] in self.temperatureAverages.keys():
                plt.suptitle("Carbon Average of Year: {}".format(str(round(self.carbonAverages[year[0]], 2))))
            else:
                plt.suptitle("Carbon Average of Year: {}\nTemperature Average: {}".format(str(round(self.carbonAverages[year[0]], 2)), str(self.temperatureAverages[year[0]])))
            plt.ylabel("Carbon")
            plt.xlabel("Months")

            plt.show()