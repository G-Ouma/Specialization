
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Temporary in-memory storage
egg_records = []


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Add egg production record
@app.route("/api/eggs", methods=["POST"])
def add_egg_record():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    shed = data.get("shed")
    date = data.get("date")
    count = data.get("count")

    if not shed or not date or count is None:
        return jsonify({
            "error": "shed, date and count are required"
        }), 400

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({
            "error": "Date must use YYYY-MM-DD format"
        }), 400

    if type(count) is not int or count < 0:
        return jsonify({
            "error": "Count must be a non-negative integer"
        }), 400

    record = {
        "shed": shed,
        "date": date,
        "count": count
    }

    egg_records.append(record)

    return jsonify({
        "message": "Egg record added successfully",
        "record": record
    }), 201


# Retrieve all egg records
@app.route("/api/eggs", methods=["GET"])
def get_egg_records():
    sorted_records = sorted(
        egg_records,
        key=lambda record: (record["date"], record["shed"])
    )

    running_total = 0
    results = []

    for record in sorted_records:
        running_total += record["count"]

        results.append({
            **record,
            "running_total": running_total
        })

    return jsonify({
        "records": results,
        "total_records": len(results),
        "total_eggs": running_total
    }), 200


if __name__ == "__main__":
    app.run(debug=True)