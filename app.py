# app.py
# Streamlit app: Morse + GCS + Braden + VIP (giao diện đẹp, tiếng Việt)
# Chạy: pip install streamlit && streamlit run app.py

import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Ứng dụng đánh giá nhanh", layout="wide")

st.title("Ứng dụng đánh giá nhanh — Morse • GCS • Braden • VIP")
st.markdown("Ứng dụng chỉ **tính toán và hiển thị kết quả**, không lưu dữ liệu. \
             Dùng nhanh tại giường hoặc trên máy tính, điện thoại.")

st.sidebar.header("Tùy chọn")
show_details = st.sidebar.checkbox("Hiện chi tiết từng tiêu chí", value=True)
st.sidebar.caption("Phiên bản: 1.1 — Không lưu, không gửi dữ liệu.")

# Tabs cho từng thang đánh giá
tabs = st.tabs(["Morse (Nguy cơ té ngã)", "GCS (Trạng thái ý thức)", "Braden (Nguy cơ loét tỳ)", "VIP (Viêm tiêm truyền)"])

# ----------------------------
# 1) Morse Fall Scale
# ----------------------------
with tabs[0]:
    st.header("Morse Fall Scale")
    st.markdown("Chọn các mục phù hợp với bệnh nhân:")

    with st.form("morse_form"):
        col1, col2 = st.columns(2)
        with col1:
            morse_q1 = st.radio("1. Tiền sử té ngã", ("Không", "Có — té ngã trong 3 tháng"))
            morse_q2 = st.radio("2. Chẩn đoán phụ (≥2 bệnh?)", ("Không", "Có — ≥2 bệnh"))
            morse_q3 = st.selectbox("3. Dụng cụ hỗ trợ đi lại",
                                    ("Không / nằm nghỉ / điều dưỡng hỗ trợ",
                                     "Nạng / gậy / khung tập đi",
                                     "Bám / tựa vào đồ đạc / xe lăn"))
        with col2:
            morse_q4 = st.radio("4. Truyền dịch / thuốc tĩnh mạch", ("Không", "Có"))
            morse_q5 = st.selectbox("5. Dáng đi / cách di chuyển",
                                    ("Bình thường / nằm nghỉ / bất động", "Yếu", "Khó khăn / loạng choạng"))
            morse_q6 = st.radio("6. Tình trạng tâm thần", ("Đánh giá đúng khả năng", "Quên giới hạn của bản thân"))
        extra_ah = st.checkbox("Bệnh nhân đang dùng thuốc hạ huyết áp (+10 điểm)?", value=False)
        morse_submitted = st.form_submit_button("Tính Morse")

    # Tính điểm Morse
    morse_score = 0
    morse_details = []
    if morse_q1.startswith("Có"): morse_score += 25; morse_details.append(("Tiền sử té ngã",25))
    else: morse_details.append(("Tiền sử té ngã",0))
    if morse_q2.startswith("Có"): morse_score += 15; morse_details.append(("Chẩn đoán phụ",15))
    else: morse_details.append(("Chẩn đoán phụ",0))
    if morse_q3.startswith("Không"): morse_score += 0; morse_details.append(("Dụng cụ",0))
    elif morse_q3.startswith("Nạng"): morse_score += 15; morse_details.append(("Dụng cụ",15))
    else: morse_score += 30; morse_details.append(("Dụng cụ",30))
    if morse_q4.startswith("Có"): morse_score += 20; morse_details.append(("Truyền dịch/IV",20))
    else: morse_details.append(("Truyền dịch/IV",0))
    if morse_q5.startswith("Bình thường"): morse_score += 0; morse_details.append(("Dáng đi",0))
    elif morse_q5.startswith("Yếu"): morse_score += 10; morse_details.append(("Dáng đi",10))
    else: morse_score += 20; morse_details.append(("Dáng đi",20))
    if morse_q6.startswith("Quên"): morse_score += 15; morse_details.append(("Tâm thần",15))
    else: morse_details.append(("Tâm thần",0))
    if extra_ah: morse_score += 10; morse_details.append(("Modifier: Thuốc hạ huyết áp",10))

    if morse_score >= 45: morse_risk = "Nguy cơ cao"
    elif morse_score >= 25: morse_risk = "Nguy cơ trung bình"
    else: morse_risk = "Nguy cơ thấp"

    st.subheader("Kết quả Morse")
    st.metric("Tổng điểm Morse", morse_score)
    st.write("Mức nguy cơ:", morse_risk)
    if show_details:
        st.write("Chi tiết điểm (tiêu chí: điểm):")
        for k,v in morse_details: st.write(f"- {k}: {v}")

