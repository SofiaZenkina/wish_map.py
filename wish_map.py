import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Цветовая схема и стили
BUTTON_COLOR = "#fae7b5"
HEADER_FONT = "Lletraferida"

CUSTOM_CSS = f"""
    <style>
        /* Вкладки при наведении и активные */
        .stTabs [role="tab"]:hover {{
            background-color: {BUTTON_COLOR} !important;
            color: black !important;
        }}

        .stTabs [role="tab"][aria-selected="true"] {{
            background-color: {BUTTON_COLOR} !important;
            color: black !important;
        }}

        /* Заголовки */
        h1, h2, h3, h4, h5, h6 {{
            font-family: '{HEADER_FONT}', sans-serif;
        }}

        /* Надпись справа сверху */
        .custom-header {{
            position: absolute;
            top: 10px;
            right: 20px;
            font-family: '{HEADER_FONT}', sans-serif;
            font-style: italic;
            font-size: 16px;
            color: black;
        }}
    </style>
"""

# Добавление пользовательских стилей и надписи сверху
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown('<div class="custom-header">Ваши цели ближе, чем вам кажется...</div>', unsafe_allow_html=True)

# Инициализация состояния сессии для хранения желаний и пользователя
if 'wishes' not in st.session_state:
    st.session_state['wishes'] = []
if 'user_credentials' not in st.session_state:
    st.session_state['user_credentials'] = None

# Авторизация с паролем
if not st.session_state['user_credentials']:
    st.title("Авторизация")
    user_email = st.text_input("Введите ваш email:")
    user_password = st.text_input("Введите пароль:", type="password")

    if st.button("Войти"):
        if user_email.strip() and user_password.strip():
            st.session_state['user_credentials'] = {
                'email': user_email.strip(),
                'password': user_password.strip()
            }
            st.success("Успешный вход! Теперь вы можете работать с картой желаний.")
            st.rerun()
        else:
            st.error("Пожалуйста, введите корректные данные.")
else:
    # Список категорий и месяцев
    categories = ["Внешность", "Отношения", "Здоровье", "Финансы", "Карьера", "Саморазвитие", "Путешествия", "Хобби", "Другое"]
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    # Создание вкладок
    tabs = st.tabs(["Добавить желание", "Мои желания"])

    # Вкладка для добавления желания
    with tabs[0]:
        st.header("Добавить желание")
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
                st.success("Желание успешно добавлено!")
            else:
                st.error("Пожалуйста, введите описание желания.")

    # Вкладка для просмотра желаний
    with tabs[1]:
        st.header("Мои желания")
        if st.session_state['wishes']:
            wishes_df = pd.DataFrame(st.session_state['wishes'])
            st.dataframe(wishes_df, use_container_width=True)

            # Скачивание в формате Excel
            excel_buffer = BytesIO()
            wishes_df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            st.download_button(
                label="Скачать таблицу в Excel",
                data=excel_buffer,
                file_name="мои_желания.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Скачивание в формате PDF
            import pdfkit
            html_content = wishes_df.to_html(index=False)
            pdf_buffer = BytesIO()
            pdfkit.from_string(html_content, pdf_buffer)
            pdf_buffer.seek(0)
            st.download_button(
                label="Скачать таблицу в PDF",
                data=pdf_buffer,
                file_name="мои_желания.pdf",
                mime="application/pdf"
            )
        else:
            st.info("Пока нет добавленных желаний. Добавьте их на вкладке 'Добавить желание'.")
