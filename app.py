# app.py
# Streamlit app: Morse + GCS + Braden + VIP (hoàn chỉnh, trực quan, tiếng Việt)
# Chạy: pip install streamlit && streamlit run app.py

import streamlit as st

# ----------------------------
# Cấu hình trang
# ----------------------------
st.set_page_config(page_title="Công cụ đánh giá cho điều dưỡng", layout="wide")
st.title("Công cụ đánh giá cho điều dưỡng")
st.markdown(
    "Công cụ này chỉ **tính toán và hiển thị kết quả**, không lưu dữ liệu. "
    "Sử dụng nhanh tại giường được xây dựng bởi **TS.ĐD Lê Quốc Dũng**, Khoa Điều dưỡng - KTYH, Trường Cao đẳng Y tế Đồng Tháp."
)

st.sidebar.header("Tùy chọn")
show_details = st.sidebar.checkbox("Hiện chi tiết từng tiêu chí", value=True)
st.sidebar.caption("Phiên bản: 1.4 — Không lưu, không gửi dữ liệu.")

# Tabs cho từng thang đánh giá
tabs = st.tabs(["Nguy cơ té ngã (Morse)", "Đánh giá hôn mê (Glasgow)", "Nguy cơ loét tỳ (Braden)", "Viêm tĩnh mạch (VIP)"])

# ----------------------------
# Khởi tạo session_state mặc định để tránh NameError
for key in ["morse_score", "morse_risk", "morse_details",
            "gcs_total", "gcs_category", "gcs_e", "gcs_v", "gcs_m",
            "braden_total", "braden_risk", "b_values",
            "vip_score", "vip_action"]:
    if key not in st.session_state:
        if "details" in key or "b_values" in key:
            st.session_state[key] = {}
        elif "score" in key or "total" in key or key in ["gcs_e","gcs_v","gcs_m"]:
            st.session_state[key] = 0
        else:
            st.session_state[key] = "Chưa tính"

# ----------------------------
# 1) Morse Fall Scale
# ----------------------------
with tabs[0]:
    st.header("Nguy cơ té ngã (Morse)")
    st.markdown("Chọn các mục phù hợp với người bệnh:")

    with st.form("morse_form"):
        col1, col2 = st.columns(2)
        with col1:
            morse_q1 = st.radio("1. Tiền sử té ngã", ("Không", "Có — té ngã trong 3 tháng"))
            morse_q2 = st.radio("2. Chẩn đoán phụ (≥2 bệnh?)hoặc dùng thuốc hạ HA, gây nghiện", ("Không", "Có"))
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
        score = 0
        details = []
        if morse_q1.startswith("Có"): score += 25; details.append(("Tiền sử té ngã",25))
        else: details.append(("Tiền sử té ngã",0))
        if morse_q2.startswith("Có"): score += 15; details.append(("Chẩn đoán phụ",15))
        else: details.append(("Chẩn đoán phụ",0))
        if morse_q3.startswith("Không"): score += 0; details.append(("Dụng cụ",0))
        elif morse_q3.startswith("Nạng") or morse_q3.startswith("Xe lăn"): score += 15; details.append(("Dụng cụ",15))
        else: score += 30; details.append(("Dụng cụ",30))
        if morse_q4.startswith("Có"): score += 20; details.append(("Truyền dịch/IV",20))
        else: details.append(("Truyền dịch/IV",0))
        if morse_q5.startswith("Bình thường"): score += 0; details.append(("Dáng đi",0))
        elif morse_q5.startswith("Yếu"): score += 10; details.append(("Dáng đi",10))
        else: score += 20; details.append(("Dáng đi",20))
        if morse_q6.startswith("Quên"): score += 15; details.append(("Tinh thần",15))
        else: details.append(("Tâm thần",0))

        if score >= 45: risk = "Nguy cơ té ngã cao"
        elif score >= 25: risk = "Nguy cơ té ngã trung bình"
        else: risk = "Nguy cơ té ngã thấp"

        st.session_state.morse_score = score
        st.session_state.morse_risk = risk
        st.session_state.morse_details = details

    st.subheader("Kết quả Morse")
    st.metric("Tổng điểm Morse", st.session_state.morse_score)
    st.write("Mức nguy cơ:", st.session_state.morse_risk)
    if show_details:
        st.write("Chi tiết điểm (tiêu chí: điểm):")
        for k,v in st.session_state.morse_details.items() if isinstance(st.session_state.morse_details, dict) else st.session_state.morse_details:
            st.write(f"- {k}: {v}")

