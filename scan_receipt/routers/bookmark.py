import ast
import json
from fastapi import FastAPI, File, UploadFile
from app import DifyModule

app = FastAPI()

difyModule = DifyModule()

@app.post("/bookmarks/categorize")
async def categorize_bookmarks(file: UploadFile = File(...)):
    # ファイルの内容を読み込む
    content = await file.read()
    # try:
    bookmarks_json_list = json.loads(content.decode("utf-8"))
    run_workflow_result_list = []
    for bookmark_json in bookmarks_json_list:
        # print(f"type(bookmark_json): \n{type(bookmark_json)}\nEnd")
        bookmark_json_str = json.dumps(bookmark_json, ensure_ascii=False)
        # print(f"len(bookmark_json_str): \n{len(bookmark_json_str)}\nEnd")
        run_workflow_result = difyModule.categorized_json(bookmark_json_str)
        run_workflow_result_list.append(run_workflow_result)

    #　分類結果をbookmark_jsonと統合
    categorized_bookmark_json_list = []
    for i in range(0, len(run_workflow_result_list)-1):
        # 理想の形 → {"分類項目1": {"LLM": {bookmarkの中身}}}
        categorized_bookmark_json_result = run_workflow_result_list[i]["data"]["outputs"]["categorized_bookmark_json"]
        categorized_bookmark_json = json.loads(categorized_bookmark_json_result)["分類項目"]
        categorized_bookmark_json_list.append(ast.literal_eval("{ " + f"\"分類項目{i}\": " + "{" + f"\"{categorized_bookmark_json}\": {bookmarks_json_list[i]}" + "} }"))

    return categorized_bookmark_json_list
    #     json_string = json.dumps(json_content, ensure_ascii=False, indent=2)
    #     return {"json_string": json_string}
    # except json.JSONDecodeError:
    #     return {"error": "Invalid JSON file"}
