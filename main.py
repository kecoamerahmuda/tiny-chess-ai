import sys,math
P={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000}
ND=[-21,-19,-12,-8,8,12,19,21];RD=[-10,-1,1,10];BD=[-11,-9,9,11];QD=RD+BD
IF="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
class E:
 def __init__(s):s.b,s.t=[None]*120,'w'
 def sb(s,f=IF):
  s.b=[' ']*120
  for i in range(120):
   r,c=divmod(i,10)
   if r<2 or r>9 or c<1 or c>8:s.b[i]='#'
  p=f.split();r,c=2,1
  for ch in p[0]:
   if ch=='/':r+=1;c=1
   elif ch.isdigit():
    for _ in range(int(ch)):s.b[r*10+c]='.';c+=1
   else:s.b[r*10+c]=ch;c+=1
  s.t=p[1] if len(p)>1 else 'w'
 def ev(s):
  sc=0
  for i in range(120):
   p=s.b[i]
   if p not in('.','#',' '):v=P[p.upper()];sc+=v if p.isupper() else -v
  return sc if s.t=='w' else -sc
 def gm(s):
  m=[];w=(s.t=='w')
  for q in range(120):
   p=s.b[q]
   if p in('.','#',' ') or (p.isupper()!=w):continue
   u=p.upper()
   if u=='P':
    st=-10 if w else 10
    if s.b[q+st]=='.':m.append((q,q+st))
    for c in(-1,1):
     t=q+st+c
     if s.b[t] not in('.','#',' ') and (s.b[t].isupper()!=w):m.append((q,t))
   else:
    d=ND if u=='N' else (BD if u=='B' else (RD if u=='R' else QD))
    l=1 if u in('N','K') else 8
    for dr in d:
     for k in range(1,l+1):
      t=q+dr*k;dst=s.b[t]
      if dst=='#':break
      if dst=='.':m.append((q,t))
      else:
       if dst.isupper()!=w:m.append((q,t))
       break
  return m
 def mm(s,m):
  u,v=m;o,d=s.b[u],s.b[v];s.b[v]=o;s.b[u]='.';s.t='b' if s.t=='w' else 'w'
  return o,d
 def um(s,m,u):
  a,b=m;s.b[a],s.b[b]=u;s.t='b' if s.t=='w' else 'w'
 def ab(s,d,a,b):
  if d==0:return s.ev(),None
  bm,bv=None,-math.inf;mv=s.gm()
  if not mv:return 0,None
  for m in mv:
   u=s.mm(m);v=-s.ab(d-1,-b,-a)[0];s.um(m,u)
   if v>bv:bv,bm=v,m
   a=max(a,v)
   if a>=b:break
  return bv,bm
 def sr(s,f):
  s.sb(f);_,m=s.ab(3,-math.inf,math.inf)
  if not m:return "0000"
  c1,r1=chr(96+(m[0]%10)),str(10-(m[0]//10))
  c2,r2=chr(96+(m[1]%10)),str(10-(m[1]//10))
  return f"{c1}{r1}{c2}{r2}"
if __name__=="__main__":
 e=E()
 for l in sys.stdin:
  t=l.strip().split()
  if not t:continue
  if t[0]=="uci":print("id name T4K\nid author mf\nuciok",flush=True)
  elif t[0]=="isready":print("readyok",flush=True)
  elif t[0]=="position":e.sb(" ".join(t[2:]) if t[1]=="fen" else IF)
  elif t[0]=="go":print(f"bestmove {e.sr(IF)}",flush=True)