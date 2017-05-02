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
                WorkingDate = Rcsv(r'C:\Users\0010012\Desktop\Kiwi Files\Programing Files\2017USWDays.csv',squeeze = True)
                for i in range(len(WorkingDate)):
                    WorkingDate[i] = (Dt.date(int(WorkingDate[i].split('/')[0]),
                                              int(WorkingDate[i].split('/')[1]),
                                              int(WorkingDate[i].split('/')[2])))

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
                WorkingDate = Rcsv(r'C:\Users\0010012\Desktop\Kiwi Files\Programing Files\2017TWWDays.csv',squeeze = True)
                for i in range(len(WorkingDate)):
                    WorkingDate[i] = (Dt.date(int(WorkingDate[i].split('/')[0]),
                                              int(WorkingDate[i].split('/')[1]),
                                              int(WorkingDate[i].split('/')[2])))

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


class BSMModel():

    def __init__(self,BasicInfo,TradingDays,Dividend = [0,'None']):

        import math as M
        from scipy.stats import norm

        ##########################################
        ##### BasicInfo = [Type,T,S,K,Vol,R] #####
        ##### Type = 'C' or 'P' ##################
        ##### T ; S ; K ; Vol ; R as float #######
        ##########################################

        ####################################################################
        ##### This model is only able to calculate the situation, ##########
        ##### which the company pays one-time dividends in the period, #####
        ##### including cash dividends or stock dividends ##################
        ####################################################################

        ##########################################################
        ##### Dividend = [D,Type], Default = [0,'None'] ##########
        ##### If type is 'None', D should be 0 ###################
        ##### If type is 'Con', D should be a float number #######
        ##### If type is 'Dis', D should be a list, ##############
        ##### whose form is [cash dividends,stock dividends] #####
        ##########################################################

