#!/bin/bash
python eigenface.py  /home/hduser/MAIN\ PROJECT/CODE/testdata/ /home/hduser/MAIN\ PROJECT/CODE/final/out/ ;
pyssim out/mean.png  "eigenmean/*" | tee /home/hduser/score.txt;
python ttt.py ;
./rr.sh ;
