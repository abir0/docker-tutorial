import logging
import time
from datetime import datetime

import psycopg2
from config import settings
from models import PrescriptionData

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Handles all database operations."""

    def __init__(self):
        self.connection_params = {
            "dbname": settings.DB_NAME,
            "user": settings.DB_USER,
            "password": settings.DB_PASS,
            "host": settings.DB_HOST,
        }

    def get_connection(self, max_retries=5, retry_delay=2):
        """Create and return a database connection with retry mechanism."""
        retries = 0
        last_exception = None

        while retries < max_retries:
            try:
                logger.info(
                    f"Attempting to connect to database (attempt {retries + 1}/{max_retries})..."
                )
                return psycopg2.connect(**self.connection_params)
            except psycopg2.OperationalError as e:
                last_exception = e
                retries += 1
                if retries < max_retries:
                    wait_time = retry_delay * retries
                    logger.warning(
                        f"Database connection failed. Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)

        # If we get here, all retries failed
        logger.error(f"Failed to connect to database after {max_retries} attempts")
        raise last_exception

    def initialize_tables(self):
            """Create necessary tables if they don't exist."""
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                create_tables_query = """
                -- Create medication_details table
                CREATE TABLE IF NOT EXISTS medication_details (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    strength VARCHAR(100),
                    form VARCHAR(100),
                    quantity INTEGER
                );
                
                -- Create dosage_instructions table
                CREATE TABLE IF NOT EXISTS dosage_instructions (
                    id SERIAL PRIMARY KEY,
                    frequency VARCHAR(255),
                    duration VARCHAR(100),
                    special_instructions TEXT
                );
                
                -- Create prescriptions table with foreign keys
                CREATE TABLE IF NOT EXISTS prescriptions (
                    id SERIAL PRIMARY KEY,
                    rx_number VARCHAR(100),
                    date_written DATE,
                    patient_name VARCHAR(255),
                    patient_dob DATE,
                    patient_id VARCHAR(100),
                    medication_id INTEGER REFERENCES medication_details(id),
                    dosage_id INTEGER REFERENCES dosage_instructions(id),
                    prescriber_name VARCHAR(255),
                    prescriber_id VARCHAR(100),
                    pharmacy_name VARCHAR(255),
                    refills INTEGER,
                    is_controlled_substance BOOLEAN,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                
                cursor.execute(create_tables_query)
                conn.commit()
                cursor.close()
                conn.close()
                logger.info("Database tables initialized successfully")
                
            except Exception as e:
                logger.error(f"Error initializing database tables: {str(e)}")
                raise

    def store_prescription(self, data: PrescriptionData):
        """Store prescription data in the database."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Insert medication details
            medication_insert = """
            INSERT INTO medication_details (name, strength, form, quantity)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """
            cursor.execute(
                medication_insert,
                (
                    data.medication.name,
                    data.medication.strength,
                    data.medication.form,
                    data.medication.quantity,
                ),
            )
            medication_id = cursor.fetchone()[0]

            # Insert dosage instructions
            dosage_insert = """
            INSERT INTO dosage_instructions (frequency, duration, special_instructions)
            VALUES (%s, %s, %s)
            RETURNING id;
            """
            cursor.execute(
                dosage_insert,
                (
                    data.dosage.frequency,
                    data.dosage.duration,
                    data.dosage.special_instructions,
                ),
            )
            dosage_id = cursor.fetchone()[0]

            # Parse dates - handle potential date format variations
            date_written = self._parse_date(data.date_written)
            patient_dob = (
                self._parse_date(data.patient_dob) if data.patient_dob else None
            )

            # Insert prescription data
            prescription_insert = """
            INSERT INTO prescriptions (
                rx_number, date_written, patient_name, patient_dob, patient_id,
                medication_id, dosage_id, prescriber_name, prescriber_id,
                pharmacy_name, refills, is_controlled_substance, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            cursor.execute(
                prescription_insert,
                (
                    data.rx_number,
                    date_written,
                    data.patient_name,
                    patient_dob,
                    data.patient_id,
                    medication_id,
                    dosage_id,
                    data.prescriber_name,
                    data.prescriber_id,
                    data.pharmacy_name,
                    data.refills,
                    data.is_controlled_substance,
                    data.notes,
                ),
            )

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    def _parse_date(self, date_str):
        """Parse date string into date object, handling multiple formats."""
        if not date_str:
            return None

        date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%d/%m/%Y"]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue

        return None
