from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
import requests

app = Flask(__name__)
app.secret_key = "your_secure_random_secret_key"

GOOGLE_SHEET_WEBHOOK_URL = (
    "https://script.google.com/macros/s/AKfycbxgVrzUK91AvYloVAW8d7N72SWz59d4BTPPE7klv4XfQKcaqbWvH4fviL7toPGgFAFI/exec"
)


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/rsvp", methods=["POST"])
def rsvp():
  names = request.form.get("names")
  attendance = request.form.get("attendance")
  notes = request.form.get("notes", "")
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  payload = {
      "timestamp": timestamp,
      "names": names,
      "attendance": attendance,
      "notes": notes,
  }

  try:
    response = requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
      flash("Thank you! Your RSVP has been recorded.", "success")
    else:
      flash("There was an error saving your RSVP. Please try again.", "error")
  except Exception as e:
    flash("Connection error. Please try again later.", "error")

  return redirect(url_for("index"))


if __name__ == "__main__":
  app.run(debug=True, port=5000)