import os
import requests
import json
from dotenv import load_dotenv
import streamlit as st
from config import DifyApiKeySettings

load_dotenv("env/.env")

dify_api_key = DifyApiKeySettings()
# DIFY_API_KEY = os.environ.get('DIFY_API_KEY')
DIFY_BASE_URL = 'http://localhost/v1'
DIFY_USER = "Kazuki"

def upload_file(file):
    target_url = f"{DIFY_BASE_URL}/files/upload"

    headers = {
        "Authorization": f"Bearer {dify_api_key.csv_to_json}",
    }

    try:
        response = requests.post(
            target_url,
            headers=headers,
            files={"file": (file.name, file.read(), file.type)},
            data={"user": DIFY_USER},
        )

        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"アップロードエラー: {response.status_code}")
            return None

    except Exception as e:
        st.error(f"予期しないエラーが発生しました: {str(e)}")
        return None


def convert_csv_to_json(file_id):
    '''xのブックマークのcsvファイルをJson形式に変換'''
    target_url = f"{DIFY_BASE_URL}/workflows/run"
    headers = {
        "Authorization": f"Bearer {dify_api_key.csv_to_json}",
        "Content-Type": "application/json"
    }

    input = {
        # Dify ワークフローの入力フィールド名と一致させる
        "bookmark_csv": {
            "type": "document",
            "transfer_method": "local_file",
            "upload_file_id": file_id
        }
    }

    payload = {
        "inputs": input,
        "response_mode": "blocking",
        "user": DIFY_USER
    }

    try:
        response = requests.post(target_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"ワークフロー実行エラー: {str(e)}")
        return None


def categorized_json(file_id):
    '''xのブックマークのJsonファイルをカテゴリごとに分類'''
    target_url = f"{DIFY_BASE_URL}/workflows/run"
    headers = {
        "Authorization": f"Bearer {dify_api_key.categorize_json}",
        "Content-Type": "application/json"
    }

    input = {
        # Dify ワークフローの入力フィールド名と一致させる
        "bookmark_csv": {
            "type": "document",
            "transfer_method": "local_file",
            "upload_file_id": file_id
        }
    }

    payload = {
        "inputs": input,
        "response_mode": "blocking",
        "user": DIFY_USER
    }

    try:
        response = requests.post(target_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"ワークフロー実行エラー: {str(e)}")
        return None



# 実行プロック

uploaded_file = st.file_uploader(
    "ファイルをアップロードしてください",
    type=["csv", "json"]
)

print(uploaded_file)

# if uploaded_file is not None:
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("ファイル名:", uploaded_file.name)
    # with col2:
    #     st.image(uploaded_file, use_container_width=True)

if st.button("ファイルをアップロード"):
    if uploaded_file.type == "text/csv":
        response = upload_file(uploaded_file)
        st.write(f'アップロード完了: ファイルID - {response["id"]}')

        with st.spinner("ワークフローを実行中..."):
            run_workflow_result = convert_csv_to_json(response["id"])
        
        bookmarks_json = run_workflow_result["data"]["outputs"]["bookmarks_json"]

    elif uploaded_file.type == "application/json":
        bookmarks_json_str = uploaded_file.getvalue().decode("utf-8")
        bookmarks_json = json.loads(bookmarks_json_str)

    # for bookmark_json in bookmarks_json:
        



    # print("########################")
    # print(bookmark_json_str)
    # print("########################")
    # bookmark_json = json.loads(bookmark_json_str)

    # print("########################")
    # print(bookmark_json)
    # print("########################")
    
    # レスポンスから画像の解析結果を取得して表示
    # st.write(bookmark_json["bookmarks"])
    st.write(bookmarks_json)


    