# ----------------------------
# 2) Glasgow Coma Scale (GCS)
# ----------------------------
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
        total = gcs_e + gcs_v + gcs_m
        st.session_state.gcs_total = total
        st.session_state.gcs_e = gcs_e
        st.session_state.gcs_v = gcs_v
        st.session_state.gcs_m = gcs_m

        if total <= 3: category = "Hôn mê rất sâu — GCS ≤ 3"
        elif 4<=total <= 8: category = "Rối loạn ý thức nặng (Hôn mê sâu) — GCS ≤ 8"
        elif 9 <= total <= 12: category = "Rối loạn ý thức trung bình — GCS 9–12"
        elif 13 <= total <= 14: category = "Rối loạn ý thức nhẹ — GCS 13–14"
        else: category = "Bình thường — GCS = 15"
        st.session_state.gcs_category = category

    st.subheader("Kết quả GCS")
    st.write(f"Điểm: **{st.session_state.gcs_total}**  "
             f"(E{st.session_state.gcs_e} V{st.session_state.gcs_v} M{st.session_state.gcs_m})")
    st.write("Phân loại mức độ:", st.session_state.gcs_category)

# ----------------------------
# 3) Braden Scale
# ----------------------------
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
        total = sum([int(val.split(" — ")[0]) for val in b_values.values()])
        st.session_state.braden_total = total
        st.session_state.b_values = b_values

        if total <= 12: risk = "Nguy cơ cao"
        elif 13 <= total <= 14: risk = "Nguy cơ trung bình"
        elif 15 <= total <= 18: risk = "Nguy cơ nhẹ"
        else: risk = "Không có nguy cơ rõ rệt"
        st.session_state.braden_risk = risk

    st.subheader("Kết quả Braden")
    st.write(f"Tổng điểm: **{st.session_state.braden_total}** (6–23)")
    st.write("Phân loại:", st.session_state.braden_risk)
    if show_details:
        for k,v in st.session_state.b_values.items():
            st.write(f"- {k}: {v}")

# ----------------------------
# 4) VIP Score
# ----------------------------
with tabs[3]:
    st.header("VIP Score (Viêm tiêm truyền)")
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
        score = int(vip_choice[0])
        st.session_state.vip_score = score

        if score >= 4: action = "Thay đường truyền, căn nhắc sử dụng kháng sinh, cấy máu, ghi HSBA, điều trị."
        elif score >= 2: action = "Thay đường truyền, ghi HSBA, căn nhắc điều trị (VIP ≥ 2)."
        elif score == 1: action = "Theo dõi chặt chẽ; kiểm tra thường xuyên ít nhất 6 giờ/lần."
        else: action = "Không có dấu hiệu viêm; tiếp tục theo dõi."
        st.session_state.vip_action = action

    st.subheader("Kết quả VIP")
    st.write(f"VIP score: **{st.session_state.vip_score}**")
    st.write(st.session_state.vip_action)

# ----------------------------
# Tóm tắt nhanh trực quan
# ----------------------------
st.markdown("---")
st.header("Tóm tắt nhanh")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Morse", st.session_state.morse_score, st.session_state.morse_risk)
col2.metric("GCS", st.session_state.gcs_total, st.session_state.gcs_category)
col3.metric("Braden", st.session_state.braden_total, st.session_state.braden_risk)
col4.metric("VIP", st.session_state.vip_score, st.session_state.vip_action)

st.info("Lưu ý: Ứng dụng này chỉ **tính và hiển thị kết quả** dựa trên tiêu chuẩn. Tuân thủ hướng dẫn và chính sách Cơ sở Y tế.")
