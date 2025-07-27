# 🏸 Badminton Rank Estimator (2568)

A Streamlit app for evaluating badminton player pair ranks and viewing registered teams.

## 🔧 Features

- 🎯 **Rank Estimation**: Select two players to calculate their average score and estimate their pair's rank.
- 📝 **Team Register Viewer**: View registered player pairs with their ranks.
- 🔁 Live integration with **Google Sheets** for real-time updates.

## 🚀 How to Run

1. **Install requirements**
   ```bash
   uv pip freeze > requirements.txt
   ```

2. **Add your Streamlit secrets**

   Create a `.streamlit/secrets.toml` file:

   ```toml
   [google]
   API_KEY = "your_google_api_key"
   SPREADSHEET_ID = "your_google_spreadsheet_id"
   ```

4. **Run the app**
   ```bash
   uv run streamlit run app.py
   ```

## 📊 Google Sheets Setup

Make sure your Google Sheet has the following sheets:

- `score`: Columns → `Name`, `Team`, `Score`
- `register`: Columns → `Team`, `Player 1`, `Player 2`, `Rank`

Also, share the sheet with the Google API service account (if using OAuth) or allow public read access (if using API key directly).

---

Enjoy ranking! ✌️