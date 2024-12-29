import streamlit as st
from client import ModelsAPIClient, DataAPIClient
from fit import fit_model
from predict import predict_model
from model_info import display_model_info


def main():
    # Инициализация API
    host = "http://****"  # Замените на рабочий хост
    port = 8000  # Замените на рабочий порт
    models_api_client = ModelsAPIClient(host, port)
    data_api_client = DataAPIClient(host, port)

    # Заголовок приложения
    st.title("Модель по анализу данных")

    # Инициализация состояния сессии
    if 'page' not in st.session_state:
        st.session_state.page = "🔄 Обучение модели"

    if 'models' not in st.session_state:
        st.session_state.models = []  # Инициализация модели

    # Создание вертикального меню с кнопками
    st.sidebar.header("Меню быстрого доступа")
    if st.sidebar.button("🔄 Обучение модели"):
        st.session_state.page = "🔄 Обучение модели"
    if st.sidebar.button("ℹ️ Информация о модели"):
        st.session_state.page = "ℹ️ Информация о модели"
    if st.sidebar.button("🔮 Предсказания"):
        st.session_state.page = "🔮 Предсказания"

    # Определение действия на основе текущей страницы
    if st.session_state.page == "🔄 Обучение модели":
        fit_model(models_api_client)
    elif st.session_state.page == "🔮 Предсказания":
        predict_model(models_api_client, data_api_client)  # Передаем оба клиента
    elif st.session_state.page == "ℹ️ Информация о модели":
        display_model_info(models_api_client)


if __name__ == "__main__":
    main()