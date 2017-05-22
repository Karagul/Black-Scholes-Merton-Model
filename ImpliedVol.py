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
This function computes the implied volatility of options based on the assumption of Black-Scholes-Merton model.
Under Black-Scholes-Merton model, there is a closed-form solution when implementing Newton-Raphson Method to calculate implied volatitlity.
About dividend: the default setting is no dividend included.
    User can add dividend calculation with known dividend payment in the holding period.
    Type1: D = [rate,'Con'], which is the continuous dividend payment over certain period with a constant payment rate.
    Type2: D = [[cash,stock],'Dis'], which can include a one-time cash or stock dividends payment over certain period.
In addition, remember to provide the function with an initial value of implied volatility.
There are many detailed explanations in this code, which may help users run this module smoothly.
'''

####################################################################################################

def ImpliedVol(Type,T,S,K,R,VolOri,IniPrice,D = [0,'None'],Iteration = 100,Tolerance = 1e-10):

    import math as M
    from scipy.stats import norm

    ############################################################################################
    ##### There is a closed-form solution for implementing Newton-Raphson Method ###############
    ##### in Black-Schole-Merton Model, but I am concerning about the speed of calculation #####
    ############################################################################################

###############################################################################
###############################################################################

    def PriceVega(Type,T,S,K,Vol,R,D):

        if D == [0,'None']:
            ##############################################
            ##### Without dividend verison (default) #####
            ##############################################
            d1 = (M.log(S/K)+((R)+(Vol*Vol/2))*T)/(Vol*M.sqrt(T))
            d2 = d1-Vol*M.sqrt(T)
            if Type == 'C':
                return [S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2),S*M.sqrt(T)*norm.pdf(d1)]
            elif Type == 'P':
                return [K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1),S*M.sqrt(T)*norm.pdf(d1)]
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
                return [S*M.exp((-D[0])*T)*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2),S*M.exp((-D[0])*T)*M.sqrt(T)*norm.pdf(d1)]
            elif Type == 'P':
                return [K*M.exp((-R)*T)*norm.cdf(-d2)-S*M.exp((-D[0])*T)*norm.cdf(-d1),S*M.exp((-D[0])*T)*M.sqrt(T)*norm.pdf(d1)]
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
                return [S*norm.cdf(d1)-K*M.exp((-R)*T)*norm.cdf(d2),S*M.sqrt(T)*norm.pdf(d1)]
            elif Type == 'P':
                return [K*M.exp((-R)*T)*norm.cdf(-d2)-S*norm.cdf(-d1),S*M.sqrt(T)*norm.pdf(d1)]
            else:
                print('Error: Please enter the correct type of the option, C or P.')
                return None

            ###############################################################

        else:
            print('Error: Please input a valid format for dividends. Check the notes to acquire further information.')
            return None

###############################################################################
###############################################################################

    IterPrice,IterVega = PriceVega(Type,T,S,K,VolOri,R,D)
    ImpVol = VolOri

    count = 0
    while count < Iteration:
        while abs(IterPrice-IniPrice) >= Tolerance:
            ImpVol = ImpVol-((IterPrice-IniPrice)/IterVega)
            IterPrice,IterVega = PriceVega(Type,T,S,K,ImpVol,R,D)
            count += 1
        break
    return ImpVol

###############################################################################
###############################################################################
###############################################################################

##### This is an example to use this module #####
import sys
##### Remember to change the file path #####
sys.path.append(r'C:\Users\0010012\Desktop\Kiwi Files')
import AnnualizedTime
############################################

AT = AnnualizedTime.AnnTime('US','20170320213000','20170321213000','20170417213000')
print(ImpliedVol('C',AT.ttm,1230,1235,0.01,0.05,5.70))
#################################################
