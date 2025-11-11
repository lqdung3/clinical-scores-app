# app.py
# Streamlit app: Morse + GCS + Braden + VIP
# Chạy: pip install streamlit && streamlit run app.py

import streamlit as st

st.set_page_config(page_title="Clinical Quick Scores", layout="centered")

st.title("Clinical Quick Scores — Morse • GCS • Braden • VIP")
st.markdown("Ứng dụng nhỏ: **chỉ tính toán và hiển thị kết quả**, không lưu dữ liệu. \
             Thiết kế cho sử dụng nhanh tại giường (web).")

st.sidebar.header("Tùy chọn hiển thị")
show_details = st.sidebar.checkbox("Hiện chi tiết từng tiêu chí", value=True)
st.sidebar.caption("Phiên bản: 1.0 — Không lưu, không gửi dữ liệu.")

# ----------------------------
# 1) Morse Fall Scale
# ----------------------------
st.header("1. Morse Fall Scale (Nguy cơ té ngã)")
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
    extra_ah = st.checkbox("Bệnh nhân đang dùng thuốc hạ huyết áp (modifier +10 điểm)?", value=False)
    morse_submitted = st.form_submit_button("Tính Morse")

# scoring Morse
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

if extra_ah:
    morse_score += 10
    morse_details.append(("Modifier: Thuốc hạ huyết áp",10))

# Morse interpretation
if morse_score >= 45:
    morse_risk = "Nguy cơ cao"
elif morse_score >= 25:
    morse_risk = "Nguy cơ trung bình"
else:
    morse_risk = "Nguy cơ thấp"

st.subheader("Kết quả Morse")
st.metric("Tổng điểm Morse", morse_score)
st.write("Mức nguy cơ:", morse_risk)
if show_details:
    st.write("Chi tiết điểm (tiêu chí: điểm):")
    for k,v in morse_details:
        st.write(f"- {k}: {v}")

st.markdown("---")

# ----------------------------
# 2) Glasgow Coma Scale (GCS)
# ----------------------------
st.header("2. Glasgow Coma Scale (GCS)")
st.markdown("Nhập điểm từng phần (E = Eye, V = Verbal, M = Motor). Tổng 3–15.")

with st.form("gcs_form"):
    gcs_e = st.selectbox("Eye opening (E)", options=[4,3,2,1], format_func=lambda x: f"{x} — " + {4:"Spontaneously",3:"To voice",2:"To pain",1:"No response"}[x])
    gcs_v = st.selectbox("Verbal response (V)", options=[5,4,3,2,1], format_func=lambda x: f"{x} — " + {5:"Oriented",4:"Confused",3:"Inappropriate words",2:"Incomprehensible sounds",1:"No verbal response"}[x])
    gcs_m = st.selectbox("Motor response (M)", options=[6,5,4,3,2,1], format_func=lambda x: f"{x} — " + {6:"Obeys commands",5:"Localizes pain",4:"Withdraws",3:"Abnormal flexion",2:"Extension",1:"No movement"}[x])
    gcs_sub = st.form_submit_button("Tính GCS")

gcs_total = gcs_e + gcs_v + gcs_m
if gcs_total <= 8:
    gcs_category = "Nặng (thường xem là hôn mê) — GCS ≤ 8"
elif 9 <= gcs_total <= 12:
    gcs_category = "Trung bình — GCS 9–12"
else:
    gcs_category = "Nhẹ — GCS ≥ 13"

st.subheader("Kết quả GCS")
st.write(f"Điểm: **{gcs_total}**  (E{gcs_e} V{gcs_v} M{gcs_m})")
st.write("Phân loại mức độ:", gcs_category)
st.markdown("---")

# ----------------------------
# 3) Braden Scale (Pressure ulcer risk)
# ----------------------------
st.header("3. Braden Scale (Nguy cơ loét tỳ)")
st.markdown("Mỗi mục có thang điểm; tổng 6–23. **Điểm thấp → nguy cơ cao**.")

