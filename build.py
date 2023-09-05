import os
from typing import TypedDict

import shutil

from weasyprint import HTML
import yaml
import jinja2
import helpers


def read_yaml(filename: str) -> TypedDict:
    """
    Read Yaml file given by ``filename`` and return dictionary data.
    """
    with open(filename, "rt", encoding="utf-8") as file:
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_data


def render_template(template_file: str, yml_data: TypedDict) -> str:
    """
    Render template file with ``yml_data``.
    """
    with open(template_file, "rt", encoding="utf-8") as file:
        jinja2_template = jinja2.Template(file.read())

    return jinja2_template.render(**yml_data)


def copy_static_data(theme_dir, output_dir) -> None:
    """
    Copy contents of theme directory skipping all jinja template files.
    """
    shutil.copytree(
        theme_dir,
        output_dir,
        ignore=lambda src, names: [
            name for name in names if name.endswith(".jinja2")],
    )


def clean(output_dir: str = "build") -> None:
    """
    Remove the output directory.
    """
    shutil.rmtree(output_dir, ignore_errors=True)


# theme -> simple or compact
def make_html(yaml_data: TypedDict, theme: str, output_dir: str = "build"):
    """
    Build the final directory, rendering all templates and copying source files
    """
    yaml_data["h"] = helpers
    yaml_data["labels"] = None

    theme_location = os.path.join("themes", theme)
    jinja2_template = os.path.join(theme_location, "index.jinja2")
    html_template = os.path.join(output_dir, "index.html")

    clean(output_dir)
    copy_static_data(theme_location, output_dir)

    html = render_template(jinja2_template, yaml_data)
    with open(html_template, "wt", encoding="utf-8") as file:
        file.write(html)


def make_pdf(file_name: str, theme: str, pdf_dir: str = "pdf", output_dir: str = "build"):
    """
    Generate PDF file out of generated 'index.html' page.
    """
    output_file = os.path.join(pdf_dir, file_name)
    input_file = os.path.join(output_dir, "index.html")
    theme_location = os.path.join("themes", theme)
    html = HTML(input_file, base_url=theme_location)
    html.write_pdf(output_file)


def make_resume_from_yaml(file_name: str, theme: str, yaml_dir: str = "resumes",
                          pdf_dir: str = "pdf", output_dir: str = "build"):
    """
    Both HTML and PDF for a single file.
    """
    resume_data = read_yaml(os.path.join(yaml_dir, f"{file_name}.yaml"))
    make_html(resume_data, theme, output_dir)
    make_pdf(f"{file_name}.pdf", theme, pdf_dir, output_dir)


def main():
    """
    Entry function for the script to handle command arguments
    and run appropriate build like 'html' and 'pdf'.
    """
    # read resume data and config with some defaults
    yaml_dir = "resumes"
    pdf_dir = "pdf"
    output_dir = "build"
    theme = "compact"
    # file_name = "jmbeach"
    # file_name = "hanula"

    files = ["jmbeach", "hanula"]

    for file in files:
        make_resume_from_yaml(file, theme, yaml_dir, pdf_dir, output_dir)


if __name__ == "__main__":
    main()
