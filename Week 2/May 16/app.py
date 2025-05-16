import autogen

config_list = [
    {
        "model": "mistralai/mixtral-8x7b-instruct",  # or "openai/gpt-3.5-turbo"
        "api_key": "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",
        "base_url": "https://openrouter.ai/api/v1"  # Important!
    }
]


llm_config={
    #"request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=4,
    is_termination_msg=lambda x: x.get("content","").rstrip().endswith("Terminate"),
    code_execution_config={"work_dir": "web","use_docker":False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction 
    Otherwise, reply CONTINUE , or the reason why the task is not solved yet."""
)

task = """
write python code to print multiplication table of 7 and store the output in another file"
"""

user_proxy.initiate_chat(
    assistant,
    message=task

)