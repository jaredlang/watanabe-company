##########################################
# CREDIT TO leolivier for his brilliant post: 
# https://gist.github.com/mberman84/ea207e7d9e5f8c5f6a3252883ef16df3?permalink_comment_id=4888023#gistcomment-4888023
##########################################

import autogen

# direct access to Ollama since 0.1.24, compatible with OpenAI /chat/completions
BASE_URL="http://localhost:11434/v1"

config_list_mistral = [
    {
        'base_url': BASE_URL,
        'api_key': "fakekey",
        'model': "mistral:latest",
    }
]

config_list_codellama = [
    {
        'base_url': BASE_URL,
        'api_key': "fakekey",
        'model': "codellama:latest",
    }
]

llm_config_mistral={
    "config_list": config_list_mistral,
}

llm_config_codellama={
    "config_list": config_list_codellama,
}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web", "use_docker": False},
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
)

task="""
Write a python script that lists the number from 1 to 100
"""

user_proxy.initiate_chat(coder, message=task)
