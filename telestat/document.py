"""
Document processing.
"""

import asyncio
from datetime import datetime
from random import randint
from typing import List

from db import get_connection
from custom_types import Document


async def request_signing(name: str, recipients: List[str], url: str) -> Document:
    """
    Request document signing from specified recipients.

    :param name: Document name.
    :param recipients: Recipients to sign doc.
    :param url: Document url.
    :return: An updated document with url in our file storage and internal id.
    """
    new_url = download_doc(url)
    db_document = await create_doc_entry(name, recipients, new_url)
    await notify_recipients(db_document['id'], db_document['name'], db_document['recipients'])
    return db_document


async def sign_document(id_):
    conn = await get_connection()
    await conn.execute(
        """
        UPDATE documents
        SET is_signed = TRUE
        WHERE id = $1::INT
        """,
        id_
    )


def download_doc(url: str) -> str:
    """
    Download document from a source and upload it to our file storage.

    :param url: source file url.
    :return: url on our file storage.
    """
    return ''.join(reversed(url))


async def create_doc_entry(name: str, recipients: List[str], url: str) -> Document:
    conn = await get_connection()
    document = await conn.fetchrow(
        """
        INSERT
        INTO documents(name, recipients, url, is_signed)
        VALUES($1::TEXT, $2::TEXT[], $3::TEXT, FALSE)
        RETURNING id, name, recipients, url
        """,
        name, recipients, url
    )
    return {
        'id': document['id'],
        'name': document['name'],
        'recipients': document['recipients'],
        'url': document['url'],
    }


async def notify_recipients(doc_id: int, doc_name: str, recipients: List[str]):
    """
    Notify recipients about doc waiting to be signed.
    """
    for recipient in recipients:
        asyncio.create_task(send_to_chat(doc_id, doc_name, recipient))
        await send_to_email(doc_id, doc_name, recipient)


async def send_to_email(doc_id: int, doc_name: str, recipient: str):
    """
    Sends email to recipient and simulates that doc will be signed with 20% chance.
    """
    print(f"[{datetime.now()}] sending email to {recipient}: you have your document {doc_name}")

    # simulate document signage.
    will_sign_document = randint(0, 4) == 1
    if will_sign_document:
        print('Document signed!')
        await sign_document(doc_id)


async def send_to_chat(doc_id: int, doc_name: str, recipient: str):
    """
    Sends invitation to recipient to sign doc in chat after waiting 5 seconds.
    """
    await asyncio.sleep(5)
    conn = await get_connection()
    is_signed = await conn.fetchval(
        """
        SELECT is_signed
        FROM documents
        WHERE id=$1::INT
        """,
        doc_id
    )
    if not is_signed:
        print('Document not signed')
        print(f"[{datetime.now()}] sending message to {recipient}: you have your document {doc_name}")

