import json
from .claude_client import messages

def background_step(project, literature_notes):
    system = open("prompts/01_background.txt", "r", encoding="utf-8").read()
    user = f"PROJECT:\n{json.dumps(project, indent=2)}\n\nLITERATURE:\n{literature_notes}"
    return messages(system, user, max_tokens=1000)

def challenge_step(background_text):
    system = open("prompts/02_challenges.txt", "r", encoding="utf-8").read()
    user = f"BACKGROUND:\n{background_text}"
    return messages(system, user, max_tokens=1200)

def methods_step(challenge_text, literature_notes):
    system = open("prompts/03_methods.txt", "r", encoding="utf-8").read()
    user = f"CHALLENGE:\n{challenge_text}\n\nLITERATURE:\n{literature_notes}"
    return messages(system, user, max_tokens=1200)

def solution_step(project, background_text, challenge_text, methods_text):
    system = open("prompts/04_solution.txt", "r", encoding="utf-8").read()
    user = f"""PROJECT:
{json.dumps(project, indent=2)}

BACKGROUND:
{background_text}

CHALLENGES:
{challenge_text}

METHODS:
{methods_text}
"""
    return messages(system, user, max_tokens=1800)

def evaluation_step(proposal_text):
    system = open("prompts/05_evaluation.txt", "r", encoding="utf-8").read()
    user = f"PROPOSAL:\n{proposal_text}"
    return messages(system, user, max_tokens=1000, temperature=0.0)
