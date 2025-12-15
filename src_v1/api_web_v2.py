from flask import Flask, request, jsonify
import pandas as pd


app = Flask(__name__)

# --- Sample DataFrame simulating Presseportal press releases ---
data = {
    "id": [1, 2, 3],
    "title": [
        "New Product Launch by Company X",
        "Police Report: Traffic Accident",
        "Government Announces New Policy"
    ],
    "category": ["Business", "Police", "Politics"],
    "date": ["2025-12-01", "2025-12-05", "2025-12-10"],
    "content": [
        "Company X has launched a new product in the tech sector...",
        "A traffic accident occurred on highway A7 with minor injuries...",
        "The government has announced a new policy regarding climate change..."
    ]
}

df = pd.DataFrame(data)


# --- API Endpoints ---
@app.route("/pressreleases", methods=["GET"])
def get_press_releases():
    """
    Returns all press releases or filters by category/date/keyword.
    Example: /pressreleases?category=Police&keyword=accident
    """
    category = request.args.get("category")
    keyword = request.args.get("keyword")
    date = request.args.get("date")

    filtered_df = df.copy()

    if category:
        filtered_df = filtered_df[filtered_df["category"].str.lower() == category.lower()]
    if keyword:
        filtered_df = filtered_df[filtered_df["content"].str.contains(keyword, case=False)]
    if date:
        filtered_df = filtered_df[filtered_df["date"] == date]

    return jsonify(filtered_df.to_dict(orient="records"))


@app.route("/pressreleases/<int:release_id>", methods=["GET"])
def get_press_release_by_id(release_id):
    """
    Returns a single press release by ID.
    Example: /pressreleases/2
    """
    release = df[df["id"] == release_id]
    if release.empty:
        return jsonify({"error": "Press release not found"}), 404
    return jsonify(release.to_dict(orient="records")[0])


@app.route("/categories", methods=["GET"])
def get_categories():
    """
    Returns all available categories.
    Example: /categories
    """
    categories = df["category"].unique().tolist()
    return jsonify(categories)


# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True)
