"""Agent builder."""

from llama_index.llms import ChatMessage
from llama_index.prompts import ChatPromptTemplate
from typing import List, cast, Optional
from core.builder_config import BUILDER_LLM
from typing import Dict, Any
import uuid
from core.constants import AGENT_CACHE_DIR
from abc import ABC, abstractmethod

from core.param_cache import ParamCache, RAGParams
from core.utils import (
    load_data,
    get_tool_objects,
    construct_agent,
)
from core.agent_builder.registry import AgentCacheRegistry


# System prompt tool
GEN_SYS_PROMPT_STR = """\
Task information is given below. 

Given the task, please generate a system prompt for an OpenAI-powered bot \
to solve this task: 
{task} \

Make sure the system prompt obeys the following requirements:
- Tells the bot to ALWAYS use tools given to solve the task. \
NEVER give an answer without using a tool.
- Does not reference a specific data source. \
The data source is implicit in any queries to the bot, \
and telling the bot to analyze a specific data source might confuse it given a \
user query.

"""

gen_sys_prompt_messages = [
    ChatMessage(
        role="system",
        content="You are helping to build a system prompt for another bot.",
    ),
    ChatMessage(role="user", content=GEN_SYS_PROMPT_STR),
]

GEN_SYS_PROMPT_TMPL = ChatPromptTemplate(gen_sys_prompt_messages)


class BaseRAGAgentBuilder(ABC):
    """Base RAG Agent builder class."""

    @property
    @abstractmethod
    def cache(self) -> ParamCache:
        """Cache."""

    @property
    @abstractmethod
    def agent_registry(self) -> AgentCacheRegistry:
        """Agent registry."""


class RAGAgentBuilder(BaseRAGAgentBuilder):
    """RAG代理構建器。

    包含一套函數來構建RAG代理，包括：
    - 設置系統提示
    - 加載數據
    - 添加網絡搜索
    - 設置參數（例如：top-k）

    必須傳入一個緩存。此緩存將在構建代理的過程中被修改。

    """

    def __init__(
        self,
        cache: Optional[ParamCache] = None,
        agent_registry: Optional[AgentCacheRegistry] = None,
    ) -> None:
        """初始化參數。"""
        self._cache = cache or ParamCache()
        self._agent_registry = agent_registry or AgentCacheRegistry(
            str(AGENT_CACHE_DIR)
        )

    @property
    def cache(self) -> ParamCache:
        """緩存。"""
        return self._cache

    @property
    def agent_registry(self) -> AgentCacheRegistry:
        """代理註冊處。"""
        return self._agent_registry

    def create_system_prompt(self, task: str) -> str:
        """為給定輸入任務的另一代理創建系統提示。"""
        llm = BUILDER_LLM
        fmt_messages = GEN_SYS_PROMPT_TMPL.format_messages(task=task)
        response = llm.chat(fmt_messages)
        self._cache.system_prompt = response.message.content

        return f"系統提示創建成功：{response.message.content}"

    def load_data(
        self,
        file_names: Optional[List[str]] = None,
        directory: Optional[str] = None,
        urls: Optional[List[str]] = None,
    ) -> str:
        """為給定任務加載數據。

        僅應指定file_names、directory或urls中的一項。

        參數：
            file_names (Optional[List[str]]): 要加載的文件名列表。
                默認為None。
            directory (Optional[str]): 從中加載文件的目錄。
            urls (Optional[List[str]]): 要加載的URL列表。
                默認為None。

        """
        file_names = file_names or []
        urls = urls or []
        directory = directory or ""
        docs = load_data(file_names=file_names, directory=directory, urls=urls)
        self._cache.docs = docs
        self._cache.file_names = file_names
        self._cache.urls = urls
        self._cache.directory = directory
        return "數據加載成功。"

    def add_web_tool(self) -> str:
        """添加網絡工具以使代理能夠解決任務。"""
        # TODO: 讓這不要硬編碼到一個網絡工具
        # 設置Metaphor工具
        if "web_search" in self._cache.tools:
            return "網絡工具已經添加。"
        else:
            self._cache.tools.append("web_search")
        return "網絡工具添加成功。"

    def get_rag_params(self) -> Dict:
        """獲取用於配置RAG管道的參數。

        應在`set_rag_params`之前調用，以便代理了解架構。

        """
        rag_params = self._cache.rag_params
        return rag_params.dict()

    def set_rag_params(self, **rag_params: Dict) -> str:
        """設置RAG參數。

        這些參數將用於實際初始化代理。
        應先調用`get_rag_params`以獲得輸入字典的架構。

        參數：
            **rag_params (Dict): RAG參數的字典

        new_dict = self._cache.rag_params.dict()
        new_dict.update(rag_params)
        rag_params_obj = RAGParams(**new_dict)
        self._cache.rag_params = rag_params_obj
        return "RAG parameters set successfully."
        """
    def create_agent(self, agent_id: Optional[str] = None) -> str:
        """Create an agent.

        There are no parameters for this function because all the
        functions should have already been called to set up the agent.

        """
        if self._cache.system_prompt is None:
            raise ValueError("Must set system prompt before creating agent.")

        # construct additional tools
        additional_tools = get_tool_objects(self.cache.tools)
        agent, extra_info = construct_agent(
            cast(str, self._cache.system_prompt),
            cast(RAGParams, self._cache.rag_params),
            self._cache.docs,
            additional_tools=additional_tools,
        )

        # if agent_id not specified, randomly generate one
        agent_id = agent_id or self._cache.agent_id or f"Agent_{str(uuid.uuid4())}"
        self._cache.vector_index = extra_info["vector_index"]
        self._cache.agent_id = agent_id
        self._cache.agent = agent

        # save the cache to disk
        self._agent_registry.add_new_agent_cache(agent_id, self._cache)
        return "Agent created successfully."

    def update_agent(
        self,
        agent_id: str,
        system_prompt: Optional[str] = None,
        include_summarization: Optional[bool] = None,
        top_k: Optional[int] = None,
        chunk_size: Optional[int] = None,
        embed_model: Optional[str] = None,
        llm: Optional[str] = None,
        additional_tools: Optional[List] = None,
    ) -> None:
        """更新代理。

        通過ID刪除舊代理並創建一個新的。
        可選地更新系統提示和RAG參數。

        注意：目前是手動調用的，不是供代理使用。


        """
        self._agent_registry.delete_agent_cache(self.cache.agent_id)

        # set agent id
        self.cache.agent_id = agent_id

        # set system prompt
        if system_prompt is not None:
            self.cache.system_prompt = system_prompt
        # get agent_builder
        # We call set_rag_params and create_agent, which will
        # update the cache
        # TODO: decouple functions from tool functions exposed to the agent
        rag_params_dict: Dict[str, Any] = {}
        if include_summarization is not None:
            rag_params_dict["include_summarization"] = include_summarization
        if top_k is not None:
            rag_params_dict["top_k"] = top_k
        if chunk_size is not None:
            rag_params_dict["chunk_size"] = chunk_size
        if embed_model is not None:
            rag_params_dict["embed_model"] = embed_model
        if llm is not None:
            rag_params_dict["llm"] = llm

        self.set_rag_params(**rag_params_dict)

        # update tools
        if additional_tools is not None:
            self.cache.tools = additional_tools

        # this will update the agent in the cache
        self.create_agent()
