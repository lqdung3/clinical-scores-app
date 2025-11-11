# app.py
# Streamlit app: Morse + GCS + Braden + VIP (giao diện trực quan, có màu sắc)
# Chạy: pip install streamlit && streamlit run app.py

import streamlit as st

# ----------------------------
# Cấu hình trang
# ----------------------------
st.set_page_config(page_title="Công cụ đánh giá cho điều dưỡng", layout="wide")
st.title("Công cụ đánh giá cho điều dưỡng")
st.markdown("Công cụ này chỉ **tính toán và hiển thị kết quả**, không lưu dữ liệu. \
             Sử dụng nhanh tại giường được xây dựng bởi **TS.ĐD Lê Quốc Dũng**, Khoa Điều dưỡng - KTYH, Trường Cao đẳng Y tế Đồng Tháp.")

st.sidebar.header("Tùy chọn")
show_details = st.sidebar.checkbox("Hiện chi tiết từng tiêu chí", value=True)
st.sidebar.caption("Phiên bản: 1.3 — Không lưu, không gửi dữ liệu.")

# Tabs cho từng thang đánh giá
tabs = st.tabs(["Nguy cơ té ngã (Morse)", "Đánh giá hôn mê (Glasgow)", "Nguy cơ loét tỳ (Braden)", "Viêm tĩnh mạch (VIP)"])

# ----------------------------
# Khởi tạo mặc định các biến
morse_score = 0
morse_risk = "Chưa tính"
morse_details = []

gcs_total = 0
gcs_category = "Chưa tính"
gcs_e, gcs_v, gcs_m = 0, 0, 0

braden_total = 0
braden_risk = "Chưa tính"
b_values = {}

vip_score = 0
vip_action = "Chưa tính"

# ----------------------------
# 1) Morse Fall Scale
with tabs[0]:
    st.header("Nguy cơ té ngã (Morse)")
    st.markdown("Chọn các mục phù hợp với người bệnh:")

    with st.form("morse_form"):
        col1, col2 = st.columns(2)
        with col1:
            morse_q1 = st.radio("1. Tiền sử té ngã", ("Không", "Có — té ngã trong 3 tháng"))
            morse_q2 = st.radio("2. Chẩn đoán phụ (≥2 bệnh?) hoặc dùng thuốc hạ HA, gây nghiện", ("Không", "Có"))
            morse_q3 = st.selectbox("3. Dụng cụ hỗ trợ đi lại",
                                    ("Không / nằm nghỉ",
                                     "Xe lăn/ Nạng / gậy / khung tập đi",
                                     "Bám / tựa vào bàn ghế / bờ tường để đi"))
        with col2:
            morse_q4 = st.radio("4. Đang truyền dịch / thuốc tĩnh mạch", ("Không", "Có"))
            morse_q5 = st.selectbox("5. Dáng đi / cách di chuyển",
                                    ("Bình thường / nằm nghỉ / bất động", "Yếu", "Khó khăn / loạng choạng"))
            morse_q6 = st.radio("6. Tình trạng tinh thần", ("Định hướng được bản thân", "Quên, lú lẫn"))
        morse_submitted = st.form_submit_button("Tính điểm Morse")
    if morse_submitted:
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
        if morse_q6.startswith("Quên"): morse_score += 15; morse_details.append(("Tinh thần",15))
        else: morse_details.append(("Tâm thần",0))
        if morse_score >= 45: morse_risk = "Nguy cơ té ngã cao"
        elif morse_score >= 25: morse_risk = "Nguy cơ té ngã trung bình"
        else: morse_risk = "Nguy cơ té ngã thấp"

    st.subheader("Kết quả Morse")
    st.metric("Tổng điểm Morse", morse_score)
    st.write("Mức nguy cơ:", morse_risk)
    if show_details:
        st.write("Chi tiết điểm (tiêu chí: điểm):")
        for k,v in morse_details: st.write(f"- {k}: {v}")

