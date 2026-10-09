import os
from dotenv import load_dotenv
from crewai_tools import YoutubeChannelSearchTool

load_dotenv()

yt_tool = YoutubeChannelSearchTool(
    youtube_channel_handle="@krishnaik06",
    config=dict(
        embedding_model=dict(
            provider="onnx",
        )
    )
)