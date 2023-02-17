import jinja2, markdown, toml, re
import os, glob, pathlib, shutil, distutils.dir_util




def load_config(config_filename):
    """
    This function takes in a filename with the sites configurations.
    It reads the configuration file then formats it using toml and returns a dictionary of configurations.
    """
    with open(config_filename, 'r') as config_file:
        return toml.loads(config_file.read())


def load_content_items(content_directory):
    """
    THis function takes in a directory name containing our content files with our posts.
    Using glob.glob, we loop through an array of files with the .md extension,
    then we use a regular exression to split the post and the title and date.
    We then use toml to create a dictionary of the post data, then we append the post content into the dictionary
    we then append the post dictionary into an array of posts called items then we return the array.
    """
    items = []
    for fn in glob.glob(f"{content_directory}/*.md"):
        with open(fn, 'r') as file:
            frontmatter, content = re.split("^\+\+\+\+\+$", file.read(), 1, re.MULTILINE)
        item = toml.loads(frontmatter)
        item['content'] = markdown.markdown(content)

        items.append(item)

    # sort in reverse chronological order
    items.sort(key=lambda x: x["date"],reverse=True)

    return items


def main():
    #load the configurations
    config = load_config("config.toml")