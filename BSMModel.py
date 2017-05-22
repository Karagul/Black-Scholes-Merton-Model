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
This is the Black-Scholes-Merton model to price options.
Before running this module, users please make sure that you can execute my AnnualizedTime module normally.
Reference: https://github.com/kaiweihuang/Black-Scholes-Merton-Model/blob/master/AnnualizedTime.py
About dividend: the default setting is no dividend included.
    User can add dividend calculation with known dividend payment in the holding period.
    Type1: D = [rate,'Con'], which is the continuous dividend payment over certain period with a constant payment rate.
    Type2: D = [[cash,stock],'Dis'], which can include a one-time cash or stock dividends payment over certain period.
There are several parts in this module can be optimized.
In fact, some factors are much more crucial than others while trading options, so users can develop a faster version of this pricing model by yourself.
There are many detailed explanations in this code, which may help users run this module smoothly.
'''

####################################################################################################

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

            if Type == 'C':
                return Price('P',T,S,K,Vol,R,D)
            elif Type == 'P':
                return Price('C',T,S,K,Vol,R,D)
            else:
                print('Error: Please enter the correct type of the option, C or P.')
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
        self.parity = Parity(BasicInfo[0],BasicInfo[1],BasicInfo[2],BasicInfo[3],BasicInfo[4],BasicInfo[5],Dividend)

###############################################################################
###############################################################################
###############################################################################

'''
Once again, before running this module, users should make sure that you can execute my AnnualizedTime module normally.
Reference: https://github.com/kaiweihuang/Black-Scholes-Merton-Model/blob/master/AnnualizedTime.py
'''

##### This is an example to use this module #####
import sys
##### Remember to change the file path #####
sys.path.append(r'C:\Users\0010012\Desktop\Kiwi Files')
import AnnualizedTime
############################################
Market = 'US'
Start = '20170302223500'
Hold = '20170303233000'
End = '20170316120000'
AT = AnnualizedTime.AnnTime(Market,Start,Hold,End)

BasicInfo = ['C',AT.ttm,45,50,0.50,0.025]
OptionPricing = BSMModel(BasicInfo,AT.toltradays)
print('Option Price: {}'.format(OptionPricing.price))
print('Delta: {}'.format(OptionPricing.delta))
print('Dollar Delta: {}'.format(OptionPricing.dollardelta))
print('Vega: {}'.format(OptionPricing.vega))
print('One Percent Vega: {}'.format(OptionPricing.onepervega))
print('Theta: {}'.format(OptionPricing.theta))
print('One Day Theta: {}'.format(OptionPricing.onedaytheta))
print('Gamma: {}'.format(OptionPricing.gamma))
print('One Percent Dollar Gamma: {}'.format(OptionPricing.oneperdollargamma))
print('Rho: {}'.format(OptionPricing.rho))
print('One Percent Rho: {}'.format(OptionPricing.oneperrho))
print('Vanna: {}'.format(OptionPricing.vanna))
print('One Percent Vanna: {}'.format(OptionPricing.onepervanna))
print('Charm: {}'.format(OptionPricing.charm))
print('One Day Charm: {}'.format(OptionPricing.onedaycharm))
print('Speed: {}'.format(OptionPricing.speed))
print('One Percent Speed: {}'.format(OptionPricing.oneperspeed))
print('Zomma: {}'.format(OptionPricing.zomma))
print('One Precent Zomma: {}'.format(OptionPricing.oneperzomma))
print('Color: {}'.format(OptionPricing.color))
print('One Day Color: {}'.format(OptionPricing.onedaycolor))
print('Dual Delta: {}'.format(OptionPricing.dualdelta))
print('Absolute Value of Dual Delta: {}'.format(OptionPricing.absdualdelta))
print('Dual Gamma: {}'.format(OptionPricing.dualgamma))
print('Parity: {}'.format(OptionPricing.parity))
#################################################
