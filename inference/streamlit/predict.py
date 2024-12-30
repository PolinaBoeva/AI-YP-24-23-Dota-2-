import streamlit as st
import pandas as pd
from client import ModelsAPIClient, DataAPIClient
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def predict_model(models_api_client, data_api_client):
    """Функция для получения предсказаний."""
    st.header("Предсказания на основе обученной модели")
    logger.info("Инициализация процесса получения предсказаний.")

    # Блок загрузки тренировочных данных
    st.subheader("Загрузка тренировочных данных")
    uploaded_file = st.file_uploader("📥 Загрузите CSV файл с данными", type="csv")

    if uploaded_file is not None:
        # Показать загруженные данные
        data = pd.read_csv(uploaded_file)
        st.session_state.uploaded_data = data
        st.write("Вот ваши загруженные данные:")
        st.dataframe(data)
        logger.info("Загруженные данные успешно отображены.")

    # Получение account IDs
    try:
        account_ids_response = data_api_client.get_account_ids()  # Обратите внимание на использование data_api_client
        if account_ids_response:
            account_ids = account_ids_response['account_ids']
            logger.info(f"Account IDs успешно получены: {account_ids}.")
        else:
            st.error("Не удалось загрузить account IDs.")
            logger.error("Ответ пустой при получении Account IDs.")
            st.stop()
    except Exception as e:
        st.error(f"Возникла ошибка при получении Account IDs: {str(e)}.")
        logger.error(f"Ошибка при получении Account IDs: {str(e)}.")
        st.stop()

    selected_account_ids = st.multiselect("Выберите Account IDs для предсказания", account_ids)

    if st.button("🔮 Получить предсказания"):
        predictions = []
        for account_id in selected_account_ids:
            data = {"account_id": account_id}  # Подготовка данных для запроса
            try:
                prediction_response = models_api_client.predict(data)
                predictions.append(prediction_response)
                logger.info(f"Получено предсказание для Account ID: {account_id}.")
            except Exception as e:
                st.error(f"Ошибка при получении предсказания для ID {account_id}: {str(e)}.")
                logger.error(f"Ошибка при получении предсказания для Account ID {account_id}: {str(e)}.")

        if predictions:
            st.write("Предсказания:")
            for prediction in predictions:
                st.json(prediction)
            logger.info("Все предсказания успешно отображены.")

    # Загрузка тестового датасета
    uploaded_test_file = st.file_uploader("📤 Загрузите тестовый датасет (CSV)", type=["csv"])
    if uploaded_test_file is not None and st.button("Отправить тестовый файл для предсказаний"):
        try:
            prediction_csv_response = models_api_client.predict_csv(uploaded_test_file)
            st.write("Предсказания из CSV файла:")
            st.json(prediction_csv_response)
            logger.info("Предсказания из тестового CSV файла успешно отображены.")
        except Exception as e:
            st.error(f"Ошибка при отправке тестового файла: {str(e)}.")
            logger.error(f"Ошибка при отправке тестового файла: {str(e)}.")
