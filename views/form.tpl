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


        <div>
            <label>Zieluhrzeit:
                <input type="time" name="time" id="time">
            </label>
            <label style="display: none;">
                <abbr title="In Sekunden oder als [Stunden:]Minuten:Sekunden">Dauer:</abbr>
                <input type="text" placeholder="3:15" name="duration" id="duration">
            </label>
        </div>
    </fieldset>


    <fieldset style="display: grid; grid-template-columns: auto auto; grid-gap: 5px;">
        <legend>Optionale Dinge:</legend>

        <div>
            <label for="step">Zeitschritt:</label>
            <input type="number" value="1" min="1" step="1" name="step" id="step">
        </div>


        <div>
            <label for="prefix">Präfix vor Restzeit</label>
            <input type="text" placeholder="Start in" name="prefix" id="prefix">
        </div>

        <div>
            <label for="ending">Text am Ende:</label>
            <input type="text" placeholder="gleich" name="ending" id="ending">
        </div>

        <div>
            <input type="submit" value="Timer starten" style="margin-top: 1rem">
        </div>
    </fieldset>

</form>

<script>
    document.forms.webform.mode.forEach(radio => radio.addEventListener("change", () => {
        const new_state = document.forms.webform.mode.value;
        const time_field = document.getElementById("time")
        const duration_field = document.getElementById("duration")
        if (new_state === "mode_time") {
            time_field.parentElement.style.display = "";
            duration_field.parentElement.style.display = "None";
            duration_field.disabled = true;
            time_field.disabled = false;
        } else {
            duration_field.parentElement.style.display = "";
            time_field.parentElement.style.display = "None";
            time_field.disabled = true;
            duration_field.disabled = false;
        }
    }));
</script>
</body>
</html>