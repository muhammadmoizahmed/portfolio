from flask import Flask, render_template, request, flash, url_for, session, redirect
import os
import json
from email.message import EmailMessage
import smtplib
import ssl
from datetime import datetime
import urllib.request
import urllib.parse
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_content():
    path = os.path.join(os.path.dirname(__file__), "static", "data", "content.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_content(data):
    path = os.path.join(os.path.dirname(__file__), "static", "data", "content.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def verify_recaptcha(token: str) -> bool:
    secret = os.environ.get("RECAPTCHA_SECRET", "")
    if not secret:
        return True
    if not token:
        return False
    data = urllib.parse.urlencode({"secret": secret, "response": token}).encode()
    req = urllib.request.Request("https://www.google.com/recaptcha/api/siteverify", data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return bool(result.get("success"))
    except Exception:
        return False

@app.route("/")
def index():
    content = load_content()
    site_key = os.environ.get("RECAPTCHA_SITE_KEY", "")
    return render_template("index.html", content=content, year=datetime.now().year, submitted=False, site_key=site_key)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()
    token = request.form.get("g-recaptcha-response", "")
    if not name or not email or not message:
        flash("Please fill all fields.", "error")
        return redirect(url_for("index"))
    if "@" not in email or "." not in email:
        flash("Please enter a valid email.", "error")
        return redirect(url_for("index"))
    if not verify_recaptcha(token):
        flash("reCAPTCHA verification failed.", "error")
        return redirect(url_for("index"))
    gmail_user = os.environ.get("GMAIL_USER", "")
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD", "")
    receiver = "moizsiddique93@gmail.com"
    if not gmail_user or not gmail_pass:
        flash("Email service not configured.", "error")
        return redirect(url_for("index"))
    msg = EmailMessage()
    msg["Subject"] = f"Portfolio Contact Form{': ' + subject if subject else ''}"
    msg["From"] = gmail_user
    msg["To"] = receiver
    msg["Reply-To"] = email
    msg.set_content(
        f"Name: {name}\nEmail: {email}\nSubject: {subject if subject else 'N/A'}\nPhone: {phone if phone else 'N/A'}\n\nMessage:\n{message}"
    )
    auto = EmailMessage()
    auto["Subject"] = "Thank you for reaching out"
    auto["From"] = gmail_user
    auto["To"] = email
    auto.set_content("Thank you! I will contact you soon.")
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)
            server.send_message(auto)
        flash("Thank you! I will contact you soon.", "success")
    except Exception:
        flash("Failed to send email. Please try again later.", "error")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        # Use environment variable for security, fallback for dev
        correct_password = os.environ.get("ADMIN_PASSWORD", "moiz@1234556m7890")
        if password == correct_password:
            session["logged_in"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin"))
        else:
            flash("Invalid password.", "error")
    return render_template("login.html", content=load_content(), year=datetime.now().year)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out.", "success")
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
        
    content = load_content()
    if request.method == "POST":
        section = request.form.get("section", "")
        
        if section == "site":
            content["site"]["title"] = request.form.get("title", "").strip()
            content["site"]["brand"] = request.form.get("brand", "").strip()
            content["site"]["role"] = request.form.get("role", "").strip()
            content["site"]["description"] = request.form.get("description", "").strip()
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    content["site"]["image"] = filename
            flash("Site info updated.", "success")
            
        elif section == "social":
            action = request.form.get("action", "")
            if action == "add":
                name = request.form.get("name", "").strip()
                url = request.form.get("url", "").strip()
                icon = request.form.get("icon", "").strip()
                
                image_filename = ""
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_filename = filename
                
                if name and url:
                    entry = {"name": name, "url": url, "icon": icon}
                    if image_filename:
                        entry["image"] = image_filename
                    content["social"].append(entry)
                    flash("Social link added.", "success")
            elif action == "delete":
                idx = int(request.form.get("index", -1))
                if 0 <= idx < len(content["social"]):
                    content["social"].pop(idx)
                    flash("Social link removed.", "success")
            elif action == "update":
                idx = int(request.form.get("index", -1))
                name = request.form.get("name", "").strip()
                url = request.form.get("url", "").strip()
                icon = request.form.get("icon", "").strip()
                
                if 0 <= idx < len(content["social"]):
                    entry = content["social"][idx]
                    entry["name"] = name
                    entry["url"] = url
                    entry["icon"] = icon
                    
                    if 'image' in request.files:
                        file = request.files['image']
                        if file and file.filename:
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            entry["image"] = filename
                    
                    content["social"][idx] = entry
                    flash("Social link updated.", "success")

        elif section == "about":
            content["about"]["paragraph"] = request.form.get("paragraph", "").strip()
            flash("About section updated.", "success")
            
        elif section == "skills":
            action = request.form.get("action", "")
            if action == "add":
                name = request.form.get("name", "").strip()
                icon = request.form.get("icon", "").strip()
                image_filename = ""
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_filename = filename
                
                if name:
                    entry = {"name": name, "icon": icon}
                    if image_filename:
                        entry["image"] = image_filename
                    content["skills"].append(entry)
                    flash("Skill added.", "success")
            elif action == "delete":
                idx = int(request.form.get("index", -1))
                if 0 <= idx < len(content["skills"]):
                    content["skills"].pop(idx)
                    flash("Skill removed.", "success")
            elif action == "update":
                idx = int(request.form.get("index", -1))
                if 0 <= idx < len(content["skills"]):
                    name = request.form.get("name", "").strip()
                    icon = request.form.get("icon", "").strip()
                    # Keep existing image if no new one
                    existing = content["skills"][idx]
                    image_filename = existing.get("image", "")
                    
                    if 'image' in request.files:
                        file = request.files['image']
                        if file and file.filename:
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            image_filename = filename
                    
                    content["skills"][idx] = {"name": name, "icon": icon}
                    if image_filename:
                        content["skills"][idx]["image"] = image_filename
                    flash("Skill updated.", "success")

        elif section == "project":
            idx = request.form.get("index", "").strip()
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            link = request.form.get("link", "").strip()
            
            # Handle new images
            new_images = []
            if 'new_images' in request.files:
                files = request.files.getlist('new_images')
                for file in files:
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        new_images.append(filename)
            
            action = request.form.get("action", "save")
            
            if action == "delete" and idx.isdigit():
                i = int(idx)
                if 0 <= i < len(content.get("projects", {}).get("all", [])):
                    content["projects"]["all"].pop(i)
                    flash("Project deleted.", "success")
            elif not title or not description:
                flash("Title and description are required.", "error")
            else:
                if idx.isdigit():
                    i = int(idx)
                    if 0 <= i < len(content.get("projects", {}).get("all", [])):
                        entry = content["projects"]["all"][i]
                        entry["title"] = title
                        entry["description"] = description
                        if link:
                            entry["link"] = link
                        else:
                            entry.pop("link", None)
                            
                        # Handle deletions
                        delete_images = request.form.getlist("delete_images")
                        current_images = entry.get("images", [])
                        remaining_images = [img for img in current_images if img not in delete_images]
                        
                        # Combine
                        entry["images"] = remaining_images + new_images
                        content["projects"]["all"][i] = entry
                        flash("Project updated.", "success")
                    else:
                        flash("Invalid index.", "error")
                else:
                    entry = {"title": title, "description": description, "images": new_images}
                    if link:
                        entry["link"] = link
                    content["projects"]["all"].append(entry)
                    flash("Project added.", "success")
        
        save_content(content)
        return redirect(url_for("admin"))
        
    return render_template("admin.html", content=content, year=datetime.now().year)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
