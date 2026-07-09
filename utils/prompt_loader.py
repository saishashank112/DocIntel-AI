import os

def load_prompt(filename: str) -> str:
    """Load a raw prompt string from the prompts folder."""
    # Find prompts directory relative to workspace root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()