# ----------------------------
# 2) Glasgow Coma Scale (GCS)
with tabs[1]:
    st.header("Đánh giá hôn mê (Glasgow)")
    st.markdown("Nhập điểm từng phần (E = Mở mắt, V = Lời nói, M = Vận động). Tổng 3–15.")

    with st.form("gcs_form"):
        gcs_e = st.selectbox("Mở mắt (E)", options=[4,3,2,1],
                             format_func=lambda x: f"{x} — " + {4:"Tự mở mắt",3:"Mở khi gọi",2:"Mở khi đau",1:"Không mở"}[x])
        gcs_v = st.selectbox("Lời nói (V)", options=[5,4,3,2,1],
                             format_func=lambda x: f"{x} — " + {5:"Bình thường",4:"Lẫn lộn",3:"Nói không phù hợp",2:"Âm thanh không hiểu",1:"Không nói"}[x])
        gcs_m = st.selectbox("Vận động (M)", options=[6,5,4,3,2,1],
                             format_func=lambda x: f"{x} — " + {6:"Làm theo mệnh lệnh",5:"Định vị đau",4:"Rút khi đau",3:"Gập bất thường",2:"Duỗi",1:"Không vận động"}[x])
        gcs_sub = st.form_submit_button("Tính GCS")

    if gcs_sub:
        gcs_total = gcs_e + gcs_v + gcs_m
        if gcs_total <= 3: gcs_category = "Hôn mê rất sâu — GCS ≤ 3"
        elif 4<=gcs_total <= 8: gcs_category = "Rối loạn ý thức nặng (Hôn mê sâu) — GCS ≤ 8"
        elif 9 <= gcs_total <= 12: gcs_category = "Rối loạn ý thức trung bình — GCS 9–12"
        elif 13 <= gcs_total <= 14: gcs_category = "Rối loạn ý thức nhẹ — GCS 9–12"
        else: gcs_category = "Bình thường — GCS = 15"

    st.subheader("Kết quả GCS")
    st.write(f"Điểm: **{gcs_total}**  (E{gcs_e} V{gcs_v} M{gcs_m})")
    st.write("Phân loại mức độ:", gcs_category)

# ----------------------------
# 3) Braden Scale
with tabs[2]:
    st.header("Nguy cơ loét tỳ (Braden)")
    st.markdown("Nhập điểm từng mục; tổng 6–23. **Điểm càng thấp → nguy cơ càng cao**.")

    braden_domains = {
        "Nhận biết cảm giác (Sensory)": {1: "Hoàn toàn không phản ứng",2: "Phản ứng hạn chế",3:"Phản ứng hơi hạn chế",4:"Phản ứng đầy đủ"},
        "Tình trạng da (Moisture)": {1:"Da luôn ẩm",2:"Da thường xuyên ẩm",3:"Da thỉnh thoảng ẩm",4:"Da hiếm khi ẩm"},
        "Hoạt động (Activity)": {1:"Hoàn toàn bất động",2:"Hạn chế vận động",3:"Di chuyển ít",4:"Hoạt động bình thường"},
        "Vận động (Mobility)": {1:"Không thể tự thay đổi tư thế",2:"Rất hạn chế",3:"Hạn chế vừa phải",4:"Bình thường"},
        "Dinh dưỡng (Nutrition)": {1:"Ăn rất ít hoặc không ăn",2:"Ăn kém",3:"Ăn đủ nhưng hạn chế",4:"Ăn bình thường"},
        "Ma sát & trượt (Friction & Shear)": {1:"Rất dễ bị trượt/ma sát",2:"Nguy cơ trượt/ma sát",3:"Rủi ro thấp"}
    }

    with st.form("braden_form"):
        b_values = {}
        for domain, options in braden_domains.items():
            opts = [f"{score} — {desc}" for score, desc in options.items()]
            b_values[domain] = st.selectbox(domain, opts, index=0)
        braden_sub = st.form_submit_button("Tính Braden")

    if braden_sub:
        braden_total = sum([int(val.split(" — ")[0]) for val in b_values.values()])
        if braden_total <= 12: braden_risk = "Nguy cơ cao"
        elif 13 <= braden_total <= 14: braden_risk = "Nguy cơ trung bình"
        elif 15 <= braden_total <= 18: braden_risk = "Nguy cơ nhẹ"
        else: braden_risk = "Không có nguy cơ rõ rệt"

    st.subheader("Kết quả Braden")
    st.write(f"Tổng điểm: **{braden_total}** (6–23)")
    st.write("Phân loại:", braden_risk)
    if show_details:
        for k,v in b_values.items():
            st.write(f"- {k}: {v}")

