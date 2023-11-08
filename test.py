ge_SOL = (16/14.77)
ge_BTC = (16/14.84)
ge_MATIC = (16/14.95)


pc_SOL = 43.65
pc_BTC = 35366.67
pc_MATIC = 0.7969

pv_SOL = pc_SOL*ge_SOL
pv_BTC = pc_BTC*ge_BTC
pv_MATIC = pc_MATIC*ge_MATIC

print("SOL",pv_SOL)
print("BTC",pv_BTC)
print("MATIC",pv_MATIC)