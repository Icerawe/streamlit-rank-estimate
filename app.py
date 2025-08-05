import streamlit as st
from function import get_sheet_data

# Load secrets
API_KEY = st.secrets["google"]["API_KEY"]
SPREADSHEET_ID = st.secrets["google"]["SPREADSHEET_ID"]

# --- UI Begins ---
tab1, tab2 = st.tabs(["🎯 ประเมิน Rank", "📝 ตรวจสอบรายชื่อ"])

with tab1:
    st.header("🏸 การแข่งขัน แบดมินตันภายใน ปี 2568 🎉✌️")
    st.markdown("###### เลือกผู้เล่นที่ต้องการคู่กัน เพื่อคํานวณ Rank")
    df_score = get_sheet_data(API_KEY, SPREADSHEET_ID, "score")
    df = df_score.astype({
        "Name": "string",
        "Team": "string",
        "Score": "float"
    })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧑‍🤝‍🧑 Player 1")
        team1 = st.selectbox("ทีมของผู้เล่น 1", df["Team"].unique(), key="team1")
        name1 = st.selectbox("ชื่อผู้เล่น 1", df[df["Team"] == team1]["Name"], key="name1")
        score1 = df[(df["Name"] == name1) & (df["Team"] == team1)]["Score"].values[0]

    with col2:
        st.markdown("### 🧑‍🤝‍🧑 Player 2")
        team2 = st.selectbox("ทีมของผู้เล่น 2", df["Team"].unique(), key="team2")
        name2 = st.selectbox("ชื่อผู้เล่น 2", df[df["Team"] == team2]["Name"], key="name2")
        score2 = df[(df["Name"] == name2) & (df["Team"] == team2)]["Score"].values[0]

    def estimate_rank(score1, score2, avg):
        if abs(score1 - score2) >= 5:
            return "มือแบก ไม่สามารถคู่กันได้"
        elif avg >= 7.5:
            return "มือ S"
        elif avg >= 5:
            return "มือ N"
        elif avg >= 1:
            return "มือ BG"
        else:
            return "ต้องมีอะไรผิด"
        
        # Estimate
    avg_score = (score1 + score2) / 2
    if name1 == name2 and team1 == team2:
        st.warning("โปรดเลือกผู้เล่นที่ต่างกัน")
    else:
        rank = estimate_rank(score1, score2, avg_score)
        st.subheader("🎯 ผลการประเมิน Rank ของผู้เล่น")
        if rank.startswith("มือแบก"):
            st.error(f"Estimated Rank: **{rank}**")
        else:
            # st.text(avg_score)
            st.success(f"Estimated Rank: **{rank}**")

with tab2:
    st.header("📝 ตรวจสอบรายชื่อ")
    df_pairs = get_sheet_data(API_KEY, SPREADSHEET_ID, "register")
    df_pairs = df_pairs[["Team", "Player 1", "Player 2", "Rank"]]

    # Optional: convert Rank to categorical for custom sorting
    rank_order = ["S", "N", "BG",]
    df_pairs["Rank"] = df_pairs["Rank"].astype(str)

    # Group by Rank and show the table
    for rank in rank_order:
        df_ranked = df_pairs[df_pairs["Rank"].str.upper() == rank.upper()]
        df_ranked = df_ranked.sort_values(by=["Team"])
        if not df_ranked.empty:
            df_ranked["Order"] = range(1, len(df_ranked) + 1)
            df_ranked.set_index("Order", inplace=True)

            st.markdown(f"### 🏅 Rank: {rank}")
            st.dataframe(df_ranked, use_container_width=True)