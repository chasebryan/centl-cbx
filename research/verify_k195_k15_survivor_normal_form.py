#!/usr/bin/env python3
"""Verify the exact two-sector h169 k15 survivor normal form."""
from collections import deque
import argparse, json, math

HJ=frozenset({1,2,4,8})
H3=frozenset({1,4,7,13})
TARGET_I=11
TARGET_II=14
EXPECTED={frozenset({1}),frozenset({1,4}),HJ,H3}

def transition(M,c,r):
 local={1,r,r*r%15}
 return frozenset(x*y%15 for x in M for y in local),c*r%15

def closure():
 units=[r for r in range(1,15) if math.gcd(r,15)==1]
 start=(frozenset({1}),1);seen={start};q=deque([start])
 while q:
  M,c=q.popleft()
  for r in units:
   z=transition(M,c,r)
   if z not in seen:seen.add(z);q.append(z)
 return seen

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--json',action='store_true');args=ap.parse_args()
 seen=closure();assert len(seen)==41
 misses={M for M,c in seen if c==1 and TARGET_I not in M and TARGET_II not in M}
 assert misses==EXPECTED
 assert HJ&H3=={1,4}
 assert TARGET_I not in HJ and TARGET_II not in HJ
 assert TARGET_I not in H3 and TARGET_II not in H3
 assert all(M<=HJ or M<=H3 for M in misses)
 # subgroup closure and character interpretation
 for H in (HJ,H3):
  assert 1 in H
  assert all((a*b)%15 in H for a in H for b in H)
 assert all((r%3)==1 for r in H3)
 # Jacobi-positive units mod15 are exactly HJ.
 def leg(a,p):
  x=pow(a%p,(p-1)//2,p);return 1 if x==1 else -1 if x==p-1 else 0
 jac={r for r in range(1,15) if math.gcd(r,15)==1 and leg(r,3)*leg(r,5)==1}
 assert jac==set(HJ)
 # Certified anchor support mixes the two sectors and therefore is unsafe.
 anchor_residues={2,97%15,377909467555760167%15}
 assert 2 in HJ and 2 not in H3
 assert 7 in H3 and 7 not in HJ
 assert not anchor_residues<=HJ and not anchor_residues<=H3
 out={'analysis':'k195-k15-survivor-normal-form-v1','closure_states':len(seen),
      'miss_masks':[sorted(M) for M in sorted(misses,key=lambda x:(len(x),sorted(x)))],
      'sectors':{'J15':sorted(HJ),'ONE3':sorted(H3),'intersection':[1,4]},
      'theorem':'k15 miss iff all prime factors of C15 lie in J15 or all lie in ONE3',
      'anchor_prediction':'hit','failures':0}
 print(json.dumps(out,indent=2,sort_keys=True) if args.json else out);return 0
if __name__=='__main__':raise SystemExit(main())
