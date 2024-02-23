import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager
import chromadb
import os
from autogen import GroupChat
import json
from autogen.retrieve_utils import TEXT_FORMATS

######################################################################
config_list_mistral = [
    {
        "base_url": "http://localhost:11434/v1",
        "api_key": "sk-111111111111",        
        "model": "TheBloke/Llama-2-7B-32K-Instruct-GGUF"
    }
]

config_list_codellama = [
    {
        "base_url": "http://localhost:11434/v1",
        "api_key": "sk-111111111111",        
        "model": "TheBloke/Llama-2-7B-32K-Instruct-GGUF"
    }
]
######################################################################
llm_config_mistral={
    "config_list": config_list_mistral,
}

llm_config_codellama={
    "config_list": config_list_codellama,
}
######################################################################
llm_config_mistral = llm_config_mistral
llm_config_codellama = llm_config_codellama
######################################################################
assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config_mistral,
    # code_execution=False # Disable code execution entirely
    code_execution_config={"work_dir":"coding", "use_docker":False}
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama,
    # code_execution=False # Disable code execution entirely
    code_execution_config={"work_dir":"coding", "use_docker":False}
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    #human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "coding", "use_docker":False},
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task="""
Write a python script to output numbers 1 to 100 and then the user_proxy agent should run the script
"""

#task="""
#Write a script to output numbers 1 to X where X is a random number generated by the user_proxy agent
#"""

#user_proxy.initiate_chat(coder, message=task)  # Simple chat with coder

groupchat = autogen.GroupChat(agents=[user_proxy, coder, assistant], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config_mistral)
user_proxy.initiate_chat(manager, message=task)