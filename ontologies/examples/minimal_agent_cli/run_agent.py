import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax

# --- Initialization ---
load_dotenv()
console = Console()

# --- LLM Studio Configuration ---
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1") # Read from .env, or use default value
client = OpenAI(base_url=LLM_BASE_URL, api_key=os.getenv("OPENAI_API_KEY", "sk-not-needed-for-local"))

# --- Load Agent's "Identity" and "Authorization" ---
try:
    with open("agent_profile.jsonld", "r") as f:
        AGENT_PROFILE = json.load(f)
    with open("delegation.jsonld", "r") as f:
        DELEGATION = json.load(f)
except FileNotFoundError as e:
    console.print(f"[bold red]Error: Configuration file {e.filename} not found. Please ensure all .jsonld files are present.[/bold red]")
    exit()

# --- Core Function for LLM Interaction ---
def ask_llm(system_prompt, user_prompt):
    """A general function for sending requests to the LLM and getting a structured JSON response."""
    try:
        model_name = "local-model" # Please adjust this according to your LLM Studio settings
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            # Remove response_format, as LLM Studio does not support it
            # response_format={"type": "json_object"},
            temperature=0.1
        )
        
        # Extract the string that may contain JSON from the response
        response_text = response.choices[0].message.content
        
        # Clean up the string, removing potential markdown tags
        if response_text.strip().startswith("```json"):
            response_text = response_text.strip()[7:-3].strip()
            
        return json.loads(response_text)
    except json.JSONDecodeError:
        console.print("[bold red]Error: LLM returned invalid JSON.[/bold red]")
        console.print(f"Raw response received:\n---\n{response_text}\n---")
        return None
    except Exception as e:
        console.print(f"[bold red]An error occurred while interacting with the LLM: {e}[/bold red]")
        console.print("[bold yellow]Please ensure LLM Studio is running, the model is loaded, and the API endpoint and model name are correct.[/bold yellow]")
        return None

# --- Main Loop ---
def main_loop():
    console.print("[bold green]Minimal Ontology Agent Started (Connected to LLM Studio). Please enter your command...[/bold green]")
    console.print("[cyan]Example: 'Please create a file named hello.txt with the content Hello Ontology!'[/cyan]")
    console.print("[cyan]Enter 'exit' to quit.[/cyan]")

    while True:
        user_input = console.input("[bold yellow]You > [/bold yellow]")
        if user_input.lower() == 'exit':
            break

        # --- Step 1: Intent Identification (Natural Language -> Intent JSON-LD) ---
        console.print("\n[bold magenta]1. Identifying your intent...[/bold magenta]")
        # Enhance Prompt, strictly requiring only JSON response
        intent_prompt_system = """
        You are an AI assistant. Your task is to convert the user's natural language request into a `core:Intent` JSON-LD object conforming to the Agent Ontology.
        You must return only a valid JSON object, without any explanations, comments, or markdown tags.
        The object should contain `label` and `details`. `details` should contain the parameters required to execute the task.
        """
        intent_json = ask_llm(intent_prompt_system, user_input)

        if not intent_json:
            continue
        
        console.print(Syntax(json.dumps(intent_json, indent=2), "json", theme="monokai", line_numbers=True))
        console.print("[green]Intent identification complete.[/green]")

        # --- Step 2: Decision and Planning (Intent -> Action JSON-LD) ---
        console.print("\n[bold magenta]2. Making decisions based on capabilities and authorization...[/bold magenta]")
        # Enhance Prompt to be more instructive, reducing the difficulty of inference for local LLMs
        planning_prompt_system = """
        You are a planner for an AI agent. Your task is to map the user's `Intent` to an available `Capability` of the agent.

        Your workflow is as follows:
        1.  **Analyze `Intent`**: Understand the goal the user wants to achieve.
        2.  **Review `AgentProfile`**: Check which capabilities are available in the `capabilities` list.
        3.  **Find the best match**: Select the **single** capability from the Profile that best matches the user's `Intent`.
        4.  **Check Authorization**: Confirm that the `Delegation` file permits the use of the selected capability.
        5.  **Construct `Action`**:
            - The `actionType` of the `Action` **must** be the `@id` of the selected capability.
            - The `parameters` of the `Action` **must** be extracted from the `details` of the `Intent`, and the parameter names must exactly match those defined in the selected capability.

        If a suitable and authorized capability is found, you **must** return a `core:Action` JSON-LD object.
        If not found, you **must** return a JSON object containing an `error` field, explaining the reason.
        You must return only a valid JSON object, without any explanations, comments, or markdown tags.
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
            console.print(f"[bold red]Decision failed: {action_json['error']}[/bold red]")
            continue
        console.print("[green]Decision complete, action planned.[/green]")

        # --- Step 3: Execution (Action -> Real World) ---
        console.print("\n[bold magenta]3. Preparing to execute action...[/bold magenta]")
        
        action_type = action_json.get("actionType")
        params = action_json.get("parameters", {})

        if action_type == "capability:WriteFile":
            file_path = params.get("filePath")
            content = params.get("content")
            
            if not file_path or content is None:
                console.print("[bold red]Execution failed: Incomplete action parameters.[/bold red]")
                continue

            console.print(f"Action: Writing file '{file_path}'")
            confirmation = console.input("[bold yellow]Continue? (y/n) > [/bold yellow]")

            if confirmation.lower() == 'y':
                try:
                    with open(file_path, "w") as f:
                        f.write(content)
                    console.print(f"[bold green]✅ Successfully wrote content to {file_path}[/bold green]\n")
                except Exception as e:
                    console.print(f"[bold red]❌ Error writing file: {e}[/bold red]\n")
            else:
                console.print("[cyan]Operation cancelled.[/cyan]\n")
        else:
            console.print(f"[bold red]Execution failed: Unknown action type '{action_type}'.[/bold red]\n")


if __name__ == "__main__":
    main_loop()