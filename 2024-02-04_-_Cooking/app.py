from flask import Flask, render_template, request, url_for
import os
import time

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def start():

    if request.method == "POST":
        if "speichern" in request.form:
            name = request.form.get("name")
            zutaten = request.form.get("zutaten")
            zubereitung = request.form.get("zubereitung")
            d = time.strftime("%d.%m.%Y • %H:%M")

            with open("static/rezepte/" + name + ".txt", "w") as fw:
                fw.write("name: " + name + "\n"\
                         "date: " + d + "\n"\
                         "zutaten: " + zutaten + "\n"\
                         + zubereitung)

    rezepte = []
    rezept_files = []    

    for rezept in os.scandir("static/rezepte"):

        rezept_files.append(rezept.name)

    rezept_files.sort()
    anzahl = len(rezept_files)

    for single_rezept in rezept_files:

        with open("static/rezepte/" + single_rezept, "r") as fr:

            lines = fr.readlines()

            rezepte.append(
                {
                    "name": lines[0].split(": ")[1],
                    "date": lines[1].split(": ")[1],
                    "zutaten": lines[2].split(": ")[1],
                    "zubereitung": "<br>".join(lines[3:])
                }
            )

    return render_template("start.html", rezepte=rezepte, anzahl=anzahl)


if __name__ == "__main__":
    app.run()