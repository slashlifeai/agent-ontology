import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax

# --- 初始化 ---
load_dotenv()
console = Console()

# --- LLM Studio 設定 ---
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1") # 從 .env 讀取，或使用預設值
client = OpenAI(base_url=LLM_BASE_URL, api_key=os.getenv("OPENAI_API_KEY", "sk-not-needed-for-local"))

# --- 載入 Agent 的「身份」和「授權」 ---
try:
    with open("agent_profile.jsonld", "r") as f:
        AGENT_PROFILE = json.load(f)
    with open("delegation.jsonld", "r") as f:
        DELEGATION = json.load(f)
except FileNotFoundError as e:
    console.print(f"[bold red]錯誤：找不到設定檔 {e.filename}。請確認所有 .jsonld 檔案都在。[/bold red]")
    exit()

# --- LLM 互動的核心函數 ---
def ask_llm(system_prompt, user_prompt):
    """一個通用的函數，用於向 LLM 發送請求並獲取結構化的 JSON 回應。"""
    try:
        model_name = "local-model" # 請根據你的 LLM Studio 設定調整此處
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            # 移除 response_format，因為 LLM Studio 不支援
            # response_format={"type": "json_object"},
            temperature=0.1
        )
        
        # 從回應中提取可能包含 JSON 的字串
        response_text = response.choices[0].message.content
        
        # 清理字串，移除可能存在的 markdown 標記
        if response_text.strip().startswith("```json"):
            response_text = response_text.strip()[7:-3].strip()
            
        return json.loads(response_text)
    except json.JSONDecodeError:
        console.print("[bold red]錯誤：LLM 回傳的不是有效的 JSON。[/bold red]")
        console.print(f"收到的原始回應：\n---\n{response_text}\n---")
        return None
    except Exception as e:
        console.print(f"[bold red]與 LLM 互動時發生錯誤：{e}[/bold red]")
        console.print("[bold yellow]請確認 LLM Studio 已啟動，模型已載入，且 API 端點和模型名稱正確。[/bold yellow]")
        return None

# --- 主循環 ---
def main_loop():
    console.print("[bold green]最小本體論代理人已啟動 (連接至 LLM Studio)。請輸入您的指令...[/bold green]")
    console.print("[cyan]範例：'請幫我建立一個叫 hello.txt 的檔案，內容是 Hello Ontology!'[/cyan]")
    console.print("[cyan]輸入 'exit' 來離開。[/cyan]")

    while True:
        user_input = console.input("[bold yellow]您 > [/bold yellow]")
        if user_input.lower() == 'exit':
            break

        # --- 步驟 1: 意圖識別 (自然語言 -> Intent JSON-LD) ---
        console.print("\n[bold magenta]1. 正在識別您的意圖...[/bold magenta]")
        # 強化 Prompt，強制要求只回傳 JSON
        intent_prompt_system = """
        你是一個 AI 助理。你的任務是將使用者的自然語言請求，轉換成一個符合 Agent Ontology 的 `core:Intent` JSON-LD 物件。
        你必須只回傳一個有效的 JSON 物件，不包含任何解釋、註解或 markdown 標記。
        物件應包含 `label` 和 `details`。`details` 應包含執行任務所需的參數。
        """
        intent_json = ask_llm(intent_prompt_system, user_input)

        if not intent_json:
            continue
        
        console.print(Syntax(json.dumps(intent_json, indent=2), "json", theme="monokai", line_numbers=True))
        console.print("[green]意圖識別完成。[/green]")

        # --- 步驟 2: 決策與規劃 (Intent -> Action JSON-LD) ---
        console.print("\n[bold magenta]2. 正在根據能力與授權進行決策...[/bold magenta]")
        # 強化 Prompt，使其更具指導性，降低本地 LLM 的推理難度
        planning_prompt_system = """
        你是一個為 AI 代理人制定計劃的規劃師。你的任務是將使用者的 `Intent` 映射到代理人的一個可用 `Capability`。

        你的工作流程如下：
        1.  **分析 `Intent`**：理解使用者想要達成的目標。
        2.  **審查 `AgentProfile`**：查看 `capabilities` 清單中有哪些可用的能力。
        3.  **尋找最佳匹配**：從 Profile 中選擇最符合使用者 `Intent` 的**單一**能力。
        4.  **檢查授權**：確認 `Delegation` 檔案允許使用這個被選中的能力。
        5.  **建構 `Action`**：
            - `Action` 的 `actionType` **必須**是被選中能力的 `@id`。
            - `Action` 的 `parameters` **必須**從 `Intent` 的 `details` 中提取，且參數名稱必須與被選中能力中定義的名稱完全一致。

        如果找到了合適且被授權的能力，你**必須**回傳一個 `core:Action` JSON-LD 物件。
        如果找不到，你**必須**回傳一個包含 `error` 欄位的 JSON 物件，並在其中解釋原因。
        你必須只回傳一個有效的 JSON 物件，不包含任何解釋、註解或 markdown 標記。
        """
        planning_prompt_user = f"""
        - Received Intent: {json.dumps(intent_json)}
        - My Profile: {json.dumps(AGENT_PROFILE)}
        - My Authorization: {json.dumps(DELEGATION)}
        """
        action_json = ask_llm(planning_prompt_system, planning_prompt_user)

        if not action_json:
            continue

        console.print(Syntax(json.dumps(action_json, indent=2), "json", theme="monokai", line_numbers=True))
        
        if "error" in action_json:
            console.print(f"[bold red]決策失敗：{action_json['error']}[/bold red]")
            continue
        console.print("[green]決策完成，已規劃行動。[/green]")

        # --- 步驟 3: 執行 (Action -> 現實世界) ---
        console.print("\n[bold magenta]3. 準備執行行動...[/bold magenta]")
        
        action_type = action_json.get("actionType")
        params = action_json.get("parameters", {})

        if action_type == "capability:WriteFile":
            file_path = params.get("filePath")
            content = params.get("content")
            
            if not file_path or content is None:
                console.print("[bold red]執行失敗：行動參數不完整。[/bold red]")
                continue

            console.print(f"行動：寫入檔案 '{file_path}'")
            confirmation = console.input("[bold yellow]是否繼續？(y/n) > [/bold yellow]")

            if confirmation.lower() == 'y':
                try:
                    with open(file_path, "w") as f:
                        f.write(content)
                    console.print(f"[bold green]✅ 成功將內容寫入 {file_path}[/bold green]\n")
                except Exception as e:
                    console.print(f"[bold red]❌ 寫入檔案時發生錯誤：{e}[/bold red]\n")
            else:
                console.print("[cyan]操作已取消。[/cyan]\n")
        else:
            console.print(f"[bold red]執行失敗：未知的行動類型 '{action_type}'。[/bold red]\n")


if __name__ == "__main__":
    main_loop()
