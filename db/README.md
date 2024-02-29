
# Scheme
## Table1 [user]
- user_id : 使用者不重複流水號(不可為none)
- name: 使用者姓名
- domain: 使用者專業領域
- role: 使用者擔任角色
- goal: 使用者目標
- tag: 使用者標籤 (AI 標註)
- timestamp: 時間戳


## Table2 [question_cluster]
- qst_id: 問題集不重複流水號(不可為none)
- qst_text: 問題
- ask_user: 提問的使用者 id  (可為空)
- expert_user: 回覆問題的使用者id (可為空)
- ai_response: [str]AI 回覆的建議
- expert_response: [str] 專家回覆
- state: 已解決、待解決、已關閉
- timestamp: 時間戳