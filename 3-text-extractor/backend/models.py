from typing import Optional

from pydantic import BaseModel, Field


class InputText(BaseModel):
    """Input data model for FastAPI endpoint."""

    text: str


class MedicationDetails(BaseModel):
    """Model for medication details."""

    name: Optional[str] = Field(None, description="Name of the medication")
    strength: Optional[str] = Field(
        None, description="Strength of the medication (e.g., 10mg, 500mg)"
    )
    form: Optional[str] = Field(
        None, description="Form of medication (e.g., tablet, capsule, liquid)"
    )
    quantity: Optional[str] = Field(
        None, description="Total quantity of medication prescribed"
    )


class DosageInstructions(BaseModel):
    """Model for dosage instructions."""

    frequency: Optional[str] = Field(
        None, description="How often to take (e.g., twice daily, every 8 hours)"
    )
    duration: Optional[str] = Field(
        None, description="Duration of treatment (e.g., 7 days, 2 weeks)"
    )
    special_instructions: Optional[str] = Field(
        None, description="Special instructions (e.g., take with food)"
    )


class PrescriptionData(BaseModel):
    """Comprehensive model for prescription data."""

    # Prescription identifiers
    rx_number: Optional[str] = Field(
        None, description="Prescription number if available"
    )
    date_written: Optional[str] = Field(
        None, description="Date the prescription was written"
    )

    # Patient information
    patient_name: Optional[str] = Field(None, description="Full name of the patient")
    patient_dob: Optional[str] = Field(None, description="Patient's date of birth")
    patient_id: Optional[str] = Field(
        None, description="Patient identifier if available"
    )

    # Medication and dosage details
    medication: MedicationDetails
    dosage: DosageInstructions

    # Prescriber information
    prescriber_name: Optional[str] = Field(
        None, description="Name of the prescribing doctor"
    )
    prescriber_id: Optional[str] = Field(
        None, description="Prescriber identifier (NPI, etc.)"
    )

    # Pharmacy information
    pharmacy_name: Optional[str] = Field(
        None, description="Name of the dispensing pharmacy"
    )

    # Refill information
    refills: Optional[int] = Field(None, description="Number of refills authorized")

    # Flags
    is_controlled_substance: Optional[bool] = Field(
        None, description="Whether the medication is a controlled substance"
    )

    # Additional information
    notes: Optional[str] = Field(
        None, description="Any additional notes or information"
    )
