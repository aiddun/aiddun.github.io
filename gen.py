import re
import os
import glob
import markdown2
import autopep8

template = ""
with open("template.html", "r") as t:
    template = t.read()


class Page:
    def __init__(self, path):
        self.path = path
        filename = os.path.basename(path)
    
        self.name = re.sub("\.[\S]*", "", filename)
        self.filetype = filename.replace(self.name + ".", "")
        with open(path, "r") as f:
            self.text = f.read()
        
        if self.filetype == "md":
            self.md_html = markdown2.markdown(self.text)
            self.is_link = False
        elif self.filetype == "link":
            self.link = self.text
            self.is_link = True
        else:
            print(f"error: invalid file type: {self.filetype}")
        pass

    def gen_link(self):
        if self.is_link:
            return f"<p><a href=\"{self.link}\">{self.name}</a></p>"
        else:
            path = "" if self.name == "home" else self.name
            return f"<p><a href=\"/{path}\">{self.name}</a></p>"


    def gen_html(self, page_template, pages):
        if (self.filetype != ".md"):
            pass 

        links = sorted([page.gen_link() for page in pages])
        links_html = "\n".join(links)

        html = page_template.replace("{title}", self.name).replace(
            "{content}", self.md_html).replace("{links}", links_html)

        # don't worry about html style as cloudflare will minify it for us
        return html


files = glob.glob("./pages/*")
pages = [Page(file) for file in files]

build_dir = "build/"
for page in pages:
    if not page.is_link:
        build_subdir = "" if page.name == "home" else f"{page.name}/"
        page_path = build_dir + build_subdir + "index.html"
        os.makedirs(os.path.dirname(page_path), exist_ok=True)

        with open(page_path, "w") as f:
            f.write(page.gen_html(template, pages))
