#!/usr/bin/env python3
import argparse
import datetime
import sched
import sys
import time
import types


def format_time(secs: int) -> str:
    minutes, seconds = divmod(secs, 60)
    if minutes > 59:
        hours, minutes = divmod(minutes, 60)
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"


def get_seconds_until_time(target_time: str) -> int:
    colon_count = target_time.count(":")
    if colon_count == 0:
        raise ValueError
    if target_time.count(":") == 1:
        target_time = target_time + ":00"

    hour, minute, second = tuple(map(int, target_time.split(":")))

    now = datetime.datetime.now()
    target = now.replace(hour=hour, minute=minute, second=second)

    if target < now:
        target = target + datetime.timedelta(days=1)

    delta = target - now
    return int(delta.total_seconds())


def get_seconds_from_mixed_format(mixed: str) -> int:
    seconds: int = 0
    colon_count = mixed.count(":")
    if colon_count == 0:
        seconds = int(mixed)

    else:
        units = [unit for unit in map(int, mixed.split(":"))]
        factor: int = 1
        s: int = 0
        for unit in reversed(units):
            s += factor * unit
            factor = factor * 60
        seconds = s
    return seconds


def write_to_file(line: str, filepath: str, verbose: bool):
    with open(filepath, mode="w") as fp:
        fp.write(line)
    if verbose:
        print(line)


def count_me_down(
    seconds: int, prefix: str, ending: str, step: int, filepath: str, verbose: bool
):
    for moment in range(0, seconds + step, step):
        if seconds < moment:
            break
        line = f"{prefix} {format_time(seconds-moment)}"
        s.enter(moment, 1, write_to_file, argument=(line, filepath, verbose))

    s.run()
    write_to_file(ending, filepath, verbose)


def get_args_interactive() -> types.SimpleNamespace:
    args = types.SimpleNamespace()
    print("Ohne Parameter gestartet. Wir machen das jetzt interaktiv.")
    until = input(
        'Möchtest du eine Ziel-Uhrzeit angeben? Standard ist eine Zeitspanne. ("Ja" oder "J" für Uhrzeit.)\n > '
    )
    if until.lower().startswith("j"):
        args.until = True
        time_in = ""
        while True:
            time_in = input(
                "Wie viel Uhr soll der Countdown enden? (24-Stunden-Format, Doppelpunkt als Trennzeichen mit Stunden und Minuten, Sekunden optional. Beispiel: 13:05)\n > "
            )
            if time_in.count(":") < 1:
                print(f"{time_in} hat keinen Doppelpunkt, das kann nicht stimmen.")
            else:
                break
        args.time_in = time_in

    else:
        args.until = False
        time_in = input(
            "Wie lange soll der Countdown andeuern? Entweder in Sekunden oder Minuten:Sekunden oder Stunden:Minuten:Sekunden, Standard: 60 Sekunden, enter ohne Eingabe zum übernehmen. \n > "
        )
        if len(time_in) == 0:
            args.time_in = "60"
        args.time_in = time_in

    file = input(
        "In welche Datei soll geschrieben werden? Standard: ./time.txt, zum übernehmen direkt enter ohne Eingabe\n > "
    )
    if len(file) == 0:
        args.file = "./time.txt"
    else:
        args.file = file

    step_unfinished = True
    step = 1
    while step_unfinished:
        step_unfinished = False
        step = input(
            "Nach wie vielen Sekunden soll aktualisiert werden? Standard ist 1, mit enter übernehmen. Sonst als Ganzzahl eingeben\n > "
        )
        if len(step) == 0:
            step = 1
        else:
            try:
                int(step)
                step_unfinished = False
            except ValueError:
                print("Das scheint keine Zahl zu sein.")
                step_unfinished = True
    args.step = abs(int(step))

    verbose = input(
        'Möchtest du zusätzlich zur Datei Ausgabe hier im Terminal? ("Ja" oder "J". Standard ist Nein.) \n > '
    )
    if verbose.lower().startswith("j"):
        args.print = True
    else:
        args.print = False

    ending = input(
        "Was soll statt 00:00 am Ende angezeigt werden? Standard ist nichts. \n > "
    )
    args.ending = ending

    prefix = input(
        "Was soll vor der Restzeitanzeige angezeigt werden? Standard ist nichts. \n > "
    )
    args.prefix = prefix

    return args


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="OBS kann Textinputs aus Dateien lesen und direkt rendern. Hiermit können wir Countdowns in Textdateien schreiben, um sie direkt in den Stream zu kleben."
    )
    parser.add_argument(
        "-f",
        "--file",
        default="./time.txt",
        help="Pfad zur Datei, die von OBS gelesen wird.",
    )
    parser.add_argument(
        "-s",
        "--step",
        type=int,
        default=1,
        help="Anzahl Sekunden, bevor neu geschrieben wird.",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="",
        help="Text, der vor der Restzeit fest angezeigt wird.",
    )
    parser.add_argument(
        "-e",
        "--ending",
        type=str,
        default="",
        help="Text, der nach dem Ablauf des Timers geschrieben wird.",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        default=False,
        help="schreibe die Ausgabe zusätzlich in die Konsole",
    )
    parser.add_argument(
        "time_in",
        help="Zeit für den Countdown. Entweder in Sekunden, Minuten:Sekunden oder als Zieluhrzeit, dann muss --until mit angegeben werden.",
    )
    parser.add_argument(
        "--until",
        action="store_true",
        help="Wenn gesetzt wird die Eingabe als Ziel-Uhrzeit und nicht als Zeitdauer gelesen. Uhrzeit in 24-Stunden-Format mit oder ohne Sekunden, Doppelpunkt als Trennzeichen.",
    )

    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        args = get_args_interactive()

    seconds = get_seconds_from_mixed_format(args.time_in)
    if args.until:
        seconds = get_seconds_until_time(args.time_in)
    step = abs(args.step)

    print(f"{seconds} Sekunden Countdown in {args.file}. Ab jetzt.")

    s = sched.scheduler(time.time, time.sleep)
    count_me_down(
        seconds=seconds,
        prefix=args.prefix,
        ending=args.ending,
        step=step,
        filepath=args.file,
        verbose=args.print,
    )
