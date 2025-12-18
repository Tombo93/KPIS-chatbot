import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from db import insert_entries, print_entries, read_db_to_df


def get_prompt_template(prompt_type):
    match prompt_type:
        case "zero_shot":
            return PromptTemplate.from_template(
                "{sys_prompt} Answer the question directly. Do not return any preamble, explanation, or reasoning. Question: {query}"
            )
        case "few_shot":
            return PromptTemplate.from_template(
                "{sys_prompt} Answer the question directly. Do not return any preamble, explanation, or reasoning. Question: {query}"
            )
        case "chain_of_thought":
            return PromptTemplate.from_template(
                "{sys_prompt} Think step by step to answer the following question. Return the answer at the end of the response after a separator ####. Question: {query}"
            )
        case "chain_of_draft":
            return  PromptTemplate.from_template(
                "{sys_prompt} Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. Return the answer at the end of the response after a separator ####. Question: {query}"
            )


def format_prompts_with_template(prompts, template):
    return [template.format(query=prompt, sys_prompt="You are generating an API URL for the Presseportal API.") for prompt in prompts]


if __name__ == "__main__":
    ########## Secrets ##########
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")
    
    ########## Experiment ##########
    model = ChatOpenAI(model="gpt-5-nano")
    prompt_types = [
        # "zero_shot",
        # "few_shot",
        # "chain_of_thought",
        "chain_of_draft"
        ]    
    df = read_db_to_df()
    api_requests = df['API_request'].tolist()

    for prompt_type in prompt_types:
        ########## Format prompts ##########
        prompts = df[prompt_type].tolist()
        template = get_prompt_template(prompt_type)
        formatted_prompts = format_prompts_with_template(prompts, template)
        ########## Run Test ##########
        responses = model.batch(formatted_prompts)
        ########## Store responses ##########
        for idx, (q, a) in enumerate(zip(formatted_prompts, responses)):
            insert_entries(q, a.content, a.response_metadata['token_usage']['total_tokens'], api_requests[idx], p_type=prompt_type)

    print_entries()
