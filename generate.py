import json
import qrcode
import base64
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def generate_qr_code(data, size=2, border=1):
    """
    Generate a QR code with the given data, and return it as a base64-encoded PNG image.
    
    Parameters:
    - data: The data to encode in the QR code.
    - size: The size of each box in the QR code (default: 10).
    - border: The thickness of the border around the QR code (default: 4).
    
    Returns:
    - A base64-encoded PNG image of the QR code.
    """
    qr = qrcode.QRCode(
        version=1,   # version controls the size of the QR code grid
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # error correction level
        box_size=size,  # Size of each box
        border=border  # Thickness of the border
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image to a BytesIO object
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    
    # Return the base64-encoded image
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to load JSON data
def load_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to render HTML from template with Jinja2
# Data to inject into the template


def render_html_from_template(template_file, data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    data['qr_code_base64'] = generate_qr_code(data['url'])
    return template.render(data)

# Function to save HTML content to a file
def save_html_to_file(html_content, output_html_file):
    with open(output_html_file, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

# Function to convert HTML to PDF
def html_to_pdf(output_html_file, output_pdf_file):
    with open(output_html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    html = HTML(string=html_content)
    html.write_pdf(output_pdf_file)
    

# Main function to generate the HTML and PDF
def generate_html_and_pdf(template_file, json_file, output_html_file, output_pdf_file):
    # Load data from JSON file
    data = load_json_data(json_file)

    # Render HTML from the template and data
    html_content = render_html_from_template(template_file, data)

    # Save HTML content to a file
    save_html_to_file(html_content, output_html_file)

    # Convert HTML content to PDF
    error = html_to_pdf(output_html_file, output_pdf_file)

    print(f"HTML and PDF successfully created: {output_html_file}, {output_pdf_file}")

# Example usage
template_file = 'template.html'  # Path to your Jinja2 HTML template
json_file = 'input.json'         # Path to your JSON data
output_html_file = 'output.html'  # Path to the output HTML file
output_pdf_file = 'output.pdf'    # Path to the output PDF file

generate_html_and_pdf(template_file, json_file, output_html_file, output_pdf_file)