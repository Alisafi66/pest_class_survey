import os
import csv
from flask import Flask, jsonify, request, send_from_directory, render_template_string

app = Flask(__name__)

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
            <button onclick="nextImage()">Next</button>
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

    return jsonify({"message": f"Responses saved to {csv_filename} successfully!"})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Route to view the responses stored in the CSV file
@app.route('/responses')
def view_responses():
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
        
        # Create HTML table from CSV data
        table_html = "<table border='1'><tr><th>Image Name</th><th>Responses</th></tr>"
        for row in rows[1:]:  # Skip header row
            table_html += f"<tr><td>{row[0]}</td><td>{', '.join(row[1:])}</td></tr>"
        table_html += "</table>"
        return table_html
    else:
        return "<p>No responses yet.</p>"

if __name__ == '__main__':
    app.run(debug=False)
