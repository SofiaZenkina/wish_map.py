import streamlit as st
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация Firebase (замени 'path_to_your_service_account.json' на путь к твоему файлу с ключом)
if not firebase_admin._apps:
    cred = credentials.Certificate('path_to_your_service_account.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Цветовая схема
BACKGROUND_COLOR = "#fae7b5"
st.markdown(
    f"<style> .stApp {{ background-color: {BACKGROUND_COLOR}; }} </style>", unsafe_allow_html=True
)

# Авторизация пользователя
st.title("🔑 Авторизация")
user_email = st.text_input("Введите ваш email для входа:")

if user_email:
    user_doc = db.collection('users').document(user_email)
    user_data = user_doc.get()

    if not user_data.exists:
        user_doc.set({"wishes": []})

    st.success("✅ Успешный вход! Теперь вы можете добавлять и просматривать свои желания.")

    # Загрузка данных пользователя
    wishes = user_doc.get().to_dict().get('wishes', [])

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
                wishes.append(new_wish)
                user_doc.update({"wishes": wishes})
                st.success("✅ Желание успешно добавлено!")
            else:
                st.error("⚠️ Пожалуйста, введите описание желания.")

    # Вкладка для просмотра желаний
    with tabs[1]:
        st.title("Мои желания")
        if wishes:
            wishes_df = pd.DataFrame(wishes)
            st.dataframe(wishes_df, use_container_width=True)

            # Кнопка для печати (вывод только таблицы без лишнего текста)
            if st.button("Печать таблицы"):
                st.write(wishes_df.to_html(index=False), unsafe_allow_html=True)
        else:
            st.info("✨ Пока нет добавленных желаний. Добавьте их на вкладке 'Добавить желание'.")
else:
    st.info("Введите email для начала работы с картой желаний.")




