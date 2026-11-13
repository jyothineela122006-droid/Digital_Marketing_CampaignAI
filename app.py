from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained AI model
model = joblib.load("digital_marketing_model.pkl")
features = joblib.load("feature_columns.pkl")
print("Required Model Features:", features)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")
@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css")

@app.route("/script.js")
def javascript():
    return send_from_directory(".", "script.js")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        input_data = {
            "Age": data["Age"],
            "Income": data["Income"],
            "AdSpend": data["AdSpend"],
            "ClickThroughRate": data["ClickThroughRate"],
            "ConversionRate": data["ConversionRate"],
            "WebsiteVisits": data["WebsiteVisits"],
            "PagesPerVisit": data["PagesPerVisit"],
            "TimeOnSite": data["TimeOnSite"],
            "SocialShares": data["SocialShares"],
            "EmailOpens": data["EmailOpens"],
            "EmailClicks": data["EmailClicks"],
            "PreviousPurchases": data["PreviousPurchases"],
            "LoyaltyPoints": data["LoyaltyPoints"],
            "Gender_Male": int(data["Gender"] == "Male"),
            "CampaignChannel_PPC": int(data["CampaignChannel"] == "PPC"),
            "CampaignChannel_Referral": int(data["CampaignChannel"] == "Referral"),
            "CampaignChannel_SEO": int(data["CampaignChannel"] == "SEO"),
            "CampaignChannel_Social Media": int(data["CampaignChannel"] == "Social Media"),
            "CampaignType_Consideration": int(data["CampaignType"] == "Consideration"),
            "CampaignType_Conversion": int(data["CampaignType"] == "Conversion"),
            "CampaignType_Retention": int(data["CampaignType"] == "Retention")
        }

        input_df = pd.DataFrame([input_data])
        input_df = input_df[features]

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1] * 100

        if prediction == 1:
            message = "High Potential for Conversion!"
        else:
            message = "Low Potential for Conversion."

        return jsonify({
            "prediction": int(prediction),
            "message": message,
            "probability": round(float(probability), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)