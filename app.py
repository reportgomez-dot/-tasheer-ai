# === نظام الرسائل الداخلي - زي Gmail - داخل موقعك ===
if 'messages_db' not in st.session_state:
    st.session_state['messages_db'] = []  # {from, to, subject, body, time, read}

def send_internal_message(from_user, to_user, subject, body):
    st.session_state['messages_db'].append({
        "from": from_user,
        "to": to_user,
        "subject": subject,
        "body": body,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "read": False,
        "id": len(st.session_state['messages_db']) + 1
    })

# === واجهة الرسائل - للعميل ===
if st.session_state['username'] != "admin":
    st.markdown("---")
    st.markdown("### 📧 صندوق الرسائل - كلم الأدمن مباشرة من هنا - زي Gmail")
    
    msg_tab1, msg_tab2 = st.tabs(["📥 الوارد", "📤 ارسل رسالة"])
    
    with msg_tab1:
        my_messages = [m for m in st.session_state['messages_db'] if m['to'] == st.session_state['username'] or m['to'] == "all"]
        if my_messages:
            for msg in reversed(my_messages):
                with st.expander(f"{'🔴' if not msg['read'] else '✅'} من: {msg['from']} - {msg['subject']} - {msg['time']}"):
                    st.write(f"**من:** {msg['from']}")
                    st.write(f"**الموضوع:** {msg['subject']}")
                    st.write(f"**الرسالة:** {msg['body']}")
                    st.write(f"**الوقت:** {msg['time']}")
                    if st.button(f"رد", key=f"reply_{msg['id']}"):
                        st.session_state['reply_to'] = msg['from']
        else:
            st.info("📭 لا يوجد رسائل - الأدمن بيرسل لك هنا التحديثات والعروض")
    
    with msg_tab2:
        st.markdown(f"**إرسال للأدمن - {st.session_state['username']} → admin**")
        subject = st.text_input("الموضوع", placeholder="مثال: استفسار عن الباقة", key="user_subject")
        body = st.text_area("الرسالة", placeholder="اكتب رسالتك هنا...", key="user_body")
        if st.button("📤 ارسل للأدمن الآن", type="primary", use_container_width=True):
            if subject and body:
                send_internal_message(st.session_state['username'], "admin", subject, body)
                st.success("✅ تم الإرسال - الأدمن بيرد عليك هنا في صندوق الوارد")
                st.balloons()
            else:
                st.error("اكتب الموضوع والرسالة")

# === واجهة الرسائل - للأدمن ===
else:
    st.markdown("---")
    st.markdown("### 📧 نظام الرسائل - Gmail داخل موقعك - تكلم كل العملاء")
    
    admin_msg_tab1, admin_msg_tab2, admin_msg_tab3 = st.tabs(["📥 رسائل العملاء", "📤 ارسل لعميل", "📢 ارسل للكل"])
    
    with admin_msg_tab1:
        admin_inbox = [m for m in st.session_state['messages_db'] if m['to'] == "admin"]
        st.metric("رسائل جديدة", len([m for m in admin_inbox if not m['read']]))
        if admin_inbox:
            for msg in reversed(admin_inbox):
                with st.expander(f"{'🔴 جديد' if not msg['read'] else '✅'} من: {msg['from']} - {msg['subject']} - {msg['time']}"):
                    st.write(f"**من:** {msg['from']} - {msg['from']}@client.com")
                    st.write(f"**الموضوع:** {msg['subject']}")
                    st.write(f"**الرسالة:** {msg['body']}")
                    # زر رد سريع
                    reply_body = st.text_area(f"رد على {msg['from']}", key=f"admin_reply_{msg['id']}")
                    if st.button(f"📤 رد على {msg['from']}", key=f"send_reply_{msg['id']}"):
                        if reply_body:
                            send_internal_message("admin", msg['from'], f"Re: {msg['subject']}", reply_body)
                            st.success(f"✅ رديت على {msg['from']}")
        else:
            st.info("📭 لا يوجد رسائل من العملاء الآن")
    
    with admin_msg_tab2:
        st.markdown("**ارسل رسالة لعميل محدد**")
        all_users = [u for u in st.session_state['users_db'].keys() if u != "admin"]
        if all_users:
            target_user = st.selectbox("اختر العميل", all_users)
            admin_subject = st.text_input("الموضوع", placeholder="مثال: تم تفعيل باقتك", key="admin_sub")
            admin_body = st.text_area("الرسالة", placeholder="مبروك تم تفعيل حسابك...", key="admin_body")
            if st.button(f"📤 ارسل لـ {target_user}", type="primary", use_container_width=True):
                if admin_subject and admin_body:
                    send_internal_message("admin", target_user, admin_subject, admin_body)
                    st.success(f"✅ أرسلت لـ {target_user}")
        else:
            st.warning("لا يوجد عملاء بعد")
    
    with admin_msg_tab3:
        st.markdown("**📢 رسالة جماعية - لكل العملاء - زي حملة ايميل**")
        broadcast_subject = st.text_input("موضوع الحملة", placeholder="مثال: عرض خاص - خصم 50% اليوم", key="broad_sub")
        broadcast_body = st.text_area("نص الحملة", placeholder="السلام عليكم عملاء TASHEER AI... اليوم عرض...", key="broad_body")
        if st.button("📢 ارسل للكل الآن", type="primary", use_container_width=True):
            if broadcast_subject and broadcast_body:
                send_internal_message("admin", "all", broadcast_subject, broadcast_body)
                st.success(f"✅ أرسلت لـ {len(all_users)} عميل - كلهم بيشوفونها في صندوق الوارد")
                st.balloons()
