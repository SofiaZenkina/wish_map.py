import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Цветовая схема и стили
BUTTON_COLOR = "#fae7b5"
HEADER_FONT = "Lletraferida"
INFO_COLOR = "#d0e6a5"  # Мягкий зеленый для уведомлений

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

        /* Кнопки без цвета при нажатии */
        div.stButton > button {{
            background-color: transparent !important;
            color: black !important;
            border: 1px solid {BUTTON_COLOR};
            border-radius: 5px;
        }}

        /* Заголовки */
        h1, h2, h3, h4, h5, h6 {{
            font-family: '{HEADER_FONT}', sans-serif;
        }}

        /* Надпись слева сверху */
        .custom-header {{
            position: absolute;
            top: 10px;
            left: 20px;
            font-family: '{HEADER_FONT}', sans-serif;
            font-style: italic;
            font-size: 16px;
            color: {BUTTON_COLOR};
        }}

        /* Уведомления */
        .stAlert {{
            background-color: {INFO_COLOR} !important;
            color: black !important;
        }}
    </style>
"""

# Добавление пользовательских стилей и надписи сверху
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown('<div class="custom-header">ваши цели ближе, чем вам кажется...</div>', unsafe_allow_html=True)

# Инициализация состояния для хранения желаний
if 'wishes' not in st.session_state:
    st.session_state['wishes'] = []

# Список категорий и месяцев
categories = ["Внешность", "Отношения", "Здоровье", "Финансы", "Карьера", "Саморазвитие", "Путешествия", "Хобби", "Другое"]
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# Создание вкладок
tabs = st.tabs(["Добавить желание", "Мои желания", "Печать таблицы"])

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
            st.warning("Пожалуйста, введите описание желания.")

# Вкладка для просмотра желаний
with tabs[1]:
    st.header("Мои желания")
    if st.session_state['wishes']:
        wishes_df = pd.DataFrame(st.session_state['wishes'])
        st.dataframe(wishes_df, use_container_width=True)
    else:
        st.info("Пока нет добавленных желаний. Добавьте их на вкладке 'Добавить желание'.")

# Вкладка для печати таблицы
with tabs[2]:
    st.header("Печать таблицы")
    if st.session_state['wishes']:
        wishes_df = pd.DataFrame(st.session_state['wishes'])

        # Скачивание в формате Excel
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            wishes_df.to_excel(writer, index=False, sheet_name="Желания")
        excel_buffer.seek(0)
        st.download_button(
            label="Скачать таблицу в Excel",
            data=excel_buffer,
            file_name="мои_желания.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Скачивание в формате PDF с использованием reportlab
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(200, 750, "Мои желания")

        # Заголовки таблицы
        x_start, y_start = 50, 720
        row_height = 20
        col_widths = [150, 150, 150]

        for i, header in enumerate(wishes_df.columns):
            pdf.drawString(x_start + sum(col_widths[:i]), y_start, header)

        # Содержимое таблицы
        for index, row in wishes_df.iterrows():
            y_pos = y_start - ((index + 1) * row_height)
            for i, item in enumerate(row):
                pdf.drawString(x_start + sum(col_widths[:i]), y_pos, str(item))

        pdf.showPage()
        pdf.save()
        pdf_buffer.seek(0)

        st.download_button(
            label="Скачать таблицу в PDF",
            data=pdf_buffer,
            file_name="мои_желания.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Пока нет добавленных желаний для печати.")
