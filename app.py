import json
import os
import subprocess
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

DEFAULT_CONFIG = "task_language=eng|os_task_file_format=json|is_text_type=plain"
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB uploads


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    @app.get("/health")
    def health() -> tuple[dict, int]:
        """Simple health-check endpoint."""
        return {"status": "ok"}, 200

    @app.post("/align")
    def align():
        """Run aeneas alignment for uploaded audio and text files."""
        if "audio" not in request.files or "text" not in request.files:
            return jsonify({
                "error": "Both 'audio' and 'text' file uploads are required."
            }), 400

        audio_file = request.files["audio"]
        text_file = request.files["text"]
        config = request.form.get("config", DEFAULT_CONFIG)

        if not audio_file.filename:
            return jsonify({"error": "Audio file must have a filename."}), 400
        if not text_file.filename:
            return jsonify({"error": "Text file must have a filename."}), 400

        with tempfile.TemporaryDirectory() as tmp_dir:
            audio_path = Path(tmp_dir) / secure_filename(audio_file.filename)
            text_path = Path(tmp_dir) / secure_filename(text_file.filename)
            output_path = Path(tmp_dir) / "map.json"

            audio_file.save(audio_path)
            text_file.save(text_path)

            command = [
                "python3",
                "-m",
                "aeneas.tools.execute_task",
                str(audio_path),
                str(text_path),
                config,
                str(output_path),
            ]

            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            if process.returncode != 0:
                return (
                    jsonify(
                        {
                            "error": "aeneas execution failed",
                            "stderr": process.stderr,
                            "stdout": process.stdout,
                            "returncode": process.returncode,
                        }
                    ),
                    500,
                )

            try:
                output_data = json.loads(output_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                output_data = output_path.read_text(encoding="utf-8")

        return jsonify(
            {
                "config": config,
                "stdout": process.stdout,
                "map": output_data,
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
