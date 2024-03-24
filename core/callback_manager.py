"""Streaming callback manager."""
from llama_index.callbacks.base_handler import BaseCallbackHandler
from llama_index.callbacks.schema import CBEventType

from typing import Optional, Dict, Any, List, Callable

STORAGE_DIR = "./storage"  # 緩存 the generated index
DATA_DIR = "./data"  # directory 保留檔案去檢索


class StreamlitFunctionsCallbackHandler(BaseCallbackHandler):
    """Callback handler that outputs streamlit components given events."""

    def __init__(self, msg_handler: Callable[[str], Any]) -> None:
        """Initialize the base callback handler."""
        self.msg_handler = msg_handler
        super().__init__([], [])

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        """一旦事件開始就跑此方法, 並且記下事件id."""
        if event_type == CBEventType.FUNCTION_CALL:
            if payload is None:
                raise ValueError("Payload 不能是 None")
            arguments_str = payload["function_call"]
            tool_str = payload["tool"].name
            print_str = f"Calling function: {tool_str} with args: {arguments_str}\n\n"
            self.msg_handler(print_str)
        else:
            pass
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """一旦事件結束就運行此方法."""
        pass
   

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """啟動overall trace."""
        pass

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """結束overall teace."""
        pass
