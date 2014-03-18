#!/bin/bash
python eigenface.py  /home/freestyler/mainpro/testdata/ /home/freestyler/mainpro/final/out/ ;
cp /home/freestyler/mainpro/final/out/mean.png  /home/freestyler/mainpro/CURRENT/FINAL_EIGEN_CODE/ ;
pyssim /home/freestyler/mainpro/CURRENT/FINAL_EIGEN_CODE/mean.png  "/home/freestyler/mainpro/CURRENT/FINAL_EIGEN_CODE/eigen_face/*" | tee /home/freestyler/score.txt;
python ttt.py;
./rr.sh;
