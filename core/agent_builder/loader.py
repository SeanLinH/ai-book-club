"""Loader agent."""

from typing import List, cast, Optional
from llama_index.tools import FunctionTool
from llama_index.agent.types import BaseAgent
from core.builder_config import BUILDER_LLM
from typing import Tuple, Callable
import streamlit as st

from core.param_cache import ParamCache
from core.utils import (
    load_meta_agent,
)
from core.agent_builder.registry import AgentCacheRegistry
from core.agent_builder.base import RAGAgentBuilder, BaseRAGAgentBuilder
from core.agent_builder.multimodal import MultimodalRAGAgentBuilder

####################
#### META Agent ####
####################

RAG_BUILDER_SYS_STR = """\
您正在協助根據用戶指定的任務構建一個代理。您應該大致按照以下順序使用工具來構建代理。

1) 創建系統提示工具：為代理創建系統提示。
2) 加載用戶指定的數據（基於他們指定的文件路徑）。
3) 決定是否添加額外的工具。
4) 為RAG管道設置參數。
5) 構建代理。

這將是一個與用戶進行來回對話的過程。
您應該繼續詢問用戶是否還有其他事情要做，直到他們說他們完成為止。
為了幫助指導他們了解過程，
您可以根據他們可用的工具給出參數設置的建議（例如，“您想設置要檢索的文檔數量嗎？”）。
"""


### DEFINE Agent ####
# NOTE: here we define a function that is dependent on the LLM,
# please make sure to update the LLM above if you change the function below


def _get_builder_agent_tools(agent_builder: RAGAgentBuilder) -> List[FunctionTool]:
    """Get list of builder agent tools to pass to the builder agent."""
    # see if metaphor api key is set, otherwise don't add web tool
    # TODO: refactor this later
    print("\n\n", st.secrets, "\n\n")

    if "metaphor_key" in st.secrets:
        fns: List[Callable] = [
            agent_builder.create_system_prompt,
            agent_builder.load_data,
            agent_builder.add_web_tool,
            agent_builder.get_rag_params,
            agent_builder.set_rag_params,
            agent_builder.create_agent,
        ]
    else:
        fns = [
            agent_builder.create_system_prompt,
            agent_builder.load_data,
            agent_builder.get_rag_params,
            agent_builder.set_rag_params,
            agent_builder.create_agent,
        ]

    fn_tools: List[FunctionTool] = [FunctionTool.from_defaults(fn=fn) for fn in fns]
    return fn_tools


def _get_mm_builder_agent_tools(
    agent_builder: MultimodalRAGAgentBuilder,
) -> List[FunctionTool]:
    """Get list of builder agent tools to pass to the builder agent."""
    fns: List[Callable] = [
        agent_builder.create_system_prompt,
        agent_builder.load_data,
        agent_builder.get_rag_params,
        agent_builder.set_rag_params,
        agent_builder.create_agent,
    ]

    fn_tools: List[FunctionTool] = [FunctionTool.from_defaults(fn=fn) for fn in fns]
    return fn_tools


# define agent
def load_meta_agent_and_tools(
    cache: Optional[ParamCache] = None,
    agent_registry: Optional[AgentCacheRegistry] = None,
    is_multimodal: bool = False,
) -> Tuple[BaseAgent, BaseRAGAgentBuilder]:
    """Load meta agent and tools."""

    if is_multimodal:
        agent_builder: BaseRAGAgentBuilder = MultimodalRAGAgentBuilder(
            cache, agent_registry=agent_registry
        )
        fn_tools = _get_mm_builder_agent_tools(
            cast(MultimodalRAGAgentBuilder, agent_builder)
        )
        builder_agent = load_meta_agent(
            fn_tools, llm=BUILDER_LLM, system_prompt=RAG_BUILDER_SYS_STR, verbose=True
        )
    else:
        # think of this as tools for the agent to use
        agent_builder = RAGAgentBuilder(cache, agent_registry=agent_registry)
        fn_tools = _get_builder_agent_tools(agent_builder)
        builder_agent = load_meta_agent(
            fn_tools, llm=BUILDER_LLM, system_prompt=RAG_BUILDER_SYS_STR, verbose=True
        )

    return builder_agent, agent_builder
