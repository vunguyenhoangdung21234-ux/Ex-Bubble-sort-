import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

# ====================== 1. CẤU HÌNH GIAO DIỆN CHUYÊN NGHIỆP ======================
st.set_page_config(page_title="Bubble Sort Analytics Pro", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .bar-container { display: flex; align-items: flex-end; justify-content: center; height: 350px; gap: 5px; padding: 20px; background: white; border-radius: 15px; }
    .log-box { height: 200px; overflow-y: auto; background: #262730; color: #00ff00; padding: 10px; font-family: 'Courier New', Courier, monospace; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# ====================== 2. KHỞI TẠO SESSION STATE ======================
if 'numbers' not in st.session_state:
    st.session_state.numbers = [random.randint(10, 100) for _ in range(15)]
if 'history_log' not in st.session_state:
    st.session_state.history_log = []
if 'stats' not in st.session_state:
    st.session_state.stats = {"swaps": 0, "comparisons": 0, "start_time": None}

# ====================== 3. THANH ĐIỀU HƯỚNG SIDEBAR ======================
with st.sidebar:
    st.title("⚙️ CẤU HÌNH")
    mode = st.radio("Chế độ nhập liệu", ["Ngẫu nhiên", "Tự nhập tay"])
    
    if mode == "Ngẫu nhiên":
        if st.button("🎲 Tạo 15 số mới"):
            st.session_state.numbers = [random.randint(10, 100) for _ in range(15)]
            st.session_state.history_log = []
            st.rerun()
    else:
        user_input = st.text_input("Nhập 15 số (cách nhau bởi dấu phẩy)", value=",".join(map(str, st.session_state.numbers)))
        if st.button("📥 Áp dụng dãy số"):
            try:
                new_list = [int(x.strip()) for x in user_input.split(",")]
                if len(new_list) == 15:
                    st.session_state.numbers = new_list
                    st.success("Đã cập nhật dãy số!")
                else:
                    st.error("Vui lòng nhập đúng 15 số.")
            except:
                st.error("Định dạng không hợp lệ.")

    st.divider()
    speed = st.slider("⏱️ Tốc độ chạy (giây/bước)", 0.05, 2.0, 0.3)
    st.info("Mẹo: Tốc độ thấp giúp bạn quan sát rõ từng lần tráo đổi.")

# ====================== 4. THUẬT TOÁN & LOGIC CHÍNH ======================
def bubble_sort_engine(arr):
    steps = []
    n = len(arr)
    temp_arr = arr.copy()
    swaps = 0
    comparisons = 0
    
    steps.append({"data": temp_arr.copy(), "msg": "Bắt đầu thuật toán", "highlight": [], "done": []})

    for i in range(n):
        swapped_in_round = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if temp_arr[j] > temp_arr[j + 1]:
                temp_arr[j], temp_arr[j + 1] = temp_arr[j + 1], temp_arr[j]
                swaps += 1
                swapped_in_round = True
                steps.append({
                    "data": temp_arr.copy(),
                    "msg": f"Hoán đổi {temp_arr[j+1]} ↔️ {temp_arr[j]}",
                    "highlight": [j, j + 1],
                    "done": list(range(n - i, n)),
                    "stats": {"swaps": swaps, "comparisons": comparisons}
                })
        
        steps.append({
            "data": temp_arr.copy(),
            "msg": f"Số {temp_arr[n-i-1]} đã 'nổi' lên vị trí cuối.",
            "highlight": [],
            "done": list(range(n - i - 1, n)),
            "stats": {"swaps": swaps, "comparisons": comparisons}
        })
        
        if not swapped_in_round:
            steps.append({
                "data": temp_arr.copy(),
                "msg": "Dãy đã được sắp xếp hoàn toàn (Tối ưu dừng sớm).",
                "highlight": [],
                "done": list(range(n)),
                "stats": {"swaps": swaps, "comparisons": comparisons}
            })
            break
    return steps

# ====================== 5. HIỂN THỊ GIAO DIỆN CHÍNH ======================
st.header("📊 Mô Phỏng Sắp Xếp Nổi Bọt (Bubble Sort)")

# Khu vực chỉ số (Metrics)
m1, m2, m3 = st.columns(3)
placeholder_swaps = m1.empty()
placeholder_comps = m2.empty()
m3.metric("Số phần tử", "15")

# Khu vực biểu đồ chính
placeholder_bars = st.empty()

# Khu vực giải thích và Nhật ký (Logs)
col_left, col_right = st.columns([2, 1])

with col_left:
    placeholder_msg = st.empty()
    if st.button("🚀 CHẠY THUẬT TOÁN", type="primary"):
        start_time = time.time()
        all_steps = bubble_sort_engine(st.session_state.numbers)
        
        for step in all_steps:
            # Cập nhật Bars
            with placeholder_bars.container():
                st.markdown('<div class="bar-container">', unsafe_allow_html=True)
                cols = st.columns(15)
                for idx, val in enumerate(step["data"]):
                    color = "#3498db"
                    if idx in step["highlight"]: color = "#e74c3c"
                    elif idx in step.get("done", []): color = "#2ecc71"
                    
                    with cols[idx]:
                        st.markdown(f"""
                            <div style="background-color: {color}; height: {val*3}px; width: 100%; border-radius: 5px;"></div>
                            <p style="text-align: center; font-size: 10px;">{val}</p>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Cập nhật tin nhắn và stats
            placeholder_msg.info(f"💡 **Trạng thái:** {step['msg']}")
            if "stats" in step:
                placeholder_swaps.metric("Lượt tráo đổi (Swaps)", step["stats"]["swaps"])
                placeholder_comps.metric("Lượt so sánh", step["stats"]["comparisons"])
                st.session_state.history_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {step['msg']}")
            
            time.sleep(speed)
        
        end_time = time.time()
        st.success(f"Hoàn thành trong {round(end_time - start_time, 2)} giây!")
        st.balloons()

with col_right:
    st.subheader("📟 Terminal Log")
    log_content = "<br>".join(st.session_state.history_log[::-1]) # Hiện log mới nhất lên đầu
    st.markdown(f'<div class="log-box">{log_content}</div>', unsafe_allow_html=True)

# ====================== 6. PHÂN TÍCH ĐỘ PHỨC TẠP & LÝ THUYẾT ======================
st.divider()
st.subheader("📚 Phân tích Khoa học Máy tính")

tab1, tab2, tab3 = st.tabs(["🕒 Thời gian tính", "📦 Không gian tính", "⚖️ So sánh thuật toán"])

with tab1:
    st.markdown("""
    Độ phức tạp thời gian (Time Complexity) của Bubble Sort:
    * **Trường hợp tốt nhất:** $O(n)$ khi mảng đã sắp xếp.
    * **Trung bình / Xấu nhất:** $O(n^2)$. Với $n=15$, số lần so sánh tối đa là $15 \times 14 / 2 = 105$.
    """)
    

with tab2:
    st.markdown("""
    Độ phức tạp không gian (Space Complexity):
    * **$O(1)$**: Thuật toán này là **In-place**, nghĩa là nó không cần tạo thêm mảng phụ, chỉ tốn một biến tạm để hoán đổi.
    """)

with tab3:
    compare_data = {
        "Thuật toán": ["Bubble Sort", "Selection Sort", "Quick Sort"],
        "Độ phức tạp": ["$O(n^2)$", "$O(n^2)$", "$O(n \log n)$"],
        "Ưu điểm": ["Dễ hiểu, Ổn định", "Ít lượt tráo đổi hơn", "Nhanh nhất cho dữ liệu lớn"],
        "Tính ổn định": ["Có", "Không", "Không"]
    }
    st.table(pd.DataFrame(compare_data))

st.caption(f"Phiên bản: 2.0.1 | Được cập nhật vào: {datetime.now().strftime('%Y')}")