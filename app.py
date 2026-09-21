import os
import csv
import datetime
from io import BytesIO
from flask import Flask, render_template, request, session, redirect, url_for, send_file
from openpyxl import Workbook

from reference_data import (
    TAILLE_ENTREPRISE, ROLE, DEMANDES_PRESTATION, FREQUENCE, SUPPORT, SEXE,
    CSAT, SATISFACTION_ROWS, SATISFACTION_SCALE, CES, ERGONOMIE_ROWS,
    ERGONOMIE_SCALE, FCR, DELAI, CONTINUITE,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-moi-en-production")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RESPONSES_FILE = os.path.join(DATA_DIR, "reponses_employeurs.csv")

CSV_HEADERS = (
    ["date_soumission", "taille_entreprise", "role", "role_autre",
     "demandes_prestation", "demandes_autre", "frequence", "support", "sexe",
     "nps_note", "nps_raison", "csat"]
    + [code for code, _ in SATISFACTION_ROWS]
    + ["ces"]
    + [code for code, _ in ERGONOMIE_ROWS]
    + ["fcr", "delai", "blocage", "suggestions", "continuite"]
)


def save_response(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_exists = os.path.isfile(RESPONSES_FILE)
    with open(RESPONSES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


@app.route("/")
def home():
    session.clear()
    return render_template("home.html")


# ------------------------------------------------------------------
# Etape 1 : Profil de l'employeur (Q1 a Q6)
# ------------------------------------------------------------------
@app.route("/etape1", methods=["GET", "POST"])
def etape1():
    if request.method == "POST":
        session["taille_entreprise"] = request.form.get("taille_entreprise")
        session["role"] = request.form.get("role")
        session["role_autre"] = request.form.get("role_autre", "")
        session["demandes_prestation"] = request.form.getlist("demandes_prestation")
        session["demandes_autre"] = request.form.get("demandes_autre", "")
        session["frequence"] = request.form.get("frequence")
        session["support"] = request.form.get("support")
        session["sexe"] = request.form.get("sexe")
        return redirect(url_for("etape2"))

    return render_template(
        "etape1.html",
        taille_entreprise=TAILLE_ENTREPRISE, role=ROLE,
        demandes_prestation=DEMANDES_PRESTATION, frequence=FREQUENCE,
        support=SUPPORT, sexe=SEXE, step=1, total_steps=5,
    )


# ------------------------------------------------------------------
# Etape 2 : NPS + raison (Q7, Q8)
# ------------------------------------------------------------------
@app.route("/etape2", methods=["GET", "POST"])
def etape2():
    if "taille_entreprise" not in session:
        return redirect(url_for("etape1"))

    if request.method == "POST":
        session["nps_note"] = request.form.get("nps_note")
        session["nps_raison"] = request.form.get("nps_raison", "")
        return redirect(url_for("etape3"))

    return render_template("etape2.html", step=2, total_steps=5)


# ------------------------------------------------------------------
# Etape 3 : CSAT global + matrice satisfaction par etape (Q9, Q10)
# ------------------------------------------------------------------
@app.route("/etape3", methods=["GET", "POST"])
def etape3():
    if "taille_entreprise" not in session:
        return redirect(url_for("etape1"))

    if request.method == "POST":
        session["csat"] = request.form.get("csat")
        for code, _ in SATISFACTION_ROWS:
            session[code] = request.form.get(code, "")
        return redirect(url_for("etape4"))

    return render_template(
        "etape3.html", csat=CSAT, rows=SATISFACTION_ROWS,
        scale=SATISFACTION_SCALE, step=3, total_steps=5,
    )


# ------------------------------------------------------------------
# Etape 4 : CES + matrice ergonomie (Q11, Q12)
# ------------------------------------------------------------------
@app.route("/etape4", methods=["GET", "POST"])
def etape4():
    if "taille_entreprise" not in session:
        return redirect(url_for("etape1"))

    if request.method == "POST":
        session["ces"] = request.form.get("ces")
        for code, _ in ERGONOMIE_ROWS:
            session[code] = request.form.get(code, "")
        return redirect(url_for("etape5"))

    return render_template(
        "etape4.html", ces=CES, rows=ERGONOMIE_ROWS,
        scale=ERGONOMIE_SCALE, step=4, total_steps=5,
    )


# ------------------------------------------------------------------
# Etape 5 : FCR, delai, blocage, suggestions, continuite (Q13 a Q17)
# ------------------------------------------------------------------
@app.route("/etape5", methods=["GET", "POST"])
def etape5():
    if "taille_entreprise" not in session:
        return redirect(url_for("etape1"))

    if request.method == "POST":
        response_data = {
            "date_soumission": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "taille_entreprise": session.get("taille_entreprise", ""),
            "role": session.get("role", ""),
            "role_autre": session.get("role_autre", ""),
            "demandes_prestation": "; ".join(session.get("demandes_prestation", [])),
            "demandes_autre": session.get("demandes_autre", ""),
            "frequence": session.get("frequence", ""),
            "support": session.get("support", ""),
            "sexe": session.get("sexe", ""),
            "nps_note": session.get("nps_note", ""),
            "nps_raison": session.get("nps_raison", ""),
            "csat": session.get("csat", ""),
            "ces": session.get("ces", ""),
            "fcr": request.form.get("fcr", ""),
            "delai": request.form.get("delai", ""),
            "blocage": request.form.get("blocage", ""),
            "suggestions": request.form.get("suggestions", ""),
            "continuite": request.form.get("continuite", ""),
        }
        for code, _ in SATISFACTION_ROWS:
            response_data[code] = session.get(code, "")
        for code, _ in ERGONOMIE_ROWS:
            response_data[code] = session.get(code, "")

        save_response(response_data)
        session.clear()
        return redirect(url_for("merci"))

    return render_template(
        "etape5.html", fcr=FCR, delai=DELAI, continuite=CONTINUITE,
        step=5, total_steps=5,
    )


@app.route("/merci")
def merci():
    return render_template("merci.html")


# ------------------------------------------------------------------
# Dashboard admin
# ------------------------------------------------------------------
@app.route("/admin/reponses")
def admin_reponses():
    admin_key = request.args.get("cle")
    if admin_key != os.environ.get("ADMIN_KEY", "employeurs2026"):
        return "Accès refusé. Ajoutez ?cle=VOTRE_CLE à l'URL.", 403

    rows = []
    if os.path.isfile(RESPONSES_FILE):
        with open(RESPONSES_FILE, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

    total = len(rows)
    nps_scores = [int(r["nps_note"]) for r in rows if r.get("nps_note", "").isdigit()]
    nps_moyen = round(sum(nps_scores) / len(nps_scores), 1) if nps_scores else None
    promoteurs = len([s for s in nps_scores if s >= 9])
    detracteurs = len([s for s in nps_scores if s <= 6])
    nps_score = round((promoteurs - detracteurs) / len(nps_scores) * 100) if nps_scores else None

    csat_values = [r["csat"] for r in rows if r.get("csat")]
    csat_satisfaits = len([c for c in csat_values if c in ("Très satisfait(e)", "Satisfait(e)")])
    csat_pourcent = round(csat_satisfaits / len(csat_values) * 100) if csat_values else None

    fcr_values = [r["fcr"] for r in rows if r.get("fcr")]
    fcr_pourcent = round(
        len([f for f in fcr_values if f == "Oui, entièrement en ligne"]) / len(fcr_values) * 100
    ) if fcr_values else None

    return render_template(
        "admin.html", rows=rows, total=total, nps_moyen=nps_moyen,
        nps_score=nps_score, csat_pourcent=csat_pourcent, fcr_pourcent=fcr_pourcent,
    )


@app.route("/admin/reponses/export")
def admin_export():
    admin_key = request.args.get("cle")
    if admin_key != os.environ.get("ADMIN_KEY", "employeurs2026"):
        return "Accès refusé.", 403

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Réponses"
    if os.path.isfile(RESPONSES_FILE):
        with open(RESPONSES_FILE, encoding="utf-8", newline="") as f:
            for row in csv.reader(f):
                worksheet.append(row)
    else:
        worksheet.append(CSV_HEADERS)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="reponses_employeurs.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
