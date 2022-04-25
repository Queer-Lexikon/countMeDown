# countMeDown

Das hier ist ein kleines Commandline-Tool in Python3, das einen Countdown in eine Textdatei schreibt. Das ist nützlich für Streams, um anzuzeigen, wie lange noch Pause oder wann der geplante Beginn sein wird, da OBS das nicht direkt unterstützt, aber eine Funktion hat, um Inhalte aus Textdateien direkt in den Stream zu tackern. 

Das alles ist inspirierend von Snaz, was (a) nicht mehr weiterentwickelt wird (SÄD), (b) nicht auf macOS läuft (SÄD) und (c) eine GUI hat (Neid!).

countMeDown kommt komplett ohne Abhängigkeiten (außer Python).



## Wie? 
Im einfachsten Falle so:

```bash
$ python3 countMeDown.py 30
30 Sekunden Countdown in ./time.txt. Ab jetzt.
```
Die entstehende Textdatei (standardmäßig time.txt) muss dann noch OBS als Textquelle bekannt gemacht werden. 

Sämtliche definierte Parameter zum starten gibt es mit `countMeDown.py --help`, was dann etwa so aussieht.

```
usage: countMeDown.py [-h] [-f FILE] [-s STEP] [-p PREFIX] [-e ENDING] [--print]
                      [--until]
                      time_in

OBS kann Textinputs aus Dateien lesen und direkt rendern. Hiermit können wir Countdowns
in Textdateien schreiben, um sie direkt in den Stream zu kleben.

positional arguments:
  time_in               Zeit für den Countdown. Entweder in Sekunden, Minuten:Sekunden
                        oder als Zieluhrzeit, dann muss --until mit angegeben werden.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Pfad zur Datei, die von OBS gelesen wird.
  -s STEP, --step STEP  Anzahl Sekunden, bevor neu geschrieben wird.
  -p PREFIX, --prefix PREFIX
                        Text, der vor der Restzeit fest angezeigt wird.
  -e ENDING, --ending ENDING
                        Text, der nach dem Ablauf des Timers geschrieben wird.
  --print               schreibe die Ausgabe zusätzlich in die Konsole
  --until               Wenn gesetzt wird die Eingabe als Ziel-Uhrzeit und nicht als
                        Zeitdauer gelesen. Uhrzeit in 24-Stunden-Format mit oder ohne
                        Sekunden, Doppelpunkt als Trennzeichen.

```

Damit lässt sich schon bisschen was anstellen:

- Die angegebene Zeit muss nicht in Sekunden umgerechnet werden, sondern kann auch Minuten und Stunden beinhalten. Dann so `Stunden:Minuten:Sekunden`
- Für so etwas wie "wir machen jetzt Pause bis um 18:00" gibt es **`--until`**: Wenn das Flag gesetzt wird, dann ist der Countdown nicht für 18 Minuten flat, sondern bis das nächste Mal 18:00 Uhr sein wird. 
- für längere Countdowns ist es vielleicht sinnig, nicht jede Sekunde neu zu setzen. Das geht mit **`--step`**. Step nimmt allerdings nur Sekundenwerte an. Hier gibts keine Option Minuten oder Stunden anzugeben.
- Während es natürlich möglich ist, den Text aus diesem Tool von statischen Texten in OBS einzurahmen, um einen Kontext zu geben, wann der Timer endet, kann es bequemer sein, das direkt in der Ausgabe zu haben. Einen Text vor die Restzeit gibt es mit **`--prefix`**. Etwa so: `$ countMeDown.py 30 --prefix "Stream startet in: "`.
- Zusätzlich gibt es noch **`--ending`**, was ebenso einen Text annimmt, dieser wird statt der Restzeit angezeigt, wenn der Timer eigentlich zu Ende ist. Etwa so: `$ countMeDown.py 10:00 --ending "gleich"`. 
- Wer die Datei an einem anderen Ort speichern möchte, kann mit **`--file`** den Pfad angeben. Etwa so: `$ countMeDown.py 120 --file "C:\\countdown.txt"`.
- um zum Testen zu sehen, was ausgegeben wird, gibt es noch **`--print`**: hier wird die Ausgabe zusätzlich noch in der Konsole ausgegeben

## Aber?

Teile dieses Programms basieren auf Python Timedeltas. Die Doku warnt: 

> Note that for very large time intervals (greater than 270 years on most platforms) this method will lose microsecond accuracy.

Das gilt auch hier.

## Läuft gut?

In der aktuellen Version wird _sched_ aus der Python-Standardbibliothek zum Planen der Dateizugriffe benutzt. Damit ergibt sich ein Overhead von wenigen hundertstel Sekunden bei 10 Minuten Countdown: 

```bash
$ time python3 countMeDown.py 10:00
python3 countMeDown.py 10:00  0,17s user 0,41s system 0% cpu 10:00,07 total
```
