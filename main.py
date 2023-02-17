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
        item['slug'] = os.path.splitext(os.path.basename(file.name))[0]
        item['url'] = f"/{item['date'].year}/{item['date'].month:0>2}/{item['date'].day:0>2}/{item['slug']}/"
        items.append(item)

    # sort in reverse chronological order
    items.sort(key=lambda x: x["date"],reverse=True)

    return items

def load_support_content(file_path):
    with open(file_path, 'r') as file:
        frontmatter, content = re.split("^\+\+\+\+\+$", file.read(), 1, re.MULTILINE)

    item = toml.loads(frontmatter)
    item['content'] = markdown.markdown(content)

    return item


def load_templates(template_directory):
    """
    This function uses Jinja to create a Jinja environment that knows to look for templates in a paticular directory.
    """
    file_sys_loader = jinja2.FileSystemLoader(template_directory)
    return jinja2.Environment(loader=file_sys_loader)


def render_site(config, content, environment, output_directory):

    #Remove output directory and all its content if it exists and create a fresh output directory.
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    #Create a homepage
    index_template = environment.get_template('index.html')
    with open(f"{output_directory}/index.html", 'w') as file:
        file.write(index_template.render(config=config,content=content['posts']))

    #Create an about and error pages (support pages)
    support_template = environment.get_template('support.html')
    with open(f"{output_directory}/about.html", 'w') as file:
        file.write(support_template.render(config=config,content=content['about']))

    with open(f"{output_directory}/error.html", 'w') as file:
        file.write(support_template.render(config=config,content=content['error']))

    #Create post pages
    post_template = environment.get_template("post.html")
    for item in content["posts"]:
        path = f"{output_directory}/{item['url']}"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with open(path+"index.html", 'w') as file:
            file.write(post_template.render(this=item, config=config, content=content))


    #Create static files

    #Copy the files from our static directory to our public directory
    distutils.dir_util.copy_tree('static', 'public')




def main():
    #load the configurations
    config = load_config("config.toml")


    #Create content for the different pages
    content = {
        "posts": load_content_items("content/posts"),
        "about": load_support_content('content/about.md'),
        "error": load_support_content('content/error.md')
    }

    #load the template environment where all out layout are stored
    environment = load_templates('layout')
    render_site(config, content, environment, "public")


main()