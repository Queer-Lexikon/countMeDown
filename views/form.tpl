<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>CountMeDown</title>
</head>
<body>
<h1>CountMeDown</h1>
<form method="post" style="width: 500px" name="webform">

    <fieldset>
        <legend>Modus:</legend>
        <div>
            <input type="radio" id="mode_time" name="mode" value="mode_time" checked>
            <label for="mode_time">Bis zur Zieluhrzeit</label>
        </div>
        <div>
            <input type="radio" id="mode_duration" name="mode" value="mode_duration">
            <label for="mode_duration">Für diese Zeitspanne</label>
        </div>

        <label>Zieluhrzeit:
            <input type="time" name="time" id="time">
        </label>
        <label style="display: none;">
            <abbr title="In Sekunden oder als [Stunden:]Minuten:Sekunden">Dauer:</abbr>
            <input type="text" placeholder="3:15" name="duration" id="duration">
        </label>
    </fieldset>


    <fieldset>
        <legend>Optionale Dinge:</legend>
        <label for="step">Zeit zwischen Aktualisierungen:</label>
        <input type="number" value="1" min="1" step="1" name="step" id="step">


        <div>
            <label for="prefix">Text für vor die Restzeit</label>
            <input type="text" placeholder="Start in" name="prefix" id="prefix">
        </div>

        <div>
            <label for="ending">Text zum nach dem Ende anzeigen</label>
            <input type="text" placeholder="gleich" name="ending" id="ending">
        </div>

    </fieldset>

    <div>
        <input type="submit" style="margin-top: 1rem">
    </div>
</form>

<script>
    document.forms.webform.mode.forEach(radio => radio.addEventListener("change", () => {
        const new_state = document.forms.webform.mode.value;
        const time_field = document.getElementById("time").parentElement
        const duration_field = document.getElementById("duration").parentElement
        if (new_state === "mode_time") {
            time_field.style.display = "";
            duration_field.style.display = "None";
        } else {
            duration_field.style.display = "";
            time_field.style.display = "None";
        }
    }));
</script>
</body>
</html>