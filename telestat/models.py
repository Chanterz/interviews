"""
Request's body and response models.
"""

from typing import List

from pydantic import BaseModel


class DocumentIn(BaseModel):
    name: str
    """
    Document name.
    """

    recipients: List[str]
    """
    List of recipients to sign document.
    """

    url: str
    """
    Document location url.
    """


class DocumentOut(DocumentIn):
    id: int
    """
    Document ID in our DB.
    """
