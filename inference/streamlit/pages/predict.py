import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import streamlit as st

from client import ModelsAPIClient, DataAPIClient
import streamlit_logging

logger = streamlit_logging.get_logger("predict_page")


def run_predict_page():
    st.header("Предсказания на основе обученной модели")
    logger.info("Инициализация процесса получения предсказаний.")

    models_api_client: ModelsAPIClient = st.session_state.models_api_client
    data_api_client: DataAPIClient = st.session_state.data_api_client

    try:
        if "account_ids" in st.session_state:
            account_ids = st.session_state.account_ids
        else:
            logger.info("Не удалось получить Account IDs из кэша, выполняется запрос к API.")
            account_ids_response = data_api_client.get_account_ids()
            account_ids = account_ids_response["account_ids"]
            st.session_state.account_ids = account_ids
    except Exception as e:
        st.error(f"Возникла ошибка при получении Account IDs: {str(e)}.")
        logger.error(f"Ошибка при получении Account IDs: {str(e)}.")

    prediction_regime = st.radio(
        "Выберите режим", ["Предсказание для одного матча", "Предсказание для нескольких матчей"]
    )

    if prediction_regime == "Предсказание для одного матча":
        st.subheader("Выбор аккаунтов для команды Radiant")
        radiant_selected_ids = st.multiselect("Выберите до 5 Account IDs для Radiant", account_ids, max_selections=5)

        st.subheader("Выбор аккаунтов для команды Dire")
        dire_selected_ids = st.multiselect("Выберите до 5 Account IDs для Dire", account_ids, max_selections=5)

        if st.button("🔮 Получить предсказания"):
            if len(radiant_selected_ids) != 5 or len(dire_selected_ids) != 5:
                st.error("Пожалуйста, выберите ровно 5 Account IDs для каждой команды.")
                logger.warning("Необходимо выбрать ровно 5 Account IDs для одной или обеих команд.")
                return

            data = {
                "radiant_team": [
                    {"account_id": int(account_id), "hero_name": "Pudge"} for account_id in radiant_selected_ids
                ],
                "dire_team": [
                    {"account_id": int(account_id), "hero_name": "Pudge"} for account_id in dire_selected_ids
                ],
            }

            try:
                prediction_response = models_api_client.predict(data)
                st.json(prediction_response)
                logger.info("Получено предсказание для команд Radiant и Dire.")
            except Exception as e:
                st.error(f"Ошибка при получении предсказания: {str(e)}.")
                logger.error(f"Ошибка при получении предсказания: {str(e)}.")
    else:
        test_data_file = st.file_uploader("Загрузите файл с данными", type=["csv"])
        if test_data_file is not None:
            data = test_data_file.read()

        test_targets_file = st.file_uploader("Загрузите файл с целевыми значениями", type=["csv"])

        if test_data_file is not None:
            if st.button("🔮 Получить предсказания"):
                try:
                    prediction_response = models_api_client.predict_csv(data)
                    st.json(prediction_response)
                    logger.info(f"Получены предсказания для {len(prediction_response["predictions"]["prediction_probas"])} матчей.")

                    if test_targets_file is not None:
                        targets = pd.read_csv(test_targets_file)["radiant_win"]
                        pred_probas = prediction_response["predictions"]["prediction_probas"]
                        preds = [1 if proba > 0.5 else 0 for proba in pred_probas]
                        metrics = {
                            "accuracy": accuracy_score(targets, preds),
                            "f1": f1_score(targets, preds),
                            "roc_auc": roc_auc_score(targets, pred_probas),
                        }
                        st.json(metrics)
                except Exception as e:
                    st.error(f"Ошибка при получении предсказания: {str(e)}.")
                    logger.error(f"Ошибка при получении предсказания: {str(e)}.")


if __name__ == "__page__":
    run_predict_page()
