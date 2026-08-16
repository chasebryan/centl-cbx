#!/usr/bin/env python3
"""Exact certificate for the k195 corridor anchor whose first signed-box hit is k15."""
import argparse, collections, json, math

S=59176
T0=7423185617863
DT=11799129838887
T=698232730531594975
P=586515493646539779169
U64=1<<64
Q=144525734917121
C3=146628873411634944793
C7Q=73314436705817472397

LUCAS={
 P:(17,{2:5,3:3,7:1,11:1,61:1,Q:1}),
 C3:(10,{2:3,3:3,7:1,11:1,61:1,Q:1}),
 C7Q:(5,{2:2,3:3,7:1,11:1,61:1,Q:1}),
}

F={
 3:{C3:1},
 7:{2:1,C7Q:1},
 11:{3:1,5:1,9775258227442329653:1},
 15:{2:2,97:1,377909467555760167:1},
 19:{23:1,47:1,49891:1,2718764527607:1},
 23:{2:1,3:1,13:1,29:1,127:1,510414703076627:1},
 27:{7:1,17:1,31:1,39747593768401991:1},
 31:{2:5,5:2,41:1,4470392482062041:1},
 47:{2:2,3:1,37:1,661:1,499614539162731:1},
 195:{7:1,37:2,41:2,67:1,277:1,490451113:1},
}

def prod(f):
 r=1
 for q,e in f.items(): r*=q**e
 return r

def mr(n):
 if n<2:return False
 for p in (2,3,5,7,11,13,17,19,23,29,31,37):
  if n%p==0:return n==p
 assert n<U64
 d=n-1;s=0
 while d%2==0:s+=1;d//=2
 for a in (2,325,9375,28178,450775,9780504,1795265022):
  if a%n==0:continue
  x=pow(a,d,n)
  if x in (1,n-1):continue
  for _ in range(s-1):
   x=x*x%n
   if x==n-1:break
  else:return False
 return True

def certify(n,cache):
 if n in cache:return cache[n]
 if n<U64:
  cache[n]=mr(n);return cache[n]
 a,fac=LUCAS[n]
 assert prod(fac)==n-1
 assert all(certify(q,cache) for q in fac)
 assert pow(a,n-1,n)==1
 assert all(math.gcd(pow(a,(n-1)//q,n)-1,n)==1 for q in fac)
 cache[n]=True;return True

def C(k):return (P+k)//4

def residues(fac,k):
 R={1%k}
 for q,e in fac.items():
  R={x*pow(q,a,k)%k for x in R for a in range(2*e+1)}
 return R

def leg(a,p):
 r=pow(a%p,(p-1)//2,p)
 return 1 if r==1 else -1 if r==p-1 else 0

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--json',action='store_true');args=ap.parse_args()
 assert T==T0+DT*S and P==169+840*T and P%840==169
 cache={};assert certify(P,cache)
 for k,fac in F.items():
  assert prod(fac)==C(k),(k,prod(fac),C(k))
  assert all(certify(q,cache) for q in fac),(k,fac)
 phases={m:T%m for m in (9,11,13,17,19,23,31,43,47)}
 assert phases=={9:7,11:2,13:2,17:6,19:16,23:15,31:7,43:39,47:0}
 # exact early misses
 assert residues(F[3],3)=={1}
 assert residues(F[7],7)=={1,2,4}
 assert residues(F[11],11)=={1,3,4,5,9}
 # Route-B D-selector support
 R={49891:1,2718764527607:1};assert prod(R)*1081==C(19)
 assert all(leg(q,19)==1 for q in R) and any(q%19!=1 for q in R)
 B={13:1,29:1,127:1,510414703076627:1};assert prod(B)*6==C(23)
 assert all(leg(q,23)==1 for q in B)
 E={17:1,31:1,39747593768401991:1};assert prod(E)*7==C(27)
 assert E[17]==E[31]==1 and 39747593768401991%27==2
 D={2:4,5:1,41:1,4470392482062041:1};assert prod(D)*10==C(31)
 assert all(leg(q,31)==1 for q in D) and 41%31==10
 J={2:1,37:1,661:1,499614539162731:1};assert prod(J)*6==C(47)
 assert all(leg(q,47)==1 for q in J)
 assert F[195][37]==2 and F[195][41]==2
 # first exact hit k15: both targets have explicit divisor witnesses
 ti=(-pow(4,-1,15))%15;tii=(-C(15))%15
 assert (ti,tii)==(11,14)
 di,dii=776,194
 assert C(15)**2%di==0 and C(15)**2%dii==0
 assert di%15==ti and dii%15==tii
 assert ti in residues(F[15],15) and tii in residues(F[15],15)
 out={'analysis':'k195-k15-ancestry-anchor-v1','s':S,'t':T,'p':P,'p_prime_certified':True,
      'phase':{f'tau{m}':r for m,r in phases.items()},
      'ancestry':['k3 MISS ONE_MOD3','k7 MISS QR7','k11 MISS tau11=2 QR11','k15 HIT I+II'],
      'k15_divisors':{'type_i':di,'type_ii':dii},
      'd_selector':{'k19':'FULL_QR','B':'QR23','E':'17*31*r(r=2 mod27)','k31':'FULL_QR,q_D=41','k47':'QR47,q_J=37'},
      'k195':{'v37':2,'v41':2},'failures':0}
 print(json.dumps(out,indent=2,sort_keys=True) if args.json else out)
 return 0
if __name__=='__main__':raise SystemExit(main())
