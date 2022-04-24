# countMeDown

Das hier ist ein kleines Commandline-Tool in Python3, das einen Countdown in eine Textdatei schreibt. Das ist nützlich für Streams, um anzuzeigen, wie lange noch Pause oder wann der geplante Beginn sein wird, da OBS das nicht direkt unterstützt, aber eine Funktion hat, um Inhalte aus Textdateien direkt in den Stream zu tackern. 

## Wie? 
Im einfachsten Falle `countMeDown.py 20` für 20 Sekunden. Das landet dann im selben Verzeichnis in einer Datei mit Namen `time.txt`.

Sämtliche definierte Parameter zum starten gibt es mit `countMeDown.py --help`, was dann etwa so aussieht.

```
usage: countMeDown.py [-h] [-f FILE] [-s STEP] [-p PREFIX] [-e ENDING] [--print] [--target_time] time_in

OBS kann Textinputs aus Dateien lesen und direkt rendern. Hiermit können wir Countdowns in Textdateien schreiben, um sie direkt in den
Stream zu kleben.

positional arguments:
  time_in               Zeit für den Countdown. Entweder in Sekunden, Minuten:Sekunden oder als Zieluhrzeit, dann muss --target-time mit
                        angegeben werden.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Pfad zur Datei, die von OBS gelesen wird.
  -s STEP, --step STEP  Anzahl Sekunden, bevor neu geschrieben wird.
  -p PREFIX, --prefix PREFIX
                        Text, der vor der Restzeit fest angezeigt wird.
  -e ENDING, --ending ENDING
                        Text, der nach dem Ablauf des Timers geschrieben wird.
  --print               schreibe die Ausgabe zusätzlich in die Konsole
  --target_time         Wenn gesetzt wird die Eingabe als Ziel-Uhrzeit und nicht als Zeitdauer gelesen. Uhrzeit in 24-Stunden-Format mit
                        oder ohne Sekunden, Doppelpunkt als Trennzeichen.

Damit lässt sich schon bisschen was anstellen:

- Die angegebene Zeit muss nicht in Sekunden umgerechnet werden, sondern kann auch Minuten und Stunden beinhalten. Dann so `Stunden:Minuten:Sekunden`
- Für so etwas wie "wir machen jetzt Pause bis um 18:00" gibt es **`--target_time`**: Wenn das Flag gesetzt wird, dann ist der Countdown nicht für 18 Minuten flat, sondern bis das nächste Mal 18:00 Uhr sein wird. 
- für längere Countdowns ist es vielleicht sinnig, nicht jede Sekunde neu zu setzen. Das geht mit **`--step`**. Step nimmt allerdings nur Sekundenwerte an. Hier gibts keine Option Minuten oder Stunden anzugeben.
- Während es natürlich möglich ist, den Text aus diesem Tool von statischen Texten in OBS einzurahmen, um einen Kontext zu geben, wann der Timer endet, kann es bequemer sein, das direkt in der Ausgabe zu haben. Einen Text vor die Restzeit gibt es mit **`--prefix`**.
- Zusätzlich gibt es noch **`--ending`**, was ebenso einen Text annimmt, dieser wird statt der Restzeit angezeigt, wenn der Timer eigentlich zu Ende ist. 
- Wer die Datei an einem anderen Ort speichern möchte, kann mit **`--file`** den Pfad angeben.
- um zum Testen zu sehen, was ausgegeben wird, gibt es noch **`--print`**: hier wird die Ausgabe zusätzlich noch in der Konsole ausgegeben
