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
    args = {
        'S':166,
        'X':1,
        'multiplier':5.92,
        'frac_multiplier':1,
        't':7.5,
        'vest':2.5,
        'r':0.04,
        # 'r':.02448,
        'sigma':.212,
        'n':5670,
    }
    print(binomial(**args))
    # print(binomial(156,1,9.238507156,.5,7.5,2.5,.02881,.211995,9450))
    # S = 156
    # X = 1
    # multiplier=9.238507156
    # frac_multiplier=.5
    # t=7.5
    # vest=2.5
    # r=.02881
    # sigma_refs = { # 180 day mean implied volatility
    #     'Visa': (.1775,508.27*10e9),
    #     'Mastercard': (.1848,431.85*10e9),
    #     'Block': (.5126,41.14*10e9),
    #     'Equifax': (.2999,29.98*10e9),
    #     'Paypal':(.4225,70.08*10e9),
    #     'Nasdaq':(.1973,32.49*10e9),
    # }
    # # # sigma_refs = { # 30 day historical volatility
    # # #     'Visa': (.1377,508.27*10e9),
    # # #     'Mastercard': (.1234,431.85*10e9),
    # # #     # 'Block': (.5126,41.14*10e9),
    # # #     # 'Equifax': (.2999,29.98*10e9),
    # # #     # 'Paypal':(.4225,70.08*10e9),
    # # #     'Nasdaq':(.1495,32.49*10e9),
    # # # }
    # vol = sum(sigma_refs[k][0]*sigma_refs[k][1] for k in sigma_refs.keys())/sum(sigma_refs[k][1] for k in sigma_refs.keys())
    # sigma = vol
    # print(sigma)
    # sigma=.2
    # n=1000
    # a = binomial(S,X,multiplier,frac_multiplier,t,vest,r,sigma,n)
    # print(a)
    # S=(324.715,156,493.43)
    # X=(1,)
    # multiplier=(4.438376,9.238507156, 2.920793675)
    # frac_multiplier=(.5,)
    # t=(7.5,)
    # vest=(2.5,)
    # r=(.02881,) # 10Y Spanish bond
    # # vol = (.4081+.5079+.1855+.1883+.2930+.2156)/6 # 180 day mean implied volatility of Paypal, Square, Visa, Mastercard, Equifax y Nasdaq
    # sigma=(vol,)
    # n=(int(7.5*252*3),)

    # combinations = list(itertools.product(S,X,multiplier,frac_multiplier,t,vest,r,sigma,n))
    # print(vol)
    # for c in combinations:
    #     res = binomial(*c)
    #     print(f"Stock price: {c[0]} €\nMultiplier: {c[2]:.2f}\nFractional multiplier: {c[3]*100} %\n--Option price: {res:.4f} €\n\n")