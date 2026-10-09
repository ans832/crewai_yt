import os
from dotenv import load_dotenv
load_dotenv()

import litellm
litellm.drop_params = True

_orig_completion = litellm.completion

def _clean_completion(*args, **kwargs):
    if "messages" in kwargs:
        for m in kwargs["messages"]:
            if isinstance(m, dict):
                m.pop("cache_control", None)
                m.pop("cache_breakpoint", None)
    return _orig_completion(*args, **kwargs)

litellm.completion = _clean_completion

from crewai import Agent, LLM
from tools import yt_tool

groq_llm = LLM(
    model="groq/openai/gpt-oss-120b",  
    api_key = os.getenv("GROQ_API_KEY")
)

## Create a senior blog content researcher

blog_researcher=Agent(
    role='Blog Researcher from Youtube Videos',
    goal='get the relevant video transcription for the topic {topic} from the provided Yt channel',
    verbose=True,
    memory=False,
    backstory=(
       "Expert in understanding videos in AI Data Science , MAchine Learning And GEN AI and providing suggestion" 
    ),
    tools=[yt_tool],
    allow_delegation=True,
    llm=groq_llm
)

## creating a senior blog writer agent with YT tool

blog_writer=Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic} from YT video',
    verbose=True,
    memory=False,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    allow_delegation=False,
    llm=groq_llm


)