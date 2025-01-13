import streamlit as st
import time

from client import ModelsAPIClient
from utils import get_ridge_params, get_catboost_params
import streamlit_logging

logger = streamlit_logging.get_logger("fit_page")


def run_fit_page():
    st.header("Обучение модели")
    logger.info("Инициализация процесса обучения модели.")

    models_api_client: ModelsAPIClient = st.session_state.models_api_client

    model_type_input = st.selectbox("Выберите модель", ["⚖️ Ridge Classifier", "🧠 CatBoost Classifier"])
    logger.info(f"Выбрана модель: {model_type_input}")

    st.subheader("Гиперпараметры модели")

    # Выбор гиперпараметров в зависимости от типа модели
    if model_type_input == "⚖️ Ridge Classifier":
        model_type = "RidgeClassifier"
        hyperparameters = get_ridge_params()
        logger.info(f"Параметры Ridge Classifier: {hyperparameters}")
    elif model_type_input == "🧠 CatBoost Classifier":
        model_type = "CatBoost"
        hyperparameters = get_catboost_params()
        logger.info(f"Параметры CatBoost Classifier: {hyperparameters}")

    model_id = st.text_input("Введите ID модели", value="model")

    if st.button("🚀 Обучить модель"):
        fit_request = {
            "model_type": model_type,
            "model_id": model_id,
            "hyperparameters": hyperparameters,
        }
        # Запуск обучения модели
        logger.info("Запуск обучения модели.")
        start_time = time.time()
        fit_response = models_api_client.fit_model(fit_request)
        st.success("Обучение модели начато!")

        # Проверка статуса обучения
        while True:
            status_response = models_api_client.get_fit_status(model_id)
            st.write(f"Статус обучения: {status_response['status']}")
            logger.info(f"Текущий статус обучения: {status_response['status']}")
            if status_response["status"] in ["Success", "Failed"]:
                break
            time.sleep(2)  # Задержка перед следующей проверкой

        end_time = time.time()
        st.write(f"⏳ Время обучения составило: {end_time - start_time:.2f} сек")
        logger.info(f"Обучение модели завершено. Время обучения: {end_time - start_time:.2f} секунд.")


if __name__ == "__page__":
    run_fit_page()
