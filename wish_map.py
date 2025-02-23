
import streamlit as st
from datetime import datetime

# Список категорий и месяцев
categories = ["Внешность", "Отношения", "Здоровье", "Финансы", "Карьера", "Саморазвитие", "Путешествия", "Хобби", "Другое"]
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# Streamlit интерфейс
st.title("Карта Желаний")
st.write("Выберите категорию и месяц для реализации ваших желаний.")

# Цветовая схема и стили
BUTTON_COLOR = "#fae7b5"
HEADER_FONT = "Lletraferida"
INFO_COLOR = "#d0e6a5"  # Мягкий зеленый для уведомлений

# Выбор категории и месяца
category = st.selectbox("Выберите категорию желания:", categories)
month = st.selectbox("Выберите месяц для реализации:", months)
description = st.text_input("Опишите вашу цель или желание:")

# Кнопка для добавления желания
if st.button("Добавить желание"):
    if description.strip():
        st.success(f"Желание добавлено! Категория: {category}, Месяц: {month}, Описание: {description}")
    else:
        st.error(" Пожалуйста, введите описание желания.")

# Отображение текущей даты
st.write(f"Сегодня: {datetime.now().strftime('%d.%m.%Y')}")
st.write("---")
st.write(" Добавьте столько желаний, сколько хотите и начните их реализацию!")

# Вкладка для скачивания таблицы
with tabs[2]:
    st.header("Скачать таблицу")
    if st.session_state['wishes']:
        wishes_df = pd.DataFrame(st.session_state['wishes'])

  # Скачивание в формате Word
        word_buffer = BytesIO()
        doc = Document()
        doc.add_heading("Мои желания", level=1)
        table = doc.add_table(rows=1, cols=len(wishes_df.columns))
        hdr_cells = table.rows[0].cells
        for i, column in enumerate(wishes_df.columns):
            hdr_cells[i].text = column

        for _, row in wishes_df.iterrows():
            row_cells = table.add_row().cells
            for i, item in enumerate(row):
                row_cells[i].text = str(item)

        doc.save(word_buffer)
        word_buffer.seek(0)

        st.download_button(
            label="Скачать в Word",
            data=word_buffer,
            file_name="мои_желания.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.info("Пока нет добавленных желаний для скачивания.")
