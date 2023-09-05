"""
Simple HTML and PDF resume generator from structurized YAML files.

Usage:
    build.py [-o=<DIR>] [-f=<FORMAT>] [-t=<THEME>] <resume_file>

Options:
    -o=<DIR>, --output_dir=<DIR>     Output directory for the build files. [default: build].
    -f=<FORMAT>, --format=<FORMAT>   Format of the build [default: html].
    -t=<NAME>, --theme=<NAME>        Name of the theme to use.
"""

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
        ignore=lambda src, names: [name for name in names if name.endswith(".jinja2")],
    )


def clean(output_dir: str) -> None:
    """
    Remove the output directory.
    """
    shutil.rmtree(output_dir, ignore_errors=True)


# theme -> simple or compact
def make_html(yaml_data: TypedDict, theme: str, output_dir: str):
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


def make_pdf(file_name: str, theme: str, output_dir: str, pdf_dir: str = "./pdf"):
    """
    Generate PDF file out of generated 'index.html' page.
    """
    output_file = os.path.join(pdf_dir, file_name.replace(".yaml", ".pdf"))
    input_file = os.path.join(output_dir, "index.html")
    theme_location = os.path.join("themes", theme)
    html = HTML(input_file, base_url=theme_location)
    html.write_pdf(output_file)


def make_resume_from_yaml(file_name: str, theme: str, output_dir: str):
    """
    Both HTML and PDF for a single file.
    """
    resume_data = read_yaml(file_name)
    make_html(resume_data, theme, output_dir)
    # make_pdf(
    #     file_name,
    #     theme,
    # )


def main():
    """
    Entry function for the script to handle command arguments
    and run appropriate build like 'html' and 'pdf'.
    """
    # read resume data and config with some defaults
    output_dir = "./build"
    theme = "simple"
    yaml_file_name = "./resumes/hanula.yaml"

    # build based on the given format
    # cmds = {'html': make_html, 'pdf': make_pdf}
    # return cmds[output_format](config, resume_data)

    make_resume_from_yaml(yaml_file_name, theme, output_dir)


if __name__ == "__main__":
    main()