with st.form("braden_form"):
    b_sensory = st.selectbox("1. Sensory perception", options=[1,2,3,4], format_func=lambda x: f"{x}")
    b_moisture = st.selectbox("2. Moisture", options=[1,2,3,4], format_func=lambda x: f"{x}")
    b_activity = st.selectbox("3. Activity", options=[1,2,3,4], format_func=lambda x: f"{x}")
    b_mobility = st.selectbox("4. Mobility", options=[1,2,3,4], format_func=lambda x: f"{x}")
    b_nutrition = st.selectbox("5. Nutrition", options=[1,2,3,4], format_func=lambda x: f"{x}")
    b_friction = st.selectbox("6. Friction & Shear", options=[1,2,3], format_func=lambda x: f"{x}")
    braden_sub = st.form_submit_button("Tính Braden")

braden_total = b_sensory + b_moisture + b_activity + b_mobility + b_nutrition + b_friction

# Braden interpretation (common thresholds)
if braden_total <= 12:
    braden_risk = "Nguy cơ cao"
elif 13 <= braden_total <= 14:
    braden_risk = "Nguy cơ trung bình"
elif 15 <= braden_total <= 18:
    braden_risk = "Nguy cơ nhẹ"
else:
    braden_risk = "Không có nguy cơ rõ rệt"

st.subheader("Kết quả Braden")
st.write(f"Tổng điểm: **{braden_total}** (6–23).")
st.write("Phân loại:", braden_risk)
if show_details:
    st.write("Chi tiết từng mục:")
    st.write(f"- Sensory: {b_sensory}, Moisture: {b_moisture}, Activity: {b_activity}")
    st.write(f"- Mobility: {b_mobility}, Nutrition: {b_nutrition}, Friction: {b_friction}")
st.markdown("---")

# ----------------------------
# 4) VIP score (Visual Infusion Phlebitis)
# ----------------------------
st.header("4. VIP Score (Visual Infusion Phlebitis)")
st.markdown("Đánh giá vị trí catheter/IV: điểm 0–5. Thông thường VIP ≥2 → cân nhắc rút cannula.")

with st.form("vip_form"):
    vip_choice = st.selectbox("Chọn mô tả phù hợp:", options=[
        ("0", "0 — IV site appears healthy (no signs of phlebitis)"),
        ("1", "1 — Slight pain or redness near IV site"),
        ("2", "2 — Pain, redness, oedema (possible early phlebitis)"),
        ("3", "3 — Pain, redness, swelling & palpable venous cord"),
        ("4", "4 — Above + pyrexia"),
        ("5", "5 — Severe phlebitis with signs of infection / purulence")
    ], format_func=lambda x: x[1])
    vip_sub = st.form_submit_button("Tính VIP")
vip_score = int(vip_choice[0])
if vip_score >= 2:
    vip_action = "Cân nhắc rút cannula và báo bác sĩ (VIP ≥ 2)."
elif vip_score == 1:
    vip_action = "Theo dõi chặt chẽ; kiểm tra thường xuyên."
else:
    vip_action = "Không có dấu hiệu viêm tiêm truyền; tiếp tục theo dõi."

st.subheader("Kết quả VIP")
st.write(f"VIP score: **{vip_score}**")
st.write(vip_action)
st.markdown("---")

# ----------------------------
# Quick summary block
# ----------------------------
st.header("Tóm tắt nhanh (summary)")
st.write(f"- Morse: {morse_score} → **{morse_risk}**")
st.write(f"- GCS: {gcs_total} → **{gcs_category}**")
st.write(f"- Braden: {braden_total} → **{braden_risk}**")
st.write(f"- VIP: {vip_score} → {vip_action}")

st.info("Lưu ý: Ứng dụng này chỉ **tính và hiển thị kết quả** dựa trên luật điểm tiêu chuẩn. Luôn tuân theo hướng dẫn và chính sách của cơ sở y tế nơi bạn làm việc.")

# References (ngắn)
st.markdown("**Tài liệu tham khảo (tóm tắt):**")
st.markdown("- Morse Fall Scale: tài liệu hướng dẫn và ngưỡng phân loại thông dụng. (Morse MFS training modules).")
st.markdown("- Glasgow Coma Scale: StatPearls / NCBI (GCS 3–15).")
st.markdown("- Braden Scale: hướng dẫn Braden (tổng 6–23; điểm thấp → nguy cơ cao).")
st.markdown("- VIP (Visual Infusion Phlebitis) score: công cụ đánh giá phlebitis; VIP ≥2 thường yêu cầu rút cannula.")
