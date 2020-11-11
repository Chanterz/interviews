"""
Complex type declarations.
"""

from typing import List, TypedDict


class Document(TypedDict):
    id: int
    name: str
    recipients: List[str]
    url: str