# ----------------------------
# 4) VIP Score
with tabs[3]:
    st.header("VIP Score (Viêm tĩnh mạch)")
    st.markdown("Đánh giá vị trí catheter/IV: điểm 0–5. VIP ≥2 → cân nhắc rút cannula.")

    with st.form("vip_form"):
        vip_options = [
            ("0","0 — IV bình thường, không viêm"),
            ("1","1 — Đau nhẹ hoặc đỏ gần IV(Viêm sớm)"),
            ("2","2 — Có 2 dấu hiệu: Đau, đỏ, sưng (viêm sớm)"),
            ("3","3 — Tất cả dấu hiệu: Đau, đỏ, sưng, sờ cứng quanh chân kim (Trung bình)"),
            ("4","4 — Tất cả dấu hiệu + tĩnh mạch thành dây"),
            ("5","5 — Tất cả dấu hiệu + sốt / có mủ")
        ]
        vip_choice = st.selectbox("Chọn mô tả phù hợp:", vip_options, format_func=lambda x: x[1])
        vip_sub = st.form_submit_button("Tính VIP")

    if vip_sub:
        vip_score = int(vip_choice[0])
        if vip_score >= 4: vip_action = "Thay đường truyền, căn nhắc dùng kháng sinh, cấy máu, ghi HSBA, điều trị."
        elif vip_score >= 2: vip_action = "Thay đường truyền, ghi HSBA, cân nhắc điều trị (VIP ≥ 2)."
        elif vip_score == 1: vip_action = "Theo dõi chặt chẽ; kiểm tra ít nhất 6 giờ/lần."
        else: vip_action = "Không có dấu hiệu viêm; tiếp tục theo dõi."

    st.subheader("Kết quả VIP")
    st.write(f"VIP score: **{vip_score}**")
    st.write(vip_action)

# ----------------------------
# Tóm tắt nhanh trực quan
st.markdown("---")
st.header("Tóm tắt nhanh (trực quan)")

def color_label(text, level):
    colors = {"high":"#ff4c4c", "medium":"#ffa500", "low":"#00cc44", "default":"#999999"}
    return f"<span style='color:{colors.get(level,'#000')}; font-weight:bold'>{text}</span>"

# Morse
m_level = "default"
if morse_submitted:
    if "cao" in morse_risk.lower(): m_level="high"
    elif "trung bình" in morse_risk.lower(): m_level="medium"
    else: m_level="low"
st.markdown(f"- Morse: {morse_score if morse_submitted else 0} → {color_label(morse_risk, m_level)}", unsafe_allow_html=True)

# GCS
g_level = "default"
if gcs_sub:
    if "rất sâu" in gcs_category.lower() or "nặng" in gcs_category.lower(): g_level="high"
    elif "trung bình" in gcs_category.lower() or "nhẹ" in gcs_category.lower(): g_level="medium"
    else: g_level="low"
st.markdown(f"- GCS: {gcs_total if gcs_sub else 0} → {color_label(gcs_category, g_level)}", unsafe_allow_html=True)

# Braden
b_level = "default"
if braden_sub:
    if "cao" in braden_risk.lower(): b_level="high"
    elif "trung bình" in braden_risk.lower(): b_level="medium"
    else: b_level="low"
st.markdown(f"- Braden: {braden_total if braden_sub else 0} → {color_label(braden_risk, b_level)}", unsafe_allow_html=True)

# VIP
v_level = "default"
if vip_sub:
    if vip_score >= 4: v_level="high"
    elif vip_score >= 2: v_level="medium"
    else: v_level="low"
st.markdown(f"- VIP: {vip_score if vip_sub else 0} → {color_label(vip_action, v_level)}", unsafe_allow_html=True)

st.info("Lưu ý: Ứng dụng này chỉ **tính và hiển thị kết quả** dựa trên tiêu chuẩn. Tuân thủ hướng dẫn và chính sách cơ sở y tế.")
