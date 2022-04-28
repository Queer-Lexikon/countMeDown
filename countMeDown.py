#!/usr/bin/env python3
import argparse
import datetime
import pathlib
import sched
import signal
import sys
import time
import types
import typing


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
        target_time += ":00"

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
            factor *= 60
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


def get_input_interactive(
    name: str,
    prompt: str,
    default: str,
    check: typing.Callable = lambda x: True,
    convert: typing.Callable = lambda x: x,
):
    valid = False
    user_input = default

    while not valid:
        valid = True
        print(f"{prompt}")
        user_input = input(f"Enter: {default} oder eintippen>")
        if len(user_input) == 0:
            user_input = default
        if not check(user_input):
            valid = False
            print(f"{user_input} ist keine gültige Eingabe für {name}.")
    return convert(user_input)


def ja_nein_to_bool(answer: str) -> bool:
    if answer.lower().startswith("j"):
        return True
    else:
        return False


def check_time_in_format(answer: str) -> bool:
    parts = answer.split(":")
    for part in parts:
        try:
            int(part)
        except ValueError:
            return False
    return True


def get_args_interactive() -> types.SimpleNamespace:
    args = types.SimpleNamespace()
    print("Ohne Parameter gestartet. Wir machen das jetzt interaktiv.")
    args.until = get_input_interactive(
        name="until",
        prompt="Möchtest du eine Ziel-Uhrzeit angeben? Ja für Uhrzeit, Nein für Zeitspanne",
        default="Ja",
        check=lambda x: x.lower().startswith("j") or x.lower().startswith("n"),
        convert=ja_nein_to_bool,
    )

    if args.until:
        args.time_in = get_input_interactive(
            name="Ziel-Uhrzeit",
            prompt="Wie viel Uhr soll der Countdown enden? (24-Stunden-Format, Doppelpunkt als Trennzeichen mit Stunden und Minuten, Sekunden optional. Beispiel 13: 05",
            default="00:00",
            check=lambda x: x.count(":") > 0,
        )
    else:
        args.time_in = get_input_interactive(
            name="Zeitdauer",
            prompt="Wie lange soll der Countdown andeuern? Entweder in Sekunden oder Minuten:Sekunden oder Stunden:Minuten:Sekunden",
            default="60",
            check=check_time_in_format,
            convert=lambda x: str(get_seconds_from_mixed_format(x)),
        )

    args.file = get_input_interactive(
        name="Dateipfad",
        prompt="In welche Datei soll geschrieben werden?",
        default="./time.txt",
        check=lambda x: pathlib.Path(x).parent.exists(),
    )

    args.step = get_input_interactive(
        name="Schrittgröße",
        prompt="Nach wie vielen Sekunden soll aktualisiert werden? Eingabe als Ganzzahl",
        default="1",
        check=lambda x: x.isdecimal(),
        convert=int,
    )

    args.print = get_input_interactive(
        name="Ausführliche Ausgabe",
        prompt='Möchtest du zusätzlich zur Datei Ausgabe hier im Terminal? ("Ja" oder "J".',
        default="Nein",
        check=lambda x: x.lower().startswith("j") or x.lower().startswith("n"),
        convert=ja_nein_to_bool,
    )

    args.ending = get_input_interactive(
        name="Endtext",
        prompt="Was soll statt 00:00 am Ende angezeigt werden?",
        default="",
    )

    args.prefix = get_input_interactive(
        name="Präfix",
        prompt="Was soll vor der Restzeitanzeige angezeigt werden?",
        default="",
    )

    return args


def exit_interrupt(signum, stackframe):
    print("Mit Strg+C beendet")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_interrupt)

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
