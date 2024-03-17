
# Scheme
## Table1 [user]
- user_id : 使用者帳號不重複流水號(不可為none)
- pwd: 使用者密碼
- name: 使用者自定義的名稱
- email: 使用者email
- domain: 使用者專業領域
- role: 使用者擔任角色
- goal: 使用者目標
- tag: 使用者標籤 (AI 標註)
- timestamp: 時間戳


## Table2 [question_cluster]
- qst_id: 問題集不重複流水號(不可為none)
- qst_text: 問題
- ask_user: 提問的使用者 id 
- state: 已解決、待解決、已關閉
- timestamp: 時間戳


## Table3 [expert_answer]
- ans_id: 專家回覆不重複流水號(不可為none)
- qst_id: 對應的問題編號
- expert_user: 回覆問題的使用者id
- expert_response: [str] 專家回覆
- timestamp: 時間戳


## Table4 [ai_answer]
- ans_id: AI回覆不重複流水號(不可為none)
- qst_id: 對應的問題編號
- user_id: 對應的使用者id
- ai_response: [str] AI回覆
- timestamp: 時間戳
