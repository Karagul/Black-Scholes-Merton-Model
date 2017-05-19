'''
MIT License
Copyright (c) 2017 Kiwi
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

####################################################################################################

'''
This is an important module which should be executed before running the Black-Scholes-Merton model.
There are many detailed explanations in this code, which may help users run this module smoothly.
'''

####################################################################################################

class AnnTime():

        ##### This module should be updated annually ######

    def __init__(self,Market,Start,Hold,End):

        import datetime as Dt
        import numpy as Np

        ###############################################
        ##### Datetime format as 'yyyymmddhhmmss' #####
        ###############################################

        Start = Dt.datetime(int(Start[0:4]),int(Start[4:6]),int(Start[6:8]),int(Start[8:10]),int(Start[10:12]),int(Start[12:]))
        Hold = Dt.datetime(int(Hold[0:4]),int(Hold[4:6]),int(Hold[6:8]),int(Hold[8:10]),int(Hold[10:12]),int(Hold[12:]))
        End = Dt.datetime(int(End[0:4]),int(End[4:6]),int(End[6:8]),int(End[8:10]),int(End[10:12]),int(End[12:]))

###############################################################################
###############################################################################

        def AnnTimeCal(Market,Start,Hold,End):

            #######################################################################
            ##### Holidays will be judged depending on different markets ##########
            ##### Since holidays will not change from year to year basically, #####
            ##### and it is fast for python to import csv files with pandas, ######
            ##### I will calculate the working days based on the csv file, ########
            ##### which should be updated for each year ###########################
            ##### Datetime format as 'yyyymmddhhmmss' #############################
            #######################################################################

            if Market == 'US':

                ##### Holidays in U.S. market in 2017 #######
                ##### '20170102','20170116','20170220', #####
                ##### '20170414','20170529','20170704', #####
                ##### '20170904','20171123','20171225' ######

                ##### Holidays for taking a half day off in U.S. market in 2017 #######
                ##### '20170703','20171124', still including in total trading days ####

                ##### Import the working date in 2017 #####
                from pandas import read_csv as Rcsv
                ##### Remember to change the file path #####
                TempWorkingDate = Rcsv(r'C:\Users\0010012\Desktop\Kiwi Files\2017USWDays.csv',squeeze = True)
                TempWorkingDate = TempWorkingDate['Date']
                WorkingDate = []
                for i in range(len(TempWorkingDate)):
                    WorkingDate.append(Dt.date(int(TempWorkingDate[i].split('/')[0]),
                                               int(TempWorkingDate[i].split('/')[1]),
                                               int(TempWorkingDate[i].split('/')[2])))
                WorkingDate = Np.array(WorkingDate)

                ##### There are 251 trading days in 2017 in total #####################
                ##### Half trading days are included in the computation ###############
                ##### Calculation will only contain trading days, not every day #######
                TotalTradingDays = len(WorkingDate)
                TotalTradingSeconds = TotalTradingDays*24*60*60

                ##### Look up the indices for start, hold, end date separately #####
                try:
                    StartIndex = Np.where(Start.date() == WorkingDate)[0][0]
                except:
                    print('Please input a valid trading date for start date in 2017.')
                    return None
                try:
                    HoldIndex = Np.where(Hold.date() == WorkingDate)[0][0]
                except:
                    print('Please input a valid trading date for hold date in 2017.')
                    return None
                try:
                    EndIndex = Np.where(End.date() == WorkingDate)[0][0]
                except:
                    print('Please input a valid trading date for end date in 2017.')
                    return None

                ##### Define the function to acquire the total passed seconds, #######
                ##### based on trading date, excluding the weekends and holidays #####
                def ToTraDatSec(WDate,BeginDate,BeginIndex,FinishDate,FinishIndex):
                    NextBegin = Dt.datetime(WDate[BeginIndex].year,WorkingDate[BeginIndex].month,WorkingDate[BeginIndex].day+1)
                    StartSeconds = (NextBegin-BeginDate).total_seconds()
                    NextFinish = Dt.datetime(WDate[FinishIndex].year,WorkingDate[FinishIndex].month,WorkingDate[FinishIndex].day)
                    EndSeconds = (FinishDate-NextFinish).total_seconds()
                    TotalSeconds = (FinishIndex-BeginIndex-1)*24*60*60+(StartSeconds+EndSeconds)
                    return TotalSeconds

                ##### Calculate the total passed seconds between start date and end date #####
                ##### based on trading date, excluding the weekends and holidays #############
                if EndIndex-StartIndex == 0:
                    TotalTTM = (End-Start).total_seconds()
                elif EndIndex-StartIndex < 0:
                    print('Please input a correct relationship between start date and end date.')
                    return None
                else:
                    TotalTTM = ToTraDatSec(WorkingDate,Start,StartIndex,End,EndIndex)

                ##### Calculate the total passed seconds between start date and hold date #####
                ##### based on trading date, excluding the weekends and holidays ##############
                if HoldIndex-StartIndex == 0:
                    TotalHdingPer = (Hold-Start).total_seconds()
                elif HoldIndex-StartIndex < 0:
                    print('Please input a correct relationship between start date and hold date.')
                    return None
                else:
                    TotalHdingPer = ToTraDatSec(WorkingDate,Start,StartIndex,Hold,HoldIndex)

                ##### Calculate the total passed seconds between hold date and end date #####
                ##### based on trading date, excluding the weekends and holidays ############
                if EndIndex-HoldIndex == 0:
                    TotalTTMAftHdingPer = (End-Hold).total_seconds()
                elif EndIndex-HoldIndex < 0:
                    print('Please input a correct relationship between hold date and end date.')
                    return None
                else:
                    TotalTTMAftHdingPer = ToTraDatSec(WorkingDate,Hold,HoldIndex,End,EndIndex)

                ##### Change the final output into list form #####
                AnnualizedTime = []
                AnnualizedTime.append(TotalTTM/TotalTradingSeconds)
                AnnualizedTime.append(TotalHdingPer/TotalTradingSeconds)
                AnnualizedTime.append(TotalTTMAftHdingPer/TotalTradingSeconds)
                AnnualizedTime.append(TotalTradingDays)

                return AnnualizedTime

        #######################################################################

            elif Market == 'TW':

                ##### Holidays in Taiwan market in 2017 #####
                ##### '20170102','20170125','20170126', #####
                ##### '20170127','20170130','20170131', #####
                ##### '20170201','20170227','20170228', #####
                ##### '20170403','20170404','20170501', #####
                ##### '20170529','20170530','20171004', #####
                ##### '20171009','20171010' #################

                ##### Market opens on Sat for adjustments in 2017 #####
                ##### '20170218','20170603','20170930' ################

                ##### Import the working date in 2017 #####
                from pandas import read_csv as Rcsv
                ##### Remember to change the file path #####
                TempWorkingDate = Rcsv(r'C:\Users\0010012\Desktop\Kiwi Files\2017TWWDays.csv',squeeze = True)
                TempWorkingDate = TempWorkingDate['Date']
                WorkingDate = []
                for i in range(len(TempWorkingDate)):
                    WorkingDate.append(Dt.date(int(TempWorkingDate[i].split('/')[0]),
                                               int(TempWorkingDate[i].split('/')[1]),
                                               int(TempWorkingDate[i].split('/')[2])))
                WorkingDate = Np.array(WorkingDate)

                ##### There are 246 trading days in 2017 in total #####################
                ##### Adjusted trading days are included in the computation ###########
                ##### Calculation will only contain trading days, not every day #######
                TotalTradingDays = len(WorkingDate)
                TotalTradingSeconds = TotalTradingDays*24*60*60

                ##### Look up the indices for start, hold, end date separately #####
                try:
                    StartIndex = Np.where(Start.date() == WorkingDate)[0][0]
                except:
                    print('Please input a valid trading date for start date in 2017.')
                    return None
                try:
                    HoldIndex = Np.where(Hold.date() == WorkingDate)[0][0]
                except:
                    print('Please input a valid trading date for hold date in 2017.')
                    return None
                try:
                    EndIndex = Np.where(End.date() == WorkingDate)[0][0]
                except:
                    print('Please input a valid trading date for end date in 2017.')
                    return None

                ##### Define the function to acquire the total passed seconds, #######
                ##### based on trading date, excluding the weekends and holidays #####
                def ToTraDatSec(WDate,BeginDate,BeginIndex,FinishDate,FinishIndex):
                    NextBegin = Dt.datetime(WDate[BeginIndex].year,WorkingDate[BeginIndex].month,WorkingDate[BeginIndex].day+1)
                    StartSeconds = (NextBegin-BeginDate).total_seconds()
                    NextFinish = Dt.datetime(WDate[FinishIndex].year,WorkingDate[FinishIndex].month,WorkingDate[FinishIndex].day)
                    EndSeconds = (FinishDate-NextFinish).total_seconds()
                    TotalSeconds = (FinishIndex-BeginIndex-1)*24*60*60+(StartSeconds+EndSeconds)
                    return TotalSeconds

                ##### Calculate the total passed seconds between start date and end date #####
                ##### based on trading date, excluding the weekends and holidays #############
                if EndIndex-StartIndex == 0:
                    TotalTTM = (End-Start).total_seconds()
                elif EndIndex-StartIndex < 0:
                    print('Please input a correct relationship between start date and end date.')
                    return None
                else:
                    TotalTTM = ToTraDatSec(WorkingDate,Start,StartIndex,End,EndIndex)

                ##### Calculate the total passed seconds between start date and hold date #####
                ##### based on trading date, excluding the weekends and holidays ##############
                if HoldIndex-StartIndex == 0:
                    TotalHdingPer = (Hold-Start).total_seconds()
                elif HoldIndex-StartIndex < 0:
                    print('Please input a correct relationship between start date and hold date.')
                    return None
                else:
                    TotalHdingPer = ToTraDatSec(WorkingDate,Start,StartIndex,Hold,HoldIndex)

                ##### Calculate the total passed seconds between hold date and end date #####
                ##### based on trading date, excluding the weekends and holidays ############
                if EndIndex-HoldIndex == 0:
                    TotalTTMAftHdingPer = (End-Hold).total_seconds()
                elif EndIndex-HoldIndex < 0:
                    print('Please input a correct relationship between hold date and end date.')
                    return None
                else:
                    TotalTTMAftHdingPer = ToTraDatSec(WorkingDate,Hold,HoldIndex,End,EndIndex)

                ##### Change the final output into list form #####
                AnnualizedTime = []
                AnnualizedTime.append(TotalTTM/TotalTradingSeconds)
                AnnualizedTime.append(TotalHdingPer/TotalTradingSeconds)
                AnnualizedTime.append(TotalTTMAftHdingPer/TotalTradingSeconds)
                AnnualizedTime.append(TotalTradingDays)

                return AnnualizedTime

        #######################################################################

            else:
                print('Error: Please enter the correct choice of market, US or TW.')
                return None

###############################################################################
###############################################################################

        TVariables = AnnTimeCal(Market,Start,Hold,End)

        ###############################################
        ##### Market = 'US' or 'TW' ###################
        ###############################################

        self.market = Market

        ##### The first term is time-to-maturity in annualized period #########################
        ##### The second term is the holding time in annualized period ########################
        ##### The last term is time-to-maturity in annualized period after holding period #####
        #####                         TotalDuration (ttm)                          ############
        ##### |------------------------|-----------------------------------------| ############
        #####  HoldingPeriod (hdingper) TotalDurationAfterHolding (ttmafthdingper) ############

        self.ttm = TVariables[0]
        self.hdingper = TVariables[1]
        self.ttmafthdingper = TVariables[2]
        self.toltradays = TVariables[3]

###############################################################################
###############################################################################
###############################################################################

'''
When using this module, user has two things to do in advance.
1. Download '2017TWWDays.csv' and '2017USWDays.csv' files from my git hub.
2. Modify the file path (line 45 and 144) that imports the two csv files.
'''

##### This is an example to use this module #####
import sys
# Remember to change the file path
sys.path.append(r'C:\Users\0010012\Desktop\Kiwi Files')
import AnnualizedTime

Market = 'US'
Start = '20170302223500'
Hold = '20170303233000'
End = '20170316120000'
AT = AnnualizedTime.AnnTime(Market,Start,Hold,End)
print(AT.market)
print(AT.ttm)
print(AT.hdingper)
print(AT.ttmafthdingper)
print(AT.toltradays)
#################################################
