#!/usr/bin/env bash

VAR="esame_rocco"

echo -e "\n=== setup.sh ===

Buongiorno! 

Questo script:
  * crea la subdirectory
    $PWD/$VAR

  * e sposta al suo interno i seguenti file
    start_script.sh 
    plot_stars.py
    colors.txt

Questo script inoltre: 
  * modifica i permessi di esecuzione dei file  start_script.sh  e  plot_stars.py  in modo da renderli eseguibili dall'utente,
  * modifica il PYTHONPATH ed il PATH di sistema in modo da rendere eseguibile l'applicazione nel suo complesso con un comando (solo in questo terminale).

Premere un tasto qualsiasi per continuare, oppure ^C per uscire: \n"

read -rsn1

chmod u+x start_script.sh plot_stars.py
mkdir $VAR
mv start_script.sh plot_stars.py colors.txt $VAR
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$PWD/$VAR"
PATH=$PATH:$PWD/$VAR

echo -e "Lo script ha terminato le operazioni.

Per eseguire l'applicazione fare partire da terminale nella subdirectory appena creata il comando
       start_script.sh\n"
