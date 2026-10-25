# بدّل هذا السطرين مؤقتاً لو ما عندك openpyxl
# with pd.ExcelWriter(...) -> استخدم CSV
st.download_button("✅ إنجاز رسمي", data=enjaz_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"Enjaz_{len(df)}.csv", mime="text/csv", use_container_width=True, type="primary")
