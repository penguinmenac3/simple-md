from typing import List, Any
import base64
import traceback
import imageio
import cv2
import numpy as np


from simple_md.document import Document, DEFAULT_STYLE


HTML_TEMPLATE="""<html>
<head>
<title>{title}</title>
<style>{style}</style>
</head>
<body>
<div class="content">{content}

</div>
</body>
</html>
"""


class HTMLDocument(Document):
    def __init__(self,
                 document_path: str,
                 title: str = "",
                 author: str = "",
                 brand_color: str = "#071C4C",
                 autoflush: bool = False,
                 echo: bool = False,
                 css: str = ""):
        """
        Create a document of an execution of the program.

        :param document_path: Where to save the document.
        :param title: (Default: "") The title of the document.
        :param author: (Default: "") The author of the document.
        :param brand_color: (Default: "#071C4C") The hex color code for
            your brand color used in the document.
        :param autoflush: (Default: False) Automatically flush after
            each operation.
        :param echo: (Default: False) If all outputs should be also
            printed to the commandline.
        :param css: (Default: "") CSS allows to use brand themes and
            customize the rendering.
        """
        if not document_path.endswith(".html"):
            raise RuntimeError("The document path must end on '.html' " + 
                               "since it is an html document.")
        self._css = css
        self._content = ""
        super().__init__(document_path, title, author, brand_color, autoflush, echo)

    def flush(self) -> None:
        """
        Write the document to disk.
         
        Automatically done after each add, unless you specify differently.
        """
        with open(self._document_path, "w") as f:
            style = DEFAULT_STYLE.replace("{brand_color}", self._brand_color)
            style = f"{style}\n{self._css}"
            style = style.replace("\n", " ")
            while "  " in style:
                style = style.replace("  ", " ")
            f.write(HTML_TEMPLATE.format(
                title=self._title,
                style=style,
                content=self._content
            ))

    def add_heading(self, text: str, level: int = 2, flush: bool | None = None) -> None:
        """
        Add a heading to the document.
        """
        self._content = f"{self._content}\n\n<h{level}>{text}</h{level}>"
        self._maybe_flush(flush)

    def add_infobox(self, text: str, flush: bool | None = None) -> None:
        """
        Add an infobox to the document.
        """
        self._content = f"{self._content}\n<blockquote>{text}</blockquote>"
        self._maybe_flush(flush)

    def add_paragraph(self, text: str, flush: bool | None = None) -> None:
        """
        Add a paragraph to the document.
        """
        self._content = f"{self._content}\n<p>{text}</p>"
        self._maybe_flush(flush)

    def add_code(self, text: str, flush: bool | None = None) -> None:
        """
        Add a preformated code section to the document.
        """
        self._content = f"{self._content}\n<pre>{text}</pre>"
        self._maybe_flush(flush)

    def add_exception(self, flush: bool | None = None) -> None:
        """
        Add an exception to the document.
        """
        text = traceback.format_exc()
        self._content = f"{self._content}\n<pre>{text}</pre>"
        self._maybe_flush(flush)

    def add_image(self, image: np.ndarray, bgr=False, embed=True, encoding: str = "jpg", style: str = "", new_line=True, flush: bool | None = None) -> None:
        """
        Add a numpy image to the html document.
        """
        if not bgr and len(image.shape) == 3:
            # only do first 3 channels, as alpha needs to stay
            image = image.copy()
            image[:,:,0:3] = image[:,:,0:3][:,:,::-1]
        if style != "":
            style = f" style='{style}'"
        if embed:
            encoded_img = cv2.imencode(f".{encoding}", image)
            b64_string = base64.b64encode(encoded_img[1]).decode('utf-8')
            self._content = f"{self._content}\n<image {style} src='data:image/{encoding};base64,{b64_string}' />"
        else:
            path = self._document_path.replace(".html", f".{self.appendix_id:04d}.{encoding}")
            self.appendix_id += 1
            cv2.imwrite(path, image)
            relative_path = path.split('/')[-1]
            self._content = f"{self._content}\n<image {style} src='{relative_path}' />"
        if new_line:
            self._content = f"{self._content}\n<BR>"
        self._maybe_flush(flush)

    def add_video(self, images: List[str], fps: float, style: str = "", new_line=True, flush: bool | None = None) -> None:
        """
        Add a numpy image to the html document.
        """
        path = self._document_path.replace(".html", f".{self.appendix_id:04d}.mp4")
        self.appendix_id += 1
        with imageio.get_writer(path, mode='I', fps=fps) as writer:
            for filename in images:
                image = imageio.imread(filename)
                writer.append_data(image)
        if style != "":
            style = f" style='{style}'"
        relative_path = path.split('/')[-1]
        self._content = f"{self._content}\n<video {style} src='{relative_path}' controls autoplay loop muted></video>"
        if new_line:
            self._content = f"{self._content}\n<BR>"
        self._maybe_flush(flush)

    def add_table(self, header: list[Any], body: list[list[Any]], flush: bool | None = None):
        content = ""
        header_html = "".join([f"<th>{x}</th>" for x in header])
        content += f"<thead>\n<tr>{header_html}</tr>\n</thead>\n"
        content += "<tbody>\n"
        for line in body:
            row = "".join([f"<td>{x}</td>" for x in line])
            content += f"<tr>{row}</tr>\n"
        content += "</tbody>\n"
        table = f"<table>\n{content}</table>"
        self._content = f"{self._content}\n{table}"
        self._maybe_flush(flush)

    def add_separator(self, flush: bool | None = None):
        self._content = f"{self._content}\n<HR>"
        self._maybe_flush(flush)
