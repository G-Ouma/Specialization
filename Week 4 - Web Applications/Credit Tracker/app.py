
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Hardcoded customer balances
customers = {
    "john kamau": 15000,
    "mary wanjiku": 8500,
    "peter kiptoo": 22000,
    "james otieno": 5000,
    "grace chebet": 12000,
    "john otieno": 15000
}


# Home route
@app.route("/")
def home():
    return render_template("index.html")


# API route
@app.route("/api/balance")
def get_balance():
    search_name = request.args.get("customer", "").strip().lower()

    if not search_name:
        return jsonify({"error": "Please provide a customer name."}), 400

    # Search for matching customers
    matches = {
        name: balance
        for name, balance in customers.items()
        if search_name in name.split()
    }

    # Also allow full-name searches
    if not matches:
        matches = {
            name: balance
            for name, balance in customers.items()
            if search_name in name
        }

    if len(matches) == 1:
        customer_name, balance = next(iter(matches.items()))

        return jsonify({
            "customer": customer_name.title(),
            "balance": balance,
            "currency": "KES"
        })

    elif len(matches) > 1:
        return jsonify({
            "error": "Multiple customers found. Please enter a more specific name."
        }), 409

    return jsonify({"error": "Customer not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
