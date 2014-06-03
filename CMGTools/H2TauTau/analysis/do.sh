## for sample generation

for a in data
#for a in tH_YtMinus1
#for a in WZ ZZ tt1l tt2l tH_YtMinus1 TTH TTW TTZ
#for a in  WZ ZZ tt1l tt2l tH_YtMinus1
#for a in  tH_YtMinus1
  do
  python sync.py --mode antiE --region f3 --phys $a &
  python sync.py --mode antiMu --region f3 --phys $a &
  python sync.py --mode antiEMu --region f3 --phys $a &
  python sync.py --mode signal --region f3 --phys $a &

  python sync.py --mode antiE --region f12 --phys $a &
  python sync.py --mode antiMu --region f12 --phys $a &
  python sync.py --mode antiEMu --region f12 --phys $a &
  python sync.py --mode signal --region f12 --phys $a &
done

###sleep 1200
###
###for a in data WZ ZZ tt1l tt2l tH_YtMinus1 TTH TTW TTZ
####for a in tH_YtMinus1
####for a in TTH TTW TTZ
####for a in WZ
####for a in tH_YtMinus1
####for a in data WZ ZZ tt1l tt2l
####for a in data
####for a in tH_YtMinus1
####for a in tH_YtMinus1
####for a in data #tt1l tt2l
####for a in WW
###  do
###  python sync.py --mode antiE --region f3 --phys $a &
###  python sync.py --mode antiMu --region f3 --phys $a &
###  python sync.py --mode antiEMu --region f3 --phys $a &
###  python sync.py --mode signal --region f3 --phys $a &
###
####  python sync.py --mode antiE --region f12 --phys $a &
####  python sync.py --mode antiMu --region f12 --phys $a &
####  python sync.py --mode antiEMu --region f12 --phys $a &
####  python sync.py --mode signal --region f12 --phys $a &
###done
###
###
###
####
####python genTree.py --mode signal --region f3
####python genTree.py --mode antiMu --region f3
####python genTree.py --mode antiE --region f3
####python genTree.py --mode antiEMu --region f3
####
####
##### for W+jet generation
####python wjet_control.py --mode muon
####python wjet_control.py --mode electron
####
####
##### for fake rate with 2D parameterization
####python func_training.py --process data --channel muon
####python func_training.py --process WZ --channel muon
####python func_training.py --process ZZ --channel muon
####python func_training.py --process data --channel electron
####python func_training.py --process WZ --channel electron
####python func_training.py --process ZZ --channel electron
####python func_training.py --process tt --channel muon
####python func_training.py --process tt --channel electron
####
####
##### for generating histogram
####python genHisto.py --kNN 25
####python genHisto.py --kNN 50
####python genHisto.py --kNN 100
###
#### for plotting
####python draw.py --mode kNN --kNN 100
####python draw.py --mode kNN --kNN 50
####python draw.py --mode kNN --kNN 25