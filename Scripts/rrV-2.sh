DONE=false
until $DONE
do
  read line || DONE=true
  if  [ "$line" = "ty1" ] || [ "$line" = "ty2" ] || [ "$line" = "ty3" ] || [ "$line" = "ty4" ] || [ "$line" = "ty5" ];
  then
    espeak thankyou;
  elif [ "$line" = "no1" ] || [ "$line" = "no2" ] || [ "$line" = "no3" ] || [ "$line" = "no4" ] || [ "$line" = "no5" ];
  then
    espeak no ;
  elif [ "$line" = "yes1" ] || [ "$line" = "yes2" ] || [ "$line" = "yes3" ] || [ "$line" = "yes4" ] || [ "$line" = "yes5" ];
  then
    espeak yes ;
  elif [ "$line" = "pl1" ] || [ "$line" = "pl2" ] || [ "$line" = "pl3" ] || [ "$line" = "pl4" ] || [ "$line" = "pl5" ];
  then
    espeak please ;
  else
    espeak please__contact__administrator ;
  fi
done </home/freestyler/final.txt
