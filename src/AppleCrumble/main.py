import click
import yaml
import os

def init():
   os.mkdir("_content")
   os.makedirs("_site/static")
   create_new_page("index")
   open("_site/static/styles.css", "w")

def create_new_page(page_name:str):
    if not (os.path.exists(f"_content/{page_name}")):
        os.mkdir(f"_content/{page_name}")
        
        with open(f"_content/{page_name}/{page_name}.md", "w") as md_file:
            md_file.write("# ***This is my new page!***")
        
        with open(f"_content/{page_name}/{page_name}.yaml", "w") as yaml_file:
            yaml_file.write("title: \"My New Page!\" \n")
            yaml_file.write("style: \"styles.css\" \n")


@click.command()
@click.option('--p', default=None, help='The name of the page that you want to make.')
def make_page(p : str):
    if p == None:
        click.echo("Page name not specified, please specify the name of the page that you want to make.")
        return
    else:
        create_new_page(p)
    
@click.command()
@click.option('--m', default=None, help='The markdown file that you want to compile into HTML.')
def build(m : str):
    if m == None:
        click.echo("No folder specified, please specify a folder.")
        return

    with open(f"_content/{m}/{m}.yaml") as yaml_file:
        readable_yaml = yaml.load(yaml_file, yaml.FullLoader)
        style = readable_yaml['style']
        title = readable_yaml['title']

        open(f"_site/static/{style}", "w")
        
        with open(f"_content/{m}/{m}.md") as md_file:
            if not (os.path.exists(f"_site/{m}")):
                os.mkdir(f"_site/{m}")

            with open(f"_site/{m}.html", "w") as html_file:
                html_file.write("<!DOCTYPE html>\n")
                html_file.write("<html>\n")
                
                html_file.write("\n<head>\n")
                html_file.write("\n<meta charset=\"UTF-8\">\n")
                html_file.write("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
                html_file.write(f"<title> {title} </title>\n")
                html_file.write(f"<link href=\"/_site/static/{style}\" rel=\"stylesheet\" type=\"text/css\" media=\"all\">\n")
                html_file.write("\n</head>\n")

                html_file.write("\n<body>\n")

                for line in md_file:
                    if line.startswith("<") or line.strip("\n").endswith(">"):
                        html_file.write(line) # Skips the whole shebang if the line is already in html
                    else:
                        tag = parse_tag(line)
                        contents = parse_contents(line, tag)
                        html_contents = convert_contents_to_html(contents)
                        converted_line = convert_lines_to_html(html_contents, tag)
                        html_file.write(f"{converted_line} \n")

                html_file.write("\n")
                html_file.write("</body>\n")
                html_file.write("\n")
                html_file.write("</html>")

# Adding the functions from parser and converter here because i can't figure out how to add them as a dependency

def parse_tag(line : str):
    if line == "\n":
        return "br"
    elif line.startswith("#"):
        number_of_hashes = 0
        increment = 0

        while True:
            if line[increment] == "#":
                number_of_hashes += 1
                increment += 1
            else:
                if number_of_hashes > 6: # Limits heading to H6 since thats the smallest a heading can go
                    number_of_hashes = 6 
                break

        return ("h" + str(number_of_hashes))
    else:
        return "p"

def parse_contents(line : str, tag : str):
    tags = { # There's most definitely a better way to do this but im lazy.
        'h1' : '# ', # The extra space is intentional so that the contents don't all begin with a space
        'h2' : '## ',
        'h3' : '### ',
        'h4' : '#### ',
        'h5' : '##### ',
        'h6' : '###### ',
        'p' : '' # The paragraph doesn't have a space because it doesn't have a prefix
    }

    if tag == 'br':
        return '\n'
    else:
        return line.strip(tags[tag]).strip("\n")

### Converts .md lines into html
def convert_lines_to_html(contents : str, tag : str):
    if tag == "br":
        return (f"<{tag}>")
    else:
        return (f"<{tag}> {contents} </{tag}>")

def convert_contents_to_html(contents : str): 
    words = contents.split()
    
    for i in range(len(words)): # This is so fucked dude
        words[i] = get_bold_and_italic(words[i])
        words[i] = get_code_block(words[i])
    
    contents = " ".join(words)
    return contents

def find_and_replace(word:str, targets:list, html_replacement:str):
    for target in targets:
        if word.startswith(target):
            word = f"<{html_replacement}>" + word.removeprefix(target)
        elif word.endswith(target):
            word = word.removesuffix(target) + f"</{html_replacement}>"
    return word

def get_code_block(word : str):
    return find_and_replace(word, ["`"], "code")

def get_bold_and_italic(word : str):
    if word.startswith("***") or word.startswith("___"):
        word = "<strong><em>" + word.removeprefix("***").removeprefix("___")
    elif word.endswith("***") or word.endswith("___"):
        word = word.removesuffix("***").removesuffix("___") + "</em></strong>"
    else:
        word = find_and_replace(word, ["**", "__"], "strong")
        word = find_and_replace(word, ["*", "_"], "em")

    return word