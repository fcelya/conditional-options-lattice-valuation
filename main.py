import math

import numpy as np

def v_regression(p,vplus,vminus,r,dt):
    return (p*vplus+(1-p)*vminus)/(math.e**(r*dt))

def binomial(S,X,multiplier,frac_multiplier,t,vest,r,sigma,n):
    dt = t/n
    u = math.e**(sigma*math.sqrt(dt))
    v = math.e**(-sigma*math.sqrt(dt))
    p = (math.e**(r*dt)-v)/(u-v)

    asset_price = np.zeros((n+1,n+1))
    asset_price[0,0] = S
    for i in range(n+1):
        for j in range(i+1):
            asset_price[i,j] = S * u**(i-j) * v**(j)

    option_price = np.zeros((n+1,n+1))
    option_price[-1,:] = np.clip(asset_price[-1,:]-X,0,None)
    
    evaluation_day = int(vest/dt)
    
    if t==vest:
        frac = asset_price[-1,:]/S/multiplier
        frac[frac<frac_multiplier] = 0
        frac[frac>1] = 1
        option_price[-1,:] *= frac

    for i in range(n-1,-1,-1):
        for j in range(i+1):
            v_regr = v_regression(p,option_price[i+1,j],option_price[i+1,j+1],r,dt)
            if i > evaluation_day:
                option_price[i,j] = max(v_regr, asset_price[i,j]-X, 0)
            elif i == evaluation_day:
                frac = asset_price[i,j]/S/multiplier
                if frac<frac_multiplier:
                    frac=0
                elif frac>1:
                    frac=1
                option_price[i,j] = max(v_regr, asset_price[i,j]-X, 0)*frac
            else:
                option_price[i,j]=max(v_regr,0)

    return option_price[0,0]


if __name__ == '__main__':
    sigma_refs = { # 180 day mean implied volatility https://www.alphaquery.com/stock/NDAQ/volatility-option-statistics/180-day/iv-mean
        'Visa': (.2110,559.62*10e9),
        'Mastercard': (.2106,471.73*10e9),
        'Block': (.4922,44.67*10e9),
        'Equifax': (.2854,33.67*10e9),
        'Paypal':(.3794,83.21*10e9),
        'Nasdaq':(.2221,43.33*10e9),
    }
    vol = sum(sigma_refs[k][0]*sigma_refs[k][1] for k in sigma_refs.keys())/sum(sigma_refs[k][1] for k in sigma_refs.keys())
    # vol = sum(sigma_refs[k][0] for k in sigma_refs.keys())/len(sigma_refs.keys())
    args = {
        'S':166,
        'X':1,
        'multiplier':5.92,#3.946666,
        'frac_multiplier':1,
        't':2,
        'vest':2,
        'r':.02277,
        'sigma':vol,#.212,
        'n':10*365*2,
    }
    print(vol,binomial(**args))
    
    # combinations = list(itertools.product(S,X,multiplier,frac_multiplier,t,vest,r,sigma,n))
    # print(vol)
    # for c in combinations:
    #     res = binomial(*c)
    #     print(f"Stock price: {c[0]} €\nMultiplier: {c[2]:.2f}\nFractional multiplier: {c[3]*100} %\n--Option price: {res:.4f} €\n\n")