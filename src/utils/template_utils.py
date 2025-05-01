from jinja2 import Environment, FileSystemLoader
import os

def load_prompt_template(template_path: str):
    """
    Loads and returns a Jinja2 template from a given file path.

    Args:
        template_path (str): Relative or absolute path to the template file.

    Returns:
        Template: A Jinja2 Template object ready to render.
    """
    directory, filename = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(directory))
    return env.get_template(filename)

