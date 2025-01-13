import streamlit as st

from client import ModelsAPIClient
import streamlit_logging

logger = streamlit_logging.get_logger("model_info_page")


def run_model_info_page():
    st.header("Информация о модели")

    models_api_client: ModelsAPIClient = st.session_state.models_api_client

    if st.button("Загрузить список обученных моделей"):
        model_list_response = models_api_client.get_model_list()
        if model_list_response:
            st.session_state.models = model_list_response["models"]  # Сохраняем список моделей
            st.write("Обученные модели:")
            st.write(st.session_state.models)

    model_id_input = st.selectbox("Выберите ID модели", st.session_state.models)

    if st.button("📖 Получить информацию о модели"):
        model_info = models_api_client.get_model_info(model_id_input)
        if model_info:
            st.write("📝 Информация о модели:")
            st.json(model_info)
        else:
            st.error("❌ Эта модель не существует.")

    if st.button("Активировать выбранную модель"):
        activate_response = models_api_client.activate_model(model_id_input)
        st.write("Модель активирована")


if __name__ == "__page__":
    run_model_info_page()
