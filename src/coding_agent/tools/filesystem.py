from pathlib import Path
from typing import Any

from coding_agent.config import get_settings
from coding_agent.tools.base import Tool


class ListDirectoryTool(Tool):
    """List files and directories inside the workspace."""

    name = "list_directory"
    description = "List files and directories inside the workspace."

    def execute(self, path: str = ".") -> dict[str, Any]:
        """List the contents of a directory."""

        settings = get_settings()

        workspace = Path(settings.workspace).resolve()
        target = (workspace / path).resolve()

        # Prevent access outside the workspace.
        try:
            target.relative_to(workspace)
        except ValueError:
            return {
                "success": False,
                "error": "Path is outside the workspace.",
            }

        if not target.exists():
            return {
                "success": False,
                "error": f"Path does not exist: {path}",
            }

        if not target.is_dir():
            return {
                "success": False,
                "error": f"Path is not a directory: {path}",
            }

        entries = []

        for entry in sorted(
            target.iterdir(),
            key=lambda item: item.name.lower(),
        ):
            entries.append(
                {
                    "name": entry.name,
                    "type": "directory" if entry.is_dir() else "file",
                }
            )

        return {
            "success": True,
            "path": path,
            "entries": entries,
        }

class ReadFileTool(Tool):
    """Read a text file inside the workspace."""

    name = "read_file"
    description = "Read the contents of a text file inside the workspace."

    def execute(self, path: str) -> dict[str, Any]:
        """Read a file and return its contents."""

        settings = get_settings()

        workspace = Path(settings.workspace).resolve()
        target = (workspace / path).resolve()

        # Prevent access outside the workspace.
        try:
            target.relative_to(workspace)
        except ValueError:
            return {
                "success": False,
                "error": "Path is outside the workspace.",
            }

        if not target.exists():
            return {
                "success": False,
                "error": f"File does not exist: {path}",
            }

        if not target.is_file():
            return {
                "success": False,
                "error": f"Path is not a file: {path}",
            }

        try:
            content = target.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return {
                "success": False,
                "error": f"File is not a UTF-8 text file: {path}",
            }
        except OSError as exc:
            return {
                "success": False,
                "error": f"Could not read file: {exc}",
            }

        return {
            "success": True,
            "path": path,
            "content": content,
        }