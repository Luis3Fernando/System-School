import jinja2
import pdfkit
import os
from django.conf import settings

def create_pdf(ruta_template, info, rutacss=''):
    nombre_template = os.path.basename(ruta_template)
    ruta_template_dir = os.path.dirname(ruta_template)
    
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template_dir))
    template = env.get_template(nombre_template)
    html = template.render(info)    
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': 'UTF-8',
    }
    
    config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    
    ruta_salida = os.path.join(settings.STATICFILES_DIRS[0], 'pdf', 'resultado.pdf')
    pdfkit.from_string(html, ruta_salida, css=rutacss if rutacss else None, options=options, configuration=config)
    return ruta_salida

#if __name__ == "__main__":
#    ruta_template = 'C:/Users/Luis Fernando/3D Objects/Praxis/Python/Pdf/template.html'
#    info = {
#        "nombre": "Moonknight"
#    }
#    create_pdf(ruta_template, info)
