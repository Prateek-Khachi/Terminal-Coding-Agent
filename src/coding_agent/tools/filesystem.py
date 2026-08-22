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

class WriteFileTool(Tool):
    """Write text content to a file inside the workspace."""

    name = "write_file"
    description = "Write text content to a file inside the workspace."

    def execute(self, path: str, content: str) -> dict[str, Any]:
        """Write content to a file."""

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

        # Refuse to write to an existing directory.
        if target.exists() and target.is_dir():
            return {
                "success": False,
                "error": f"Path is a directory: {path}",
            }

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        except OSError as exc:
            return {
                "success": False,
                "error": f"Could not write file: {exc}",
            }

        return {
            "success": True,
            "path": path,
            "message": f"File written successfully: {path}",
        }

class EditFileTool(Tool):
    """Replace text in an existing file inside the workspace."""

    name = "edit_file"
    description = "Replace specific text in an existing file inside the workspace."

    def execute(
        self,
        path: str,
        old_text: str,
        new_text: str,
    ) -> dict[str, Any]:
        """Replace exactly one occurrence of old_text with new_text."""

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

        occurrences = content.count(old_text)

        if occurrences == 0:
            return {
                "success": False,
                "error": "The specified old_text was not found in the file.",
            }

        if occurrences > 1:
            return {
                "success": False,
                "error": (
                    f"old_text appears {occurrences} times. "
                    "The text must appear exactly once."
                ),
            }

        updated_content = content.replace(old_text, new_text, 1)

        try:
            target.write_text(updated_content, encoding="utf-8")
        except OSError as exc:
            return {
                "success": False,
                "error": f"Could not write file: {exc}",
            }

        return {
            "success": True,
            "path": path,
            "message": "File edited successfully.",
        }