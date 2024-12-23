import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
# Function to load JSON data
def load_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to render HTML from template with Jinja2
def render_html_from_template(template_file, data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
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