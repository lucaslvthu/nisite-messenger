import streamlit as st
from datetime import datetime

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="Nisite Messenger", page_icon="💬")

# Giả lập Database dùng chung trên máy chủ
@st.cache_resource
def get_database():
    return {
        "users": {},       # Lưu {username: password}
        "friendships": [], # Lưu các cặp bạn bè {user1, user2}
        "messages": []     # Lưu tin nhắn toàn cục
    }

db = get_database()

# 2. XỬ LÝ ĐĂNG NHẬP / ĐĂNG KÝ
if 'current_user' not in st.session_state:
    st.title("🌐 Nisite Messenger")
    mode = st.radio("Chế độ", ["Đăng nhập", "Đăng ký"], horizontal=True)
    user = st.text_input("Tên đăng nhập").lower().strip()
    pwd = st.text_input("Mật khẩu", type="password")

    if mode == "Đăng ký":
        if st.button("Tạo tài khoản"):
            if user in db["users"]:
                st.error("Tên này đã có người dùng! Hãy chọn tên khác.")
            elif user and pwd:
                db["users"][user] = pwd
                st.success("Đăng ký xong! Mời bạn chuyển sang Đăng nhập.")
    else:
        if st.button("Vào Nisite"):
            if user in db["users"] and db["users"][user] == pwd:
                st.session_state.current_user = user
                st.rerun()
            else:
                st.error("Sai thông tin đăng nhập.")

# 3. GIAO DIỆN CHÍNH
else:
    me = st.session_state.current_user
    tab_chat, tab_account = st.tabs(["💬 Nhắn tin", "👤 Tài khoản"])

    with tab_chat:
        # Mục Kết bạn
        st.subheader("👥 Kết bạn")
        friend_name = st.text_input("Nhập chính xác tên bạn bè:").lower().strip()
        if st.button("Thêm bạn"):
            if friend_name == me:
                st.warning("Bạn không thể kết bạn với chính mình.")
            elif friend_name not in db["users"]:
                st.error("Không tìm thấy người dùng này.")
            else:
                if {me, friend_name} not in db["friendships"]:
                    db["friendships"].append({me, friend_name})
                    st.success(f"Đã kết bạn với {friend_name}!")
                else:
                    st.info("Hai bạn đã là bạn bè.")

        st.divider()
        
        # Mục Nhắn tin (Chỉ hiện người đã kết bạn)
        my_friends = [list(f - {me})[0] for f in db["friendships"] if me in f]
        if not my_friends:
            st.info("Chưa có bạn bè. Hãy kết bạn ở trên để nhắn tin.")
        else:
            chat_target = st.selectbox("Chọn người muốn nhắn:", my_friends)
            
            # Khung hiển thị chat
            chat_area = st.container(height=300, border=True)
            with chat_area:
                for m in db["messages"]:
                    if {m['from'], m['to']} == {me, chat_target}:
                        align = "right" if m['from'] == me else "left"
                        color = "#dcf8c6" if m['from'] == me else "#f0f0f0"
                        st.markdown(f"<div style='text-align: {align};'><div style='display: inline-block; background: {color}; padding: 8px 12px; border-radius: 15px; margin: 5px;'>{m['text']}</div></div>", unsafe_allow_html=True)

            # Ô gửi tin nhắn
            with st.form("send", clear_on_submit=True):
                txt = st.text_input("Nhập tin nhắn...")
                if st.form_submit_button("Gửi"):
                    if txt:
                        db["messages"].append({"from": me, "to": chat_target, "text": txt, "time": datetime.now()})
                        st.rerun()

    with tab_account:
        st.write(f"Đang dùng: **{me}**")
        if st.button("Đăng xuất"):
            del st.session_state.current_user
            st.rerun()
