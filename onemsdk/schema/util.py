import os

import jinja2


def load_template(template_file: str, **data):
    dir = os.path.dirname(os.path.abspath(template_file))
    renv = jinja2.Environment(loader=jinja2.FileSystemLoader(dir))
    return renv.get_template(template_file).render(data)
