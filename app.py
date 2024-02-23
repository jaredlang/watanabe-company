from dotenv import load_dotenv
import os
import json

import autogen
from autogen.agentchat.contrib.agent_builder import AgentBuilder

load_dotenv() 

# load the config file and model from .env
config_file_or_env = os.environ["LLM_CONFIG_LIST"]
model_list = [m.strip() for m in os.environ["LLM_MODEL"].split(",")]

llm_config = {"temperature": 0}

config_list = autogen.config_list_from_json(
    config_file_or_env, 
    filter_dict={"model": [m.strip() for m in model_list]}
)


def start_task(execution_task: str, agent_list: list):
    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config})
    agent_list[0].initiate_chat(manager, message=execution_task)


def create_positions(): 
    AGENT_SYS_MSG_PROMPT = """Considering the following position:

POSITION: {position}

What requirements should this position be satisfied?

Hint:
# Your answer should be in one sentence.
# Your answer should be natural, starting from "As a ...".
# People with the above position need to complete a task given by a leader or colleague.
# People will work in a group chat, solving tasks with other people with different jobs.
# The modified requirement should not contain the code interpreter skill.
# Coding skill is limited to Python.
"""

    position_list = [
        "Environmental_Scientist",
        "Astronomer",
        "Software_Developer",
        "Data_Analyst",
        "Journalist",
        "Teacher",
        "Lawyer",
        "Programmer",
        "Accountant",
        "Mathematician",
        "Physicist",
        "Biologist",
        "Chemist",
        "Statistician",
        "IT_Specialist",
        "Cybersecurity_Expert",
        "Artificial_Intelligence_Engineer",
        "Financial_Analyst",
    ]

    build_manager = autogen.OpenAIWrapper(config_list=config_list)
    sys_msg_list = []

    for pos in position_list:
        resp_agent_sys_msg = (
            build_manager.create(
                messages=[
                    {
                        "role": "user",
                        "content": AGENT_SYS_MSG_PROMPT.format(
                            position=pos,
                            default_sys_msg=autogen.AssistantAgent.DEFAULT_SYSTEM_MESSAGE,
                        ),
                    }
                ]
            )
            .choices[0]
            .message.content
        )
        sys_msg_list.append({"name": pos, "profile": resp_agent_sys_msg})
    
    return sys_msg_list


position_list = create_positions() 

library_path_or_json = json.dumps(position_list)

building_task = """Find a paper on arxiv by programming, and analyze its application in some domain. 
For example, find a recent paper about gpt-4 on arxiv and find its potential applications in software.
"""

agent_builder = AgentBuilder(
    config_file_or_env=config_file_or_env, builder_model=model_list[0], agent_model=model_list[0]
)

agent_list, _ = agent_builder.build_from_library(
    building_task, library_path_or_json, llm_config, 
    coding=True, code_execution_config = {"work_dir": "coding", "use_docker": True }
)

start_task(
    execution_task="Find a recent paper about explainable AI on arxiv and find its potential applications in medical.",
    agent_list=agent_list,
)

agent_builder.clear_all_agents()
