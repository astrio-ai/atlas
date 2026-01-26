"""
Tool registry for LLM-controlled tool orchestration.

This module provides a registry of tools that can be called by the LLM,
mapping them to function definitions and execution handlers.
"""
import json
from typing import Any, Callable, Dict, List, Optional


class ToolRegistry:
    """Registry for LLM-callable tools."""

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Callable] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable,
    ):
        """
        Register a tool.

        Args:
            name: Function name for the tool
            description: Description of what the tool does
            parameters: JSON Schema parameters definition
            handler: Callable that executes the tool
        """
        self._tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
        }
        self._handlers[name] = handler

    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Get all registered tools as function definitions for the LLM."""
        return [
            {
                "type": "function",
                "function": tool_def,
            }
            for tool_def in self._tools.values()
        ]

    def execute(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool by name with given arguments.

        Args:
            name: Tool name
            arguments: Arguments for the tool

        Returns:
            Result of tool execution
        """
        if name not in self._handlers:
            raise ValueError(f"Unknown tool: {name}")

        handler = self._handlers[name]
        return handler(**arguments)

    def has_tool(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._tools


# Global registry instance
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """Get the global tool registry."""
    return _registry


def register_tool(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    handler: Callable,
):
    """Convenience function to register a tool in the global registry."""
    _registry.register(name, description, parameters, handler)
