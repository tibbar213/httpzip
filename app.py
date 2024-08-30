from flask import Flask, request, render_template, send_file, Response
from unzip_http import RemoteZipFile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    files = []
    url = ""
    if request.method == "POST":
        url = request.form["url"]
        try:
            with RemoteZipFile(url) as z:
                files = z.namelist()  # Get the list of files in the remote ZIP
        except Exception as e:
            print(f"Error: {e}")

    return render_template("index.html", files=files, url=url)

@app.route("/download", methods=["GET"])
def download_file():
    url = request.args.get("url")
    filename = request.args.get("file")

    try:
        with RemoteZipFile(url) as z:
            def generate():
                with z.open(filename) as file_in_zip:
                    for chunk in iter(lambda: file_in_zip.read(8192), b""):
                        yield chunk

            response = Response(generate(), mimetype='application/octet-stream')
            response.headers.set('Content-Disposition', 'attachment', filename=filename)
            return response
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)