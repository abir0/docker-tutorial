import json
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(data, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    page_width, page_height = letter

    # Minimal color palette
    PRIMARY = colors.HexColor("#2d4059")
    SECONDARY = colors.HexColor("#f5f5f5")

    # Clean background
    c.setFillColor(colors.white)
    c.rect(0, 0, page_width, page_height, fill=1)

    # Header Section
    c.setFillColor(PRIMARY)
    c.rect(0, page_height - 60, page_width, 60, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        page_width / 2, page_height - 45, f"{data['name']} - Professional Report"
    )

    # Section parameters
    section_x = 40
    section_width = page_width - 80
    current_y = page_height - 100

    def draw_section(title, content_lines, section_height):
        nonlocal current_y
        # Section container
        c.setStrokeColor(colors.lightgrey)
        c.setFillColor(SECONDARY)
        c.rect(
            section_x, current_y - section_height, section_width, section_height, fill=1
        )

        # Section title
        c.setFillColor(PRIMARY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(section_x + 10, current_y - 25, title)

        # Content
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        text = c.beginText(section_x + 20, current_y - 50)
        for line in content_lines:
            text.textLine(line)
        c.drawText(text)

        current_y -= section_height + 30

    # Personal Information
    personal_info = [
        f"Age: {data['age']}",
        f"Location: {data['location']}",
        f"Position: {data['job']}",
        f"Salary: {data['salary']}",
    ]
    draw_section("Personal Information", personal_info, 100)

    # Contact Information
    contact_info = [data["contact"]["email"], data["contact"]["phone"]]
    draw_section("Contact Information", contact_info, 80)

    # Education
    education = [
        f"{edu['degree']} in {edu['field']} - {edu['university']} ({edu['year']})"
        for edu in data["education"]
    ]
    draw_section("Education", education, (40 + 20 * len(data["education"])))

    # Work Experience
    work_experience = []
    for job in data["work_experience"]:
        work_experience.extend(
            [
                f"Role: {job['position']}",
                f"Company: {job['company']} ({job['start_year']}-{job['end_year']})",
                f"Responsibilities: {job['responsibilities']}",
                "",  # Add spacing between entries
            ]
        )
    draw_section("Work Experience", work_experience, (40 + 20 * len(work_experience)))

    c.showPage()
    c.save()


def load_data(filename):
    with open(filename, "r") as file:
        return json.load(file)


def main():
    # Load demo data
    data = load_data("data/report_data.json")

    # Generate PDF for each person in the data
    os.makedirs("generated_pdfs", exist_ok=True)
    for i, person in enumerate(data):
        output_file = f"generated_pdfs/report_{i + 1}.pdf"
        generate_pdf(person, output_file)
        print(f"Generated PDF for {person['name']} saved as {output_file}")


if __name__ == "__main__":
    main()
