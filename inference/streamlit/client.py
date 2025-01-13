import requests

import streamlit_logging

logger = streamlit_logging.get_logger(__name__)


class ModelsAPIClient:
    def __init__(self, host: str, port: int):
        logger.info("Инициализация ModelsAPIClient для работы с моделями.")
        self.base_url = f"{host}:{port}/api/v1/models"
        logger.info(f"Базовый URL ModelsAPIClient: {self.base_url}")

    def fit_model(self, params: dict):
        """Отправка параметров для обучения модели."""
        logger.info("Отправка параметров для обучения модели.")
        response = requests.post(f"{self.base_url}/fit", json=params)
        logger.info(f"Ответ от сервера: {response.status_code}, {response.json()}")
        return response.json()

    def get_fit_status(self, model_id: str):
        """Получение статуса асинхронной задачи обучения."""
        logger.info("Получение статуса обучения модели.")
        response = requests.get(f"{self.base_url}/fit/status", params={"model_id": model_id})
        logger.info(f"Ответ от сервера: {response.status_code}, {response.json()}")
        return response.json()

    def get_model_list(self):
        """Получение списка всех обученных моделей."""
        logger.info("Запрос списка всех обученных моделей.")
        response = requests.get(f"{self.base_url}/list")
        logger.info(f"Ответ от сервера: {response.status_code}, {response.json()}")
        return response.json()

    def activate_model(self, model_id: str):
        """Установка активной модели для прогноза."""
        logger.info(f"Активация модели с ID: {model_id}.")
        response = requests.put(f"{self.base_url}/activate", params={"model_id": model_id})
        logger.info(f"Ответ от сервера: {response.status_code}, {response.json()}")
        return response.json()

    def predict(self, data: dict):
        """Прогноз исхода на основе выбранных данных. Используется активированная модель."""
        logger.info("Отправка данных для прогноза.")
        response = requests.post(f"{self.base_url}/predict", json=data)
        logger.info(f"Ответ от сервера: {response.status_code}, {response.json()}")
        return response.json()

    def predict_csv(self, csv_data):
        """Прогноз исхода на основе CSV-файла."""
        logger.info("Отправка CSV-файла для прогноза.")
        response = requests.post(f"{self.base_url}/predict_csv", files={"request": csv_data})
        logger.info(f"Получены предсказания для {len(response.json()['predictions']['predictions'])} матчей.")
        return response.json()

    def get_model_info(self, model_id: str):
        """Получение информации об обученной модели."""
        logger.info(f"Запрос информации о модели с ID: {model_id}.")
        response = requests.get(f"{self.base_url}/model_info", params={"model_id": model_id})
        logger.info(f"Ответ от сервера: {response.status_code}, {response.json()}")
        return response.json()


class DataAPIClient:
    def __init__(self, host: str, port: int):
        logger.info("Инициализация DataAPIClient для работы с данными.")
        self.base_url = f"{host}:{port}/api/v1/data"
        logger.info(f"Базовый URL DataAPIClient: {self.base_url}")

    def get_account_ids(self):
        """Получение уникальных account_id из API."""
        logger.info("Запрос уникальных account_id из API.")
        response = requests.get(f"{self.base_url}/account_ids")
        if response.status_code == 200:
            logger.info("Account IDs успешно получены.")
            return response.json()  # Предполагается, что API возвращает список account_ids
        else:
            logger.error("Не удалось получить Account IDs из API.")
            raise Exception("Не удалось получить Account IDs из API.")