# ----------------------------
# 2) Glasgow Coma Scale (GCS)
# ----------------------------
with tabs[1]:
    st.header("Glasgow Coma Scale (GCS)")
    st.markdown("Nhập điểm từng phần (E = Mở mắt, V = Ngôn ngữ, M = Vận động). Tổng 3–15.")

    with st.form("gcs_form"):
        gcs_e = st.selectbox("Mở mắt (E)", options=[4,3,2,1], format_func=lambda x: f"{x} — " + {4:"Tự mở mắt",3:"Mở khi gọi",2:"Mở khi đau",1:"Không mở"}[x])
        gcs_v = st.selectbox("Ngôn ngữ (V)", options=[5,4,3,2,1], format_func=lambda x: f"{x} — " + {5:"Bình thường",4:"Lẫn lộn",3:"Nói không phù hợp",2:"Âm thanh không hiểu",1:"Không nói"}[x])
        gcs_m = st.selectbox("Vận động (M)", options=[6,5,4,3,2,1], format_func=lambda x: f"{x} — " + {6:"Làm theo mệnh lệnh",5:"Định vị đau",4:"Rút khi đau",3:"Gập bất thường",2:"Duỗi",1:"Không vận động"}[x])
        gcs_sub = st.form_submit_button("Tính GCS")

    gcs_total = gcs_e + gcs_v + gcs_m
    if gcs_total <= 8: gcs_category = "Nặng (thường hôn mê) — GCS ≤ 8"
    elif 9 <= gcs_total <= 12: gcs_category = "Trung bình — GCS 9–12"
    else: gcs_category = "Nhẹ — GCS ≥ 13"

    st.subheader("Kết quả GCS")
    st.write(f"Điểm: **{gcs_total}**  (E{gcs_e} V{gcs_v} M{gcs_m})")
    st.write("Phân loại mức độ:", gcs_category)

# ----------------------------
# 3) Braden Scale
# ----------------------------
with tabs[2]:
    st.header("Braden Scale (Nguy cơ loét tỳ)")
    st.markdown("Nhập điểm từng mục; tổng 6–23. **Điểm thấp → nguy cơ cao**.")

    with st.form("braden_form"):
        b_sensory = st.selectbox("1. Cảm nhận (Sensory)", options=[1,2,3,4])
        b_moisture = st.selectbox("2. Ẩm ướt (Moisture)", options=[1,2,3,4])
        b_activity = st.selectbox("3. Hoạt động (Activity)", options=[1,2,3,4])
        b_mobility = st.selectbox("4. Vận động (Mobility)", options=[1,2,3,4])
        b_nutrition = st.selectbox("5. Dinh dưỡng (Nutrition)", options=[1,2,3,4])
        b_friction = st.selectbox("6. Ma sát & trượt (Friction & Shear)", options=[1,2,3])
        braden_sub = st.form_submit_button("Tính Braden")

    braden_total = b_sensory + b_moisture + b_activity + b_mobility + b_nutrition + b_friction
    if braden_total <= 12: braden_risk = "Nguy cơ cao"
    elif 13 <= braden_total <= 14: braden_risk = "Nguy cơ trung bình"
    elif 15 <= braden_total <= 18: braden_risk = "Nguy cơ nhẹ"
    else: braden_risk = "Không có nguy cơ rõ rệt"

    st.subheader("Kết quả Braden")
    st.write(f"Tổng điểm: **{braden_total}** (6–23)")
    st.write("Phân loại:", braden_risk)
    if show_details:
        st.write(f"- Cảm nhận: {b_sensory}, Ẩm ướt: {b_moisture}, Hoạt động: {b_activity}")
        st.write(f"- Vận động: {b_mobility}, Dinh dưỡng: {b_nutrition}, Ma sát: {b_friction}")

# ----------------------------
# 4) VIP Score
# ----------------------------
with tabs[3]:
    st.header("VIP Score (Viêm tiêm truyền)")
    st.markdown("Đánh giá vị trí catheter/IV: điểm 0–5. VIP ≥2 → cân nhắc rút cannula.")

    with st.form("vip_form"):
        vip_choice = st.selectbox("Chọn mô tả phù hợp:", options=[
            ("0","0 — IV bình thường, không viêm"),
            ("1","1 — Đau nhẹ hoặc đỏ gần IV"),
            ("2","2 — Đau, đỏ, phù (viêm sớm)"),
            ("3","3 — Đau, đỏ, phù, tĩnh mạch nổi cứng"),
            ("4","4 — Như trên + sốt"),
            ("5","5 — Viêm nặng, có mủ hoặc nhiễm trùng")
        ], format_func=lambda x: x[1])
        vip_sub = st.form_submit_button("Tính VIP")

    vip_score = int(vip_choice[0])
    if vip_score >= 2: vip_action = "Cân nhắc rút cannula và báo bác sĩ (VIP ≥ 2)."
    elif vip_score == 1: vip_action = "Theo dõi chặt chẽ; kiểm tra thường xuyên."
    else: vip_action = "Không có dấu hiệu viêm; tiếp tục theo dõi."

    st.subheader("Kết quả VIP")
    st.write(f"VIP score: **{vip_score}**")
    st.write(vip_action)

# ----------------------------
# Tóm tắt nhanh
# ----------------------------
st.markdown("---")
st.header("Tóm tắt nhanh")
st.write(f"- Morse: {morse_score} → **{morse_risk}**")
st.write(f"- GCS: {gcs_total} → **{gcs_category}**")
st.write(f"- Braden: {braden_total} → **{braden_risk}**")
st.write(f"- VIP: {vip_score} → {vip_action}")

st.info("Lưu ý: Ứng dụng này chỉ **tính và hiển thị kết quả** dựa trên tiêu chuẩn. Tuân thủ hướng dẫn và chính sách của cơ sở y tế.")
