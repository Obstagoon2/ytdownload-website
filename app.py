from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        file_format = request.form.get("format")
        if not url:
            return "Error: No URL provided", 400

        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{uuid.uuid4()}.%(ext)s"
        filepath = os.path.join(output_dir, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': 'bestaudio/best' if file_format == 'mp3' else 'best',
        }

        if file_format == "mp3":
            ydl_opts["postprocessors"] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        actual_file = max(
            [os.path.join(output_dir, f) for f in os.listdir(output_dir)],
            key=os.path.getctime
        )

        return send_file(actual_file, as_attachment=True)

    return render_template("index.html")
