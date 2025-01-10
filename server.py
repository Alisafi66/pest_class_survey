import os
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, jsonify, request, send_from_directory, render_template_string

app = Flask(__name__)

# Email settings (these should ideally come from environment variables for security reasons)
EMAIL_USER = os.getenv("EMAIL_USER", "abdelekrimsafi3@.com")  # Get from environment variable or replace
EMAIL_PASS = os.getenv("EMAIL_PASS", "Abdelkarim30")  # Get from environment variable or replace

# Image folder and CSV filename
image_folder = 'static/images'
csv_filename = "responses.csv"

# HTML content for the index page
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Viewer</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div id="container">
        <img id="image-display" src="" alt="Image" />
        <div id="buttons">
            <button onclick="recordResponse('Yes')">Yes</button>
            <button onclick="recordResponse('No')">No</button>
            <button onclick="recordResponse('Not Sure')">Not Sure</button>
        </div>
    </div>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/images')
def get_images():
    images = [img for img in os.listdir(image_folder) if img.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    return jsonify(images)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(image_folder, filename)

@app.route('/submit', methods=['POST'])
def submit_responses():
    data = request.json
    user_name = data.get("userName", "user").strip().replace(" ", "_")
    responses = data.get("responses", {})

    # Read existing data from CSV, if it exists
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = list(csv.reader(csvfile))
            header = reader[0]
            rows = reader[1:]
    else:
        header = ["Image Name"]
        rows = []

    # Ensure the user column is in the header
    if user_name not in header:
        header.append(user_name)

    # Update rows with user responses
    image_to_response = {row[0]: row for row in rows}
    for image, response in responses.items():
        if image in image_to_response:
            image_to_response[image].append(response)
        else:
            new_row = [image] + [""] * (len(header) - 2) + [response]
            image_to_response[image] = new_row

    # Fill in empty cells for new users in existing rows
    for row in image_to_response.values():
        while len(row) < len(header):
            row.append("")

    # Write updated data to the CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write header row
        writer.writerows(image_to_response.values())  # Write all rows

    # Send an email notification after responses are saved
    subject = "Survey Completed"
    body = f"Survey responses have been successfully saved by {user_name}. Responses are recorded in {csv_filename}."
    recipient_email = "recipient_email@example.com"  # The email where you want to receive notifications
    send_email(subject, body, recipient_email)

    return jsonify({"message": f"Responses saved to {csv_filename} successfully!"})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def send_email(subject, body, recipient_email):
    """
    Function to send email via SMTP (Gmail in this case).
    """
    sender_email = EMAIL_USER
    sender_password = EMAIL_PASS

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=False)
