from flask import Flask, jsonify, request, render_template, send_file, Response
import os
import uuid
import html
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024    # 1kb limit

file_infos = {}
samples = []

@app.get("/")
def index():
    return render_template("index.html", samples=samples)

@app.get("/file")
def file():
    return render_template("file.html")

@app.post("/api/upload")
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "Please upload a file"}), 400
    
    _, ext = os.path.splitext(file.filename)
    if ext not in [".png", ".jpg", ".jpeg", ".gif"]:
        return jsonify({"error": "Invalid extension"}), 400
    
    _, original_filename = os.path.split(file.filename)
    file_id = str(uuid.uuid4())
    path = f"./uploads/{file_id}{ext}"
    file_infos[file_id] = {
        "original_filename": html.escape(original_filename),
        "path": path
    }
    file.save(path)

    return jsonify({"success": True, "file_id": file_id})

@app.get("/api/file/<file_id>")
def file_api(file_id):
    if file_id not in file_infos:
        return jsonify({"error": "File doesn't exist"}), 404
    
    path = file_infos[file_id]["path"]
    
    response = send_file(path, mimetype="application/octet-stream")
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/api/filename/<file_id>")
def file_info(file_id):
    if file_id not in file_infos:
        return jsonify({"error": "File doesn't exist"}), 404
    
    return Response(
        file_infos[file_id]["original_filename"], 
        mimetype="text/plain"
    )

if __name__ == "__main__":
    for filename in os.listdir("./samples"):

        _, ext = os.path.splitext(filename)
        file_id = str(uuid.uuid4())
        path = f"./uploads/{file_id}{ext}"
        shutil.copy(f"./samples/{filename}", path)
        file_infos[file_id] = {
            "original_filename": html.escape(filename),
            "path": path
        }
        samples.append(file_id)
    app.run(host="0.0.0.0", port=3000)
