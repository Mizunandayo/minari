"""Shared language/framework/grammardetection. Single source of truth"""







from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageInfo:
    language: str
    framework: str
    grammar: str









_TABLE: dict[str, LanguageInfo] = {
    "py":  LanguageInfo("python", "pytest", "python"),
    "js":  LanguageInfo("javascript", "jest", "javascript"),
    "jsx": LanguageInfo("javascript", "jest", "javascript"),
    "ts":  LanguageInfo("typescript", "jest", "typescript"),
    "tsx": LanguageInfo("typescript", "jest", "tsx"),
    "go":  LanguageInfo("go", "testify", "go"),
    "java": LanguageInfo("java", "junit", "java"),
}






def detect_language(file_path: str) -> LanguageInfo | None:
    ext = file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
    return _TABLE.get(ext)



