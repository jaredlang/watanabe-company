# Create my bot company with AutoGen to complete a task

As I explore more multi-agent with AutoGen, OpenAI bill amounts up quickly. For a persona project, I want to research on how to utilize local LLM with AutoGen.

* with OpenAI
    - Without a doubt, OpenAI leads the chart of easy-to-use and quality chat.
    - OpenAI gets expensive when multiple agents chat with each other.

* with FastChat
    - Found this blog: [Use AutoGen with FastChat](https://microsoft.github.io/autogen/blog/2023/07/14/Local-LLMs/)
    - Didn't try it because FastChat is less known and it requires changing the FastChat code. 

* with Ollama
    - Then found this 2-week-old chat on [AutoGen with well-known local LLMs](https://gist.github.com/mberman84/ea207e7d9e5f8c5f6a3252883ef16df3)
    - Key Takeways
        1. Since version 0.1.24, Ollama is compatible with OpenAI API.
        2. Need to specify the model and base URL in the config list.

## Environment Variables

* with OpenAI
    - LLM_MODEL=gpt-4-1106-preview,gpt-4
    - LLM_CONFIG_LIST=OAI_CONFIG_LIST

* with Ollama
    - LLM_MODEL=mistral:latest,codellama:latest
    - LLM_CONFIG_LIST=OLM_CONFIG_LIST

## Run Locally

* My Windows laptop is too slow to run this program locally. It doesn't even have a GPU.
* 1xA10 instance on [Lambda Labs](https://cloud.lambdalabs.com/instances) is a better option.
* Steps to run it on an Lambda instance
    1. Install [Ollama](https://ollama.com/download/linux)
    2. Install [Docker](https://docs.docker.com/engine/install/ubuntu/)
    3. Start docker as a damon: sudo systemctl start docker
    3. Git clone this repo
    4. Create the .env file
* Run into this error and don't know what's wrong. The same script runs fine with OpenAI. The sample py file runs OK locally.
    - This issue was caused by the output of the previous step. Codellama doesn't return the selected agents as an array of names, which messes up the next steps.

    ```
    ==> Looking for suitable agents in library...
    ['Programmer', 'Data_Analyst', 'Software_Developer', 'Researcher_Scientist_#_(Researcher_Scientist_can_be_a_combination_of_Environmental_Scientist', 'Astronomer', 'Physicist', 'Biologist', 'Chemist_or_Statistician)'] are selected.
    ==> Generating system message...
    Preparing system message for Programmer...
    Preparing system message for Data_Analyst...
    Preparing system message for Software_Developer...
    Preparing system message for Researcher_Scientist_#_(Researcher_Scientist_can_be_a_combination_of_Environmental_Scientist...
    Preparing system message for Astronomer...
    Preparing system message for Physicist...
    ==> Creating agents...
    Creating agent Programmer with backbone codellama:7b-code-q4_K_M...
    Traceback (most recent call last):
    File "/home/ubuntu/watanabe-company/app.py", line 101, in <module>
        agent_list, _ = agent_builder.build_from_library(
    File "/home/ubuntu/watanabe-company/.venv/lib/python3.10/site-packages/autogen/agentchat/contrib/agent_builder.py", line 631, in build_from_library
        return self._build_agents(use_oai_assistant, **kwargs)
    File "/home/ubuntu/watanabe-company/.venv/lib/python3.10/site-packages/autogen/agentchat/contrib/agent_builder.py", line 654, in _build_agents
        self._create_agent(
    File "/home/ubuntu/watanabe-company/.venv/lib/python3.10/site-packages/autogen/agentchat/contrib/agent_builder.py", line 221, in _create_agent
        hf_api.model_info(model_name_or_hf_repo)
    File "/home/ubuntu/watanabe-company/.venv/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py", line 110, in _inner_fn
        validate_repo_id(arg_value)
    File "/home/ubuntu/watanabe-company/.venv/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py", line 164, in validate_repo_id
        raise HFValidationError(
    huggingface_hub.utils._validators.HFValidationError: Repo id must use alphanumeric chars or '-', '_', '.', '--' and '..' are forbidden, '-' and '.' cannot start or end the name, max length is 96: 'codellama:7b-code-q4_K_M'.
    ```