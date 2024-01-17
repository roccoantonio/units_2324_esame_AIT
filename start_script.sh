#!/usr/bin/env bash

VAR=https://github.com/MilenaValentini/TRM_Dati/raw/main/Nemo_6670.dat

echo -e "\n=== start_script.sh ===

Buongiorno!

Questo script:

  * scarica il file  $VAR
    nella presente directory

  * e lancia plot_stars.py

Premere un tasto qualsiasi per continuare, oppure ^C per uscire: \n"

read -rsn1

echo -e "Sto scaricando il file:\n"

wget -nv  $VAR

echo -e "\nOra avvio lo script python."

python plot_stars.py Nemo_6670.dat

echo -e "\nTutti i plot sono stati salvati in file separati in questa directory.\n\nLo script ha terminato tutte le operazioni."
