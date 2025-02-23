import streamlit as st
import pandas as pd
from datetime import datetime

# Цветовая схема
BACKGROUND_COLOR = "#fae7b5"
st.markdown(
    f"<style> .stApp {{ background-color: {BACKGROUND_COLOR}; }} </style>", unsafe_allow_html=True
)

# Инициализация состояния сессии для хранения желаний
if 'wishes' not in st.session_state:
    st.session_state['wishes'] = []
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None

# Авторизация пользователя
st.title("🔑 Авторизация")
user_email = st.text_input("Введите ваш email для входа:", value=st.session_state['user_email'] or "")

if st.button("Войти"):
    if user_email.strip():
        st.session_state['user_email'] = user_email.strip()
        st.success("✅ Успешный вход! Теперь вы можете добавлять и просматривать свои желания.")
    else:
        st.error("⚠️ Пожалуйста, введите корректный email.")

if st.session_state['user_email']:
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

            # Кнопка для печати (вывод только таблицы без лишнего текста)
            if st.button("Печать таблицы"):
                st.write(wishes_df.to_html(index=False), unsafe_allow_html=True)
        else:
            st.info("✨ Пока нет добавленных желаний. Добавьте их на вкладке 'Добавить желание'.")
else:
    st.info("Введите email для начала работы с картой желаний.")



