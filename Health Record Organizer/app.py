from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import sqlite3
import os
import uuid

app = Flask(__name__)
app.secret_key = "secret_key"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize Database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    phone TEXT UNIQUE,
                    password TEXT,
                    unique_id TEXT UNIQUE
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    filename TEXT,
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        password = request.form["password"]
        unique_id = str(uuid.uuid4())[:8]

        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, phone, password, unique_id) VALUES (?, ?, ?, ?)",
                (username, phone, password, unique_id)
            )
            conn.commit()
            conn.close()

            # Show success message with user details
            return render_template(
                "register.html",
                username=username,
                phone=phone,
                password=password,
                unique_id=unique_id
            )
        except sqlite3.IntegrityError:
            # Phone number already exists
            error_message = "User with this phone number already exists!"
            return render_template("register.html", error_message=error_message)
    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE phone=?", (phone,))
        user = c.fetchone()
        conn.close()
        if user:
            if user[3] == password:  # Assuming password is in the 4th column
                return redirect(url_for("dashboard", user_id=user[0]))
            else:
                error_message = "Incorrect credentials. Please try again."
        else:
            error_message = "New user? Please register."
        return render_template("login.html", error_message=error_message)
    return render_template("login.html")


@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    # Fetch the user details including phone number
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    
    # Fetch the reports related to the user
    c.execute("SELECT * FROM reports WHERE user_id=?", (user_id,))
    reports = c.fetchall()
    
    conn.close()

    if user:
        return render_template("dashboard.html", username=user[1], phone=user[2], unique_id=user[4], user_id=user[0], reports=reports)
    else:
        flash("User not found!")
        return redirect(url_for('home'))


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("report")
    description = request.form.get("description")
    user_id = request.form.get("user_id")

    if not user_id:
        flash("User ID is missing. Please try again.")
        return redirect(url_for("dashboard", user_id=user_id))

    if file:
        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO reports (user_id, filename, description) VALUES (?, ?, ?)",
                  (user_id, filename, description))
        conn.commit()
        conn.close()
        flash("Upload successful!")
    else:
        flash("No file selected.")
    return redirect(url_for("dashboard", user_id=user_id))

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        unique_id = request.form["unique_id"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT phone, password FROM users WHERE unique_id=?", (unique_id,))
        user = c.fetchone()
        conn.close()

        if user:
            user_details = {"phone": user[0], "password": user[1]}
            return render_template("forgot.html", user_details=user_details)
        else:
            error_message = "Unique ID does not exist. Please try again."
            return render_template("forgot.html", error_message=error_message)
    return render_template("forgot.html")


@app.route("/download/<int:report_id>")
def download(report_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT filename, user_id FROM reports WHERE id=?", (report_id,))
    report = c.fetchone()
    conn.close()
    
    if report:
        filename = report[0]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        if os.path.exists(filepath):
            return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)
        else:
            flash("File not found.")
    else:
        flash("Report not found.")
    
    return redirect(url_for("dashboard", user_id=report[1]))

@app.route("/delete/<int:report_id>")
def delete(report_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT filename, user_id FROM reports WHERE id=?", (report_id,))
    report = c.fetchone()
    
    if report:
        filename = report[0]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
        
        c.execute("DELETE FROM reports WHERE id=?", (report_id,))
        conn.commit()
        flash("Report deleted successfully!")
        conn.close()
        
        return redirect(url_for("dashboard", user_id=report[1]))
    
    conn.close()
    flash("Report not found.")
    return redirect(url_for("dashboard", user_id=report[1]))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    init_db()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
