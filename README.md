![AppleCrumble Logo](https://cdn.hackclub.com/01a1ebc0-43b3-7697-a4b4-6f231963e134/IMG_6478.png)
# AppleCrumble

AppleCrumble is a stupid-simple command-line based SSG (static-site generator) that takes your markdown (.md) files and YAML files and turns them into HTML files able to be read by the browser.

## Installation

To install AppleCrumble, make sure you have pip installed. Then run:

` pip install AppleCrumble `

in your terminal.

After that, AppleCrumble is now able to be used anywhere on your computer!

## Development

### Creating a new AppleCrumble project

To create a new site using AppleCrumble, navigate to the directory you want to use for your site in your terminal, and then run the command:

` AppleCrumble-init `

This command will create two sub-directories: `_content` and `_site`, and will also create a basic initial page folder called `index`.

### Creating a new page

To create a new page, run the command:

` AppleCrumble-create_new_page --p="pagenamegoeshere" `

That will create a new directory under `_content` named `pagenamegoeshere` that contains two files,  `pagenamegoeshere.md` and `pagenamegoeshere.yaml`. The markdown file is where you'll do all the actual writing for your new page, while the YAML file contains two very important pieces of data: the title of the page, and the CSS file that your page will use as its style.

The CSS file will be created at build time if it doesn't already exist in the `_site/static` subdirectory.

### Building your page

When you've finished writing in your beautiful markdown file, you're going to want to turn it into HTML that the browser can actually use. To do so, simply run this command:

` AppleCrumble-build --m="pagenamegoeshere" `

This will take the markdown and YAML files for that specific page, and compile them into one `pagenamegoeshere.html` file stored in the `_site` directory. After that, you should be able to open the file in your browser and see your beautiful webpage. In order to make an update to your page, simply make a change to the markdown or YAML file and run the build command again.

## Limitations

As of version 0.1.0, AppleCrumble is very simplistic, only being able to convert a few simple markdown tags into HTML. However, more updates and improvements are planned for the future. In addition, you can also use plain HTML in your markdown files, or make additions to the built HTML files if you need to accomplish something AppleCrumble can't.

## AI Disclosure

Absolutely zero AI was used throughout the process of making this project.