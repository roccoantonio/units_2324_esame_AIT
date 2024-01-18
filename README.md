# Esame AIT
In questo repository sono presenti i file per l'esame di Abilità Informatiche e Telematiche tenuto presso l'Università degli Studi di Trieste dalle proff.sse Valentini e Bertocco.

## Contenuti

### setup.sh
Script di setup che *deve* essere lanciata con il comando
```
source setup.sh
```
Lo script sposta i file dalla `$PWD` in cui è lanciato nella subdirectory  `esame_rocco/`, rende eseguibili i file di script `start_script.sh` e `plot_stars.py` e imposta le variabili di sistema `PATH` e `PYTHONPATH`.

### start_script.sh
Lo script viene lanciato dalla subdirectory creata precedentemente. Dopo il lancio lo script scarica i file necessari per l'esecuzione dello script python dopodiché lancia lo stesso.

### plot_stars.py
Lo script produce i plot richiesti dalla consegna. Oltre a mostrare i plot sullo schermo durante l'esecuzione ne salva i contenuti in file separati nella directory da cui viene lanciato.

### colors.txt
File contenente valori RGB dei colori utilizzati per produrre lo scatter plot iniziale.
