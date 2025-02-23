import streamlit as st
import pandas as pd
from datetime import datetime

# Цветовая схема
BUTTON_COLOR = "#fae7b5"
CUSTOM_CSS = f"""
    <style>
        div.stButton > button {{
            background-color: {BUTTON_COLOR} !important;
            color: black !important;
            border-radius: 5px;
            border: none;
        }}
    </style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Инициализация состояния сессии для хранения желаний
if 'wishes' not in st.session_state:
    st.session_state['wishes'] = []
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None

# Авторизация пользователя
if not st.session_state['user_email']:
    st.title("🔑 Авторизация")
    user_email = st.text_input("Введите ваш email для входа:")
    if st.button("Войти"):
        if user_email.strip():
            st.session_state['user_email'] = user_email.strip()
            st.success("✅ Успешный вход! Теперь вы можете добавлять и просматривать свои желания.")
            st.rerun()
        else:
            st.error("⚠️ Пожалуйста, введите корректный email.")
else:
    # Список категорий и месяцев
    categories = ["Внешность", "Отношения", "Здоровье", "Финансы", "Карьера", "Саморазвитие", "Путешествия", "Хобби", "Другое"]
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    # Создание вкладок
    tabs = st.tabs(["Добавить желание", "Мои желания"])

    # Вкладка для добавления желания
    with tabs[0]:
        st.title("🌟 Добавить желание")
        category = st.selectbox("Выберите категорию желания:", categories)
        month = st.selectbox("Выберите месяц для реализации:", months)
        description = st.text_input("Опишите вашу цель или желание:")

        if st.button("Добавить желание"):
            if description.strip():
                new_wish = {
                    "Желание": description.strip(),
                    "Категория": category,
                    "Месяц": month
                }
                st.session_state['wishes'].append(new_wish)
                st.success("✅ Желание успешно добавлено!")
            else:
                st.error("⚠️ Пожалуйста, введите описание желания.")

    # Вкладка для просмотра желаний
    with tabs[1]:
        st.title("📋 Мои желания")
        if st.session_state['wishes']:
            wishes_df = pd.DataFrame(st.session_state['wishes'])
            st.dataframe(wishes_df, use_container_width=True)

            # Кнопка для печати (выводит всплывающее окно с принтером для печати таблицы)
            if st.button("Печать таблицы"):
                st.markdown(
                    f"""
                    <script>
                        const printWindow = window.open('', '', 'height=600,width=800');
                        printWindow.document.write('<html><head><title>Печать таблицы</title></head><body>');
                        printWindow.document.write(`{wishes_df.to_html(index=False)}`);
                        printWindow.document.write('</body></html>');
                        printWindow.document.close();
                        printWindow.print();
                    </script>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("✨ Пока нет добавленных желаний. Добавьте их на вкладке 'Добавить желание'.")


