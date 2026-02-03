from weasyprint import HTML
from django.template.loader import render_to_string
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

def generate_yearly_report_pdf(year, principal, teachers, classes):
    """
    Generates a PDF report for the given year.
    Returns the path to the generated PDF.
    """
    try:
        context = {
            'year': year,
            'principal': principal,
            'teachers': teachers,
            'classes': classes, # List of dicts with class info, students, marks, attendance
        }
        
        html_string = render_to_string('reports/yearly_report_pdf.html', context)
        
        filename = f'Yearly_Report_{year}.pdf'
        media_path = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(media_path, exist_ok=True)
        file_path = os.path.join(media_path, filename)
        
        # Base URL handling
        base_url = settings.MEDIA_ROOT
        
        html = HTML(string=html_string, base_url=base_url)
        html.write_pdf(target=file_path)
        
        logger.info(f"PDF generated successfully for year {year} at {file_path}")
        return os.path.join('reports', filename)
    except Exception as e:
        logger.error(f"Failed to generate PDF for year {year}: {str(e)}")
        raise Exception(f"PDF generation error: {str(e)}")
