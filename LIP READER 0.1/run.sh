#!/bin/bash
python eigenface.py  /home/hduser/MAIN\ PROJECT/CODE/main/testdata/ /home/hduser/MAIN\ PROJECT/CODE/main/out/ ;
pyssim out/mean.png  "eigenmean/*" | tee /home/hduser/score.txt;
python sort.py ;
./rr.sh ;
