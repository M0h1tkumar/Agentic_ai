from fastapi import FastAPI, File, UploadFile, HTTPException
from docling.document_converter import DocumentConverter
from pathlib import Path
import tempfile
import shutil
import logging
import time

app = FastAPI(
    title="Docling PDF Parser API",
    version="1.0.0"
)

converter = DocumentConverter()

logging.basicConfig(level=logging.INFO)


@app.get("/")
def root():
    return {
        "message": "Docling PDF Parser API is running"
    }


@app.post("/parse-pdf")
async def parse_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    start = time.time()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = Path(temp_file.name)
            shutil.copyfileobj(file.file, temp_file)

        if temp_path.stat().st_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        result = converter.convert(str(temp_path))
        markdown = result.document.export_to_markdown()

        processing_time = round(time.time() - start, 2)

        return {
            "filename": file.filename,
            "processing_time_seconds": processing_time,
            "markdown_length": len(markdown),
            "markdown": markdown
        }

    except Exception as e:
        logging.exception("PDF Conversion Failed")

        raise HTTPException(
            status_code=500,
            detail=f"Conversion failed: {str(e)}"
        )

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
