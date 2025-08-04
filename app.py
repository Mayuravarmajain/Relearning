from flask import Flask, request, jsonify
import importlib
import json
import os
import sys

app = Flask(__name__)

# Add current dir to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load DOCID → Pattern mapping
with open("config/patterns.json") as f:
    DOCID_TO_PATTERN = json.load(f)

@app.route("/check", methods=["POST"])
def check_pattern():
    stage = request.form["stage"]
    pattern = request.form["pattern"]
    return jsonify({"status": "not_found", "message": f"Pattern '{pattern}' not found in stage '{stage}'."})

@app.route("/relearn", methods=["POST"])
def relearn():
    stage = request.form["stage"]
    doc_or_pattern = request.form["pattern"]

    try:
        # For L-1, pattern is entered directly
        if stage == "L-1":
            pattern = doc_or_pattern
        else:
            pattern = DOCID_TO_PATTERN.get(doc_or_pattern)
            if not pattern:
                return jsonify({"status": "error", "message": f"DOCID '{doc_or_pattern}' not found in config."})

        # Build module name
        
        module_name = f"{stage.upper().replace('-', '')}_LOAD.relearn_module"
        print("Importing module:", module_name)  # For debugging

        module = importlib.import_module(module_name)

        # Call the module's `process` function
        message = module.process(pattern)
        return jsonify({"status": "success", "message": message})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
