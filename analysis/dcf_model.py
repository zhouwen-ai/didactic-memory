FX=6.78; ADS=1474e6; CASH=456.4; DEBT=4.8; OTHER_NC=96.4  # bn RMB
MC_USD=112.306; PX=78.90

def dcf(fcf0,r,g1,g2,gt,n1=5,n2=5):
    pv=0; f=fcf0
    for i in range(1,n1+1):
        f*= (1+g1); pv+= f/(1+r)**i
    for i in range(n1+1,n1+n2+1):
        f*= (1+g2); pv+= f/(1+r)**i
    tv=f*(1+gt)/(r-gt); pv+= tv/(1+r)**(n1+n2)
    return pv

def per_ads(op_ev, cash=CASH):
    eq=op_ev+cash-DEBT
    return eq, eq/FX*1e9/ADS

print("=== 三档 DCF（基准 FCF 起点 = 790 亿元，已按现金实际累积速度扣除资本开支）===")
for name,(f0,r,g1,g2,gt) in {
 "悲观 (FCF 600亿, r=15%, 2%/1%/0%)":(60,.15,.02,.01,.00),
 "基准 (FCF 790亿, r=13%, 6%/3%/2%)":(79,.13,.06,.03,.02),
 "乐观 (FCF 1120亿报表口径, r=12%, 8%/4%/2.5%)":(112,.12,.08,.04,.025),
}.items():
    ev=dcf(f0,r,g1,g2,gt); eq,ps=per_ads(ev)
    print(f"{name:46s} 经营EV {ev:7.1f}亿  股权 {eq:7.1f}亿  = US${ps:6.1f}/ADS  ({ps/PX-1:+.0%})")

print("\n=== 基准 FCF 790 亿的敏感性：每 ADS 美元 ===")
print(f"{'':10s}"+"".join(f"gT={g:.1%}".rjust(12) for g in (.00,.01,.02,.03)))
for r in (.11,.12,.13,.14,.15):
    row=f"r={r:.0%}".ljust(10)
    for gt in (.00,.01,.02,.03):
        ev=dcf(79,r,.06,.03,gt); _,ps=per_ads(ev)
        row+=f"${ps:,.0f}".rjust(12)
    print(row)

print("\n=== 反推：当前股价 US$78.90 隐含了什么？（r=13%, FCF0=790亿, 永续增长 g）===")
MC_RMB=MC_USD*FX
net_cash=CASH-DEBT
for credit,label in [(1.0,"100% 计入现金"),(0.5,"50% 计入现金"),(0.0,"完全不计现金")]:
    biz = MC_RMB - net_cash*credit
    # biz = 79*(1+g)/(0.13-g)  ->  solve
    g = (0.13*biz - 79)/(biz+79)
    print(f"{label:16s} 市场为主业付 {biz:7.1f}亿元  →  隐含永续增长 g = {g:+.1%}")