###############################################################################
###############################################################################

        def Price(Type,T,S,K,Vol,R,D):

            ##### Notice: T is the time to maturity of the options #####

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return S*M.exp((-D[0])*T)*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return K*M.exp((-R)*T)*norm.cdf(-d2)-S*M.exp((-D[0])*T)*norm.cdf(-d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Delta(Type,T,S,K,Vol,R,D):

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C':
                    return norm.cdf(d1)
                elif Type == 'P':
                    return -norm.cdf(-d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C':
                    return M.exp((-D[0])*T)*norm.cdf(d1)
                elif Type == 'P':
                    return -M.exp((-D[0])*T)*norm.cdf(-d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C':
                    return norm.cdf(d1)
                elif Type == 'P':
                    return -norm.cdf(-d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Vega(Type,T,S,K,Vol,R,D):

            #######################################################################################
            ##### The total vega of a position is the multiplication of its quantity and vega #####
            #######################################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return S*M.sqrt(T)*norm.pdf(d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return S*M.exp((-D[0])*T)*M.sqrt(T)*norm.pdf(d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return S*M.sqrt(T)*norm.pdf(d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Theta(Type,T,S,K,Vol,R,D):

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return -(S*norm.pdf(d1)*Vol)/(2*M.sqrt(T))-R*K*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return -(S*norm.pdf(d1)*Vol)/(2*M.sqrt(T))+R*K*M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return -(M.exp((-D[0])*T)*S*norm.pdf(d1)*Vol)/(2*M.sqrt(T))-R*K*M.exp((-R)*T)*norm.cdf(d2)+D[0]*S*M.exp((-D[0])*T)*norm.cdf(d1)
                elif Type == 'P':
                    return -(M.exp((-D[0])*T)*S*norm.pdf(d1)*Vol)/(2*M.sqrt(T))+R*K*M.exp((-R)*T)*norm.cdf(-d2)-D[0]*S*M.exp((-D[0])*T)*norm.cdf(-d1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return -(S*norm.pdf(d1)*Vol)/(2*M.sqrt(T))-R*K*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return -(S*norm.pdf(d1)*Vol)/(2*M.sqrt(T))+R*K*M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Gamma(Type,T,S,K,Vol,R,D):

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return norm.pdf(d1)/(S*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return (M.exp((-D[0])*T)*norm.pdf(d1))/(S*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return norm.pdf(d1)/(S*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Rho(Type,T,S,K,Vol,R,D):

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return K*T*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return -K*T*M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return K*T*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return -K*T*M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return K*T*M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return -K*T*M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Vanna(Type,T,S,K,Vol,R,D):

            ###################################################################################################
            ##### Vanna is a second order derivative of the option value, #####################################
            ##### which equals to the derivative of vega with respect to underlying stock price, ##############
            ##### and it also mathematically equals to the derivative of delta with respect to volatility #####
            ###################################################################################################

            #######################################################################################################
            ##### Vanna can be used to maintain a delta-hedged or vega-hedged portfolio, ##########################
            ##### as it helps anticipate changes to the effectiveness of a delta-hedge as volatility changes, #####
            ##### or the effectiveness of a vega-hedge against change in the underlying stock price ###############
            #######################################################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (-norm.pdf(d1)*d2)/Vol
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (-M.exp((-D[0])*T)*norm.pdf(d1)*d2)/Vol
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (-norm.pdf(d1)*d2)/Vol
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Charm(Type,T,S,K,Vol,R,D):

            ##############################################################################################
            ##### Color is a second order derivative of the option value, ################################
            ##### which measures the instantaneous rate of change of delta over the passage of time, #####
            ##### and equals to the derivative of theta with respect to the underlying stock price #######
            ##############################################################################################

            #######################################################################################
            ##### Color can be used to monitor a delta-hedging position over a certain period #####
            ##### as it helps anticipate the effectiveness of the hedge as time passes ############
            ##### The mathematical result of the formula for charm is expressed in delta/year #####
            ##### and it is often useful to divide this by the number of days per year, ###########
            ##### in order to arrive at the delta decay per day ###################################
            #######################################################################################

            ##############################################################################
            ##### This use is fairly accurate, ###########################################
            ##### when the number of days remaining until option expiration is large #####
            ##### When an option nears expiration, charm itself may change quickly, ######
            ##### rendering full day estimates of delta decay inaccurate #################
            ##############################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return ((-norm.pdf(d1))*(2*R*T-d2*Vol*M.sqrt(T)))/(2*T*Vol*M.sqrt(T))
                elif Type == 'P':
                    return ((-norm.pdf(d1))*(2*R*T-d2*Vol*M.sqrt(T)))/(2*T*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return (D[0]*M.exp((-D[0])*T)*norm.cdf(d1))-((M.exp((-D[0])*T)*norm.pdf(d1))*(2*(R-D[0])*T-d2*Vol*M.sqrt(T)))/(2*T*Vol*M.sqrt(T))
                elif Type == 'P':
                    return (-D[0]*M.exp((-D[0])*T)*norm.cdf(-d1))-((M.exp((-D[0])*T)*norm.pdf(d1))*(2*(R-D[0])*T-d2*Vol*M.sqrt(T)))/(2*T*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return ((-norm.pdf(d1))*(2*R*T-d2*Vol*M.sqrt(T)))/(2*T*Vol*M.sqrt(T))
                elif Type == 'P':
                    return ((-norm.pdf(d1))*(2*R*T-d2*Vol*M.sqrt(T)))/(2*T*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Speed(Type,T,S,K,Vol,R,D):

            #########################################################################################################
            ##### Speed is a third order derivative of the option value, ############################################
            ##### which measures the rate of change of Gamma with respect to changes in underlying stock price, #####
            ##### and equals to the derivative of gamma with respect to the underlying stock price ##################
            ##### Speed can be important to monitor when delta-hedging or gamma-hedging a portfolio ################
            #########################################################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return ((-norm.pdf(d1))/(S*S*Vol*M.sqrt(T)))*(((d1)/(Vol*M.sqrt(T)))+1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return ((-M.exp((-D[0])*T)*norm.pdf(d1))/(S*S*Vol*M.sqrt(T)))*(((d1)/(Vol*M.sqrt(T)))+1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                if Type == 'C' or Type == 'P':
                    return ((-norm.pdf(d1))/(S*S*Vol*M.sqrt(T)))*(((d1)/(Vol*M.sqrt(T)))+1)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Zomma(Type,T,S,K,Vol,R,D):

            #############################################################################################
            ##### Zomma is a third order derivative of the option value, ################################
            ##### which measures the rate of change of gamma with respect to changes in volatility, #####
            ##### and equals to the derivative of gamma with respect to the volatility ##################
            #############################################################################################

            ##################################################################################################
            ##### Zomma can be a useful sensitivity to monitor when maintaining a gamma-hedged portfolio #####
            ##### as it helps anticipate changes to the effectiveness of the hedge as volatility changes #####
            ##################################################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (norm.pdf(d1)*(d1*d2-1))/(S*Vol*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (M.exp((-D[0])*T)*norm.pdf(d1)*(d1*d2-1))/(S*Vol*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (norm.pdf(d1)*(d1*d2-1))/(S*Vol*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Color(Type,T,S,K,Vol,R,D):

            #####################################################################################
            ##### Color is a third order derivative of the option value, ########################
            ##### which measures the rate of change of gamma over the passage of time, ##########
            ##### and equals to the derivative of gamma with respect to the passage of time #####
            #####################################################################################

            #######################################################################################
            ##### Color can be used to maintain a gamma-hedged portfolio, #########################
            ##### as it helps anticipate the effectiveness of the hedge as time passes ############
            ##### The mathematical result of the formula for color is expressed in gamma/year #####
            ##### and it is often useful to divide this by the number of days per year, ###########
            ##### in order to arrive at the change in gamma per day ###############################
            #######################################################################################

            ##############################################################################
            ##### This use is fairly accurate, ###########################################
            ##### when the number of days remaining until option expiration is large #####
            ##### When an option nears expiration, color itself may change quickly, ######
            ##### rendering full day estimates of gamma change inaccurate ################
            ##############################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return ((-norm.pdf(d1))/(2*S*T*Vol*M.sqrt(T)))*(1+(((2*R*T-d2*Vol*M.sqrt(T))*d1)/(Vol*M.sqrt(T))))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return ((-M.exp((-D[0])*T)*norm.pdf(d1))/(2*S*T*Vol*M.sqrt(T)))*(2*D[0]*T+1+(((2*(R-D[0])*T-d2*Vol*M.sqrt(T))*d1)/(Vol*M.sqrt(T))))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return ((-norm.pdf(d1))/(2*S*T*Vol*M.sqrt(T)))*(1+(((2*R*T-d2*Vol*M.sqrt(T))*d1)/(Vol*M.sqrt(T))))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def DualDelta(Type,T,S,K,Vol,R,D):

            #############################################################################
            ##### The actual probability of an option finishing in the money, ###########
            ##### It is the first derivative of option price with respect to strike #####
            ##### For most models, such as Black-Scholes Model or Heston Model, #########
            ##### the relationship between delta and dual delta is trivial ##############
            #############################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return -M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return -M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return -M.exp((-R)*T)*norm.cdf(d2)
                elif Type == 'P':
                    return M.exp((-R)*T)*norm.cdf(-d2)
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def DualGamma(Type,T,S,K,Vol,R,D):

            #########################################################################
            ##### Dual gamma to gamma is the same as dual delta to delta ############
            ##### Formally, it is the second derivative with respect to strike, #####
            ##### which means how fast dual delta changes with the strike, ##########
            #########################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (M.exp((-R)*T)*norm.pdf(d2))/(K*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (M.exp((-R)*T)*norm.pdf(d2))/(K*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C' or Type == 'P':
                    return (M.exp((-R)*T)*norm.pdf(d2))/(K*Vol*M.sqrt(T))
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        def Parity(Type,T,S,K,Vol,R,D):

            ##############################################################################
            ##### If Type == 'C', then the function returns a pair of option values, #####
            ##### whose form equals [Call Value,Put Value], ##############################
            ##### where two values are calculated with all the same conditions, ##########
            ##### in order to match the parity situation #################################
            ##############################################################################

            ##############################################################################
            ##### If Type == 'P', then the function returns a pair of option values, #####
            ##### whose form equals [Put Value,Call Value], ##############################
            ##### where two values are calculated with all the same conditions, ##########
            ##### in order to match the parity situation #################################
            ##############################################################################

            #############################################################
            ##### Notice: T is the time to maturity of the options ######
            ##### If conditions base on the type of dividends first #####
            #############################################################

            if D == [0,'None']:
                ##############################################
                ##### Without dividend verison (default) #####
                ##############################################
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return [S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2),K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1)]
                elif Type == 'P':
                    return [K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1),S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2)]
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == float and D[1] == 'Con' and len(D) == 2:
                #####################################
                ##### D as float ; Type = 'Con' #####
                #####################################
                d1 = (M.log(S/K)+((R-D[0])+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return [S*M.exp((-D[0])*T)*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2),K*M.exp((-R)*T)*norm.cdf(-d2)-S*M.exp((-D[0])*T)*norm.cdf(-d1)]
                elif Type == 'P':
                    return [K*M.exp((-R)*T)*norm.cdf(-d2)-S*M.exp((-D[0])*T)*norm.cdf(-d1),S*M.exp((-D[0])*T)*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2)]
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            elif type(D[0]) == list and len(D[0]) == 2 and D[1] == 'Dis' and len(D) == 2:
                #####################################################################
                ##### Type = 'Dis', and this is a more real model in most cases #####
                #####################################################################
                #####################################################################
                ##### D = [list,'Dis'], list = [cash dividends,stock dividends] #####
                #####################################################################
                S -= D[0][0]*M.exp((-R)*T)
                S /= (1+0.1*D[0][1])
                d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
                d2 = d1-Vol*M.sqrt(T)
                if Type == 'C':
                    return [S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2),K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1)]
                elif Type == 'P':
                    return [K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1),S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2)]
                else:
                    print('Error: Please enter the correct type of the option, C or P.')
                    return None

                ###############################################################

            else:
                print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
                return None

###############################################################################
###############################################################################

        PRICE = Price(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        DELTA = Delta(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        VEGA = Vega(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        THETA = Theta(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        GAMMA = Gamma(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        RHO = Rho(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)

        ##### The option value #####
        self.price = PRICE
        ##### The theoretical delta #####
        self.delta = DELTA
        ##### The dollar delta for practical use #####
        self.dollardelta = BasicInfo[2]*DELTA
        ##### The theoretical vega #####
        self.vega = VEGA
        ##### The one percent vega for practical use #####
        self.onepervega = 0.01*VEGA
        ##### The theoretical theta #####
        self.theta = THETA
        ##### The one day theta for practical use #####
        self.onedaytheta = THETA/TradingDays
        ##### The theoretical gamma #####
        self.gamma = GAMMA
        ##### The one percent dollar gamma for practical use #####
        self.oneperdollargamma = BasicInfo[2]*BasicInfo[2]*0.01*GAMMA
        ##### The theoretical rho #####
        self.rho = RHO
        ##### The one percent rho for practical use #####
        self.oneperrho = 0.01*RHO

        ##### The theoretical vanna #####
        self.vanna = Vanna(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The one percent vanna for practical use #####
        self.onepervanna = 0.01*Vanna(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The theoretical charm #####
        self.charm = Charm(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The one day charm for practical use #####
        self.onedaycharm = Charm(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)/TradingDays

        ##### The theoretical speed #####
        self.speed = Speed(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The one percent speed for practical use #####
        ##### This means the changes of gamma amount when the underlying stock price changes for 1 percent #####
        self.oneperspeed = 0.01*Speed(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The theoretical zomma #####
        self.zomma = Zomma(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The one percent zomma for practical use #####
        ##### This means the changes of gamma amount when the volatility changes for 1 percent #####
        self.oneperzomma = 0.01*Zomma(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The theoretical color #####
        self.color = Color(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The one day color for practical use #####
        ##### This means the changes of gamma amount when the time passes for 1 day #####
        self.onedaycolor = Color(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)/TradingDays

        ##### The theoretical dual delta #####
        self.dualdelta = DualDelta(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The absolute value of dual delta for practical use #####
        self.absdualdelta = abs(DualDelta(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend))
        ##### The theoretical dual gamma #####
        self.dualgamma = DualGamma(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)
        ##### The put-call parity #####
        ##### Return a pair of values, including a call and a put with other things being equal #####
        self.parity = Parity()


###############################################################################
###############################################################################
###############################################################################