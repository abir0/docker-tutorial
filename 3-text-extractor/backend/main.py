import logging

from fastapi import FastAPI, HTTPException

from database import DatabaseManager
from extraction import TextExtractor
from models import InputText, PrescriptionData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Prescription Text Extractor")

# Initialize services
db_manager = DatabaseManager()
text_extractor = TextExtractor()


# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    try:
        db_manager.initialize_tables()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")


@app.post("/process_text/", response_model=PrescriptionData)
async def process_text(input_text: InputText):
    """Process prescription text and extract structured data."""
    try:
        # Extract structured data from text
        prescription_data = text_extractor.extract_prescription_data(input_text.text)

        # Store the extracted data in PostgreSQL
        db_manager.store_prescription(prescription_data)

        return prescription_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing prescription: {str(e)}"
        )


# Add a health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
