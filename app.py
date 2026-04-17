from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os
print("Current Directory:", os.getcwd())
print("Files in Directory:", os.listdir())

app = Flask(__name__, static_folder='.')
CORS(app)

# ── Load & prepare data (unchanged logic) ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "commercedata.csv")

print("Dataset path:", file_path)

data = pd.read_csv(file_path)
if 'event' in data.columns:
    event_score = {'view': 1, 'addtocart': 2, 'purchase': 3}
    data['rating'] = data['event'].map(event_score)

user_col    = 'customer_id'
product_col = 'product_id'
ratings_col = 'ratings'

matrix = data.pivot_table(
    index=user_col,
    columns=product_col,
    values=ratings_col).fillna(0)

similarity = cosine_similarity(matrix)
similarity_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

product_map = {}
if 'product_name' in data.columns:
    product_map = (data.drop_duplicates('product_id')
                       .set_index('product_id')['product_name']
                       .to_dict())

# ── Recommendation function (unchanged logic) ──────────────────────────────────
def recommend_products(customer_id, top_n=5):
    if customer_id not in similarity_df.index:
        return None
    similar_users   = similarity_df[customer_id].sort_values(ascending=False).iloc[1:6]
    user_products   = set(data[data[user_col] == customer_id][product_col])
    recommended_ids = set()
    for sim_user in similar_users.index:
        recommended_ids.update(set(data[data[user_col] == sim_user][product_col]))
    final_ids = list(recommended_ids - user_products)[:top_n]
    return [{"id": pid, "name": product_map.get(pid, "Unknown Product")} for pid in final_ids]

# ── API routes ─────────────────────────────────────────────────────────────────
@app.route('/api/recommend')
def recommend():
    try:
        cid = request.args.get('customer_id')
        top_n = int(request.args.get('top_n', 5))

        if not cid:
            return jsonify({"error": "Customer ID required"}), 400

        cid = int(cid)

        # your recommendation logic here
        recommendations = []

        return jsonify({
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
   try:
    # your logic here
    cid = request.args.get('customer_id')

    if not cid:
        return jsonify({"error": "Customer ID required"})
   except Exception as e:
       return jsonify({"error": str(e)})
       if result is None:
           return jsonify({"error": "Customer not found"}), 404
           return jsonify({"customer_id": cid, "recommendations": result})
   except (ValueError, TypeError):
       return jsonify({"error": "Invalid customer ID"}), 400

@app.route('/api/customers', methods=['GET'])
def api_customers():
    ids = sorted(matrix.index.tolist())
    return jsonify({"customer_ids": ids})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
