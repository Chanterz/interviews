import uvicorn
from fastapi import FastAPI

import document
from models import DocumentIn, DocumentOut

app = FastAPI(debug=True)


@app.post('/request_doc_signing', response_model=DocumentOut)
async def request_document_signing(doc: DocumentIn):
    """
    Requests document signing from specified recipients.
    """
    return await document.request_signing(doc.name, doc.recipients, doc.url)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
