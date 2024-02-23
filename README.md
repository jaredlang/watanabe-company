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
        - LLM_MODEL=mistral:latest,codellama:7b-code-q4_K_M
        - LLM_CONFIG_LIST=OLM_CONFIG_LIST

## Run Locally

    * My Windows laptop is too slow to run this program locally. It doesn't even have a GPU.
    * 1xA10 instance on [Lambda Labs](https://cloud.lambdalabs.com/instances) is a better option.
    * Steps to run it on an Lambda instance 
        1. Install [Ollama](https://ollama.com/download/linux) 
        2. Install [Docker](https://docs.docker.com/engine/install/ubuntu/) 
        3. Git clone this repo 
        4. Create the .env file
