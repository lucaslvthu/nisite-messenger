import streamlit as st
from datetime import datetime

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="Nisite Messenger", page_icon="💬", layout="centered")

# Giả lập cơ sở dữ liệu tin nhắn và bạn bè trong Session State
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'friends' not in st.session_state:
    st.session_state.friends = ["Admin", "Bạn thân", "Người lạ"]
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# CSS để tạo giao diện giống App di động
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    .chat-bubble-user { background-color: #dcf8c6; padding: 10px; border-radius: 15px; margin-bottom: 10px; text-align: right; border: 1px solid #c7edba; }
    .chat-bubble-other { background-color: white; padding: 10px; border-radius: 15px; margin-bottom: 10px; text-align: left; border: 1px solid #e1e1e1; }
    .taskbar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; padding: 10px; display: flex; justify-content: space-around; border-top: 1px solid #ddd; z-index: 100; }
    .main-container { margin-bottom: 80px; }
    </style>
    """, unsafe_allow_html=True)

# 2. GIAO DIỆN ĐĂNG NHẬP
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #075e54;'>Nisite</h1>", unsafe_allow_html=True)
    with st.container():
        st.info("Ứng dụng không xác thực danh tính. Chỉ cần nhập tên để bắt đầu.")
        name = st.text_input("Tên đăng nhập (Username)")
        pwd = st.text_input("Mật khẩu", type="password")
        if st.button("Bắt đầu trò chuyện", use_container_width=True, type="primary"):
            if name and pwd:
                st.session_state.user_name = name
                st.session_state.logged_in = True
                st.rerun()

# 3. GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP)
else:
    # Thanh Taskbar dưới cùng
    tab_selection = st.sidebar.radio("Menu", ["💬 Nhắn tin", "👤 Tài khoản"], label_visibility="collapsed")

    # --- MỤC NHẮN TIN ---
    if "Nhắn tin" in tab_selection:
        st.markdown(f"### 💬 Trò chuyện (Chào {st.session_state.user_name})")
        
        # Chọn bạn bè để nhắn
        target_friend = st.selectbox("Chọn bạn bè để nhắn tin:", st.session_state.friends)
        
        st.divider()
        
        # Hiển thị khung chat
        chat_placeholder = st.container(height=400)
        with chat_placeholder:
            for msg in st.session_state.messages:
                if msg['sender'] == st.session_state.user_name:
                    st.markdown(f"<div class='chat-bubble-user'><b>Bạn:</b> {msg['text']}<br><small>{msg['time']}</small></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-bubble-other'><b>{msg['sender']}:</b> {msg['text']}<br><small>{msg['time']}</small></div>", unsafe_allow_html=True)

        # Ô nhập tin nhắn
        with st.form("send_message", clear_on_submit=True):
            user_msg = st.text_input("Nhập tin nhắn...", placeholder="Nhắn gì đó...")
            if st.form_submit_button("Gửi"):
                if user_msg:
                    new_msg = {
                        "sender": st.session_state.user_name,
                        "text": user_msg,
                        "time": datetime.now().strftime("%H:%M")
                    }
                    st.session_state.messages.append(new_msg)
                    st.rerun()

    # --- MỤC TÀI KHOẢN (Giống Nisite trước đó) ---
    else:
        st.markdown("### 👤 Cài đặt tài khoản")
        with st.expander("📝 Thông tin cá nhân"):
            st.write(f"Tên người dùng: **{st.session_state.user_name}**")
            st.text_input("Thay đổi tên hiển thị")
            st.button("Lưu thay đổi")

        with st.expander("👥 Quản lý bạn bè"):
            new_friend = st.text_input("Nhập tên người dùng để kết bạn")
            if st.button("Gửi lời mời kết bạn"):
                st.success(f"Đã gửi lời mời tới {new_friend}")

        with st.expander("⚙️ Cài đặt hệ thống"):
            st.radio("Giao diện", ["Sáng", "Tối"])
            if st.button("Xóa tài khoản", type="secondary"):
                st.warning("Hành động này sẽ xóa toàn bộ dữ liệu.")
            
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

# 4. LƯU Ý CHO VIỆC DÙNG CHUNG VỚI BẠN BÈ
# Để bạn bè có thể nhắn tin cho nhau thật sự, bạn cần triển khai (deploy) code này lên internet.