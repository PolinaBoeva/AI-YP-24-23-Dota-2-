import streamlit as st
from client import ModelsAPIClient, DataAPIClient
from config import get_config
import streamlit_logging

logger = streamlit_logging.get_logger(__name__)


def init_streamlit_app():
    st.set_page_config(
        page_title="Предсказательные модели для DotA 2",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="auto",
    )
    if "models_api_client" not in st.session_state:
        st.session_state.models_api_client = ModelsAPIClient(
            get_config().client_config.fastapi_host, get_config().client_config.fastapi_port
        )
    if "data_api_client" not in st.session_state:
        st.session_state.data_api_client = DataAPIClient(
            get_config().client_config.fastapi_host, get_config().client_config.fastapi_port
        )
    if "models" not in st.session_state:
        st.session_state.models = []
    if "account_ids" not in st.session_state:
        try:
            account_ids_response = st.session_state.data_api_client.get_account_ids()
            st.session_state.account_ids = account_ids_response["account_ids"]
        except Exception as e:
            logger.error(f"Ошибка при получении account_ids: {e}")


def main():
    init_streamlit_app()

    pages = [
        st.Page("pages/eda.py", title="EDA", icon="📊", url_path="/eda"),
        st.Page("pages/fit.py", title=" Обучение модели", icon="🧠", url_path="/fit"),
        st.Page("pages/model_info.py", title="Информация о модели", icon="📖", url_path="/model_info"),
        st.Page("pages/predict.py", title="Предсказания", icon="🔮", url_path="/predict"),
    ]
    navigation = st.navigation(pages)
    navigation.run()


if __name__ == "__main__":
    main()
