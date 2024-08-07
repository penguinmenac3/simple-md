from typing import List, Any
import numpy as np
import matplotlib.pyplot as plt

from simple_md.document import Document
from simple_md.document_html import HTMLDocument
from simple_md.document_md import MDDocument


class MultiDocument(Document):
    def __init__(self,
                 document_path: str,
                 title: str = "",
                 author: str = "",
                 brand_color: str = "#071C4C",
                 autoflush: bool = False,
                 echo: bool = False,
                 css: str = "",
                 include_style: bool = True):
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
        :param include_style: (Default: True) Include the CSS style for
            the MD, disable if your viewers do not support it.
        """
        if not document_path.endswith(".*"):
            raise RuntimeError("The document path must end on '.*' " + 
                               "since it is a markdown and html document.")
        self.md = MDDocument(document_path.replace(".*", ".md"), title, author,
                           brand_color, autoflush, echo, css, include_style)
        self.html = HTMLDocument(document_path.replace(".*", ".html"), title, author,
                               brand_color, autoflush, False, css)
        super().__init__(document_path, "", "", brand_color, autoflush, echo)

    def flush(self) -> None:
        """
        Write the document to disk.
         
        Automatically done after each add, unless you specify differently.
        """
        self.md.flush()
        self.html.flush()

    def add_heading(self, text: str, level: int = 2, flush: bool | None = None) -> None:
        """
        Add a heading to the document.
        """
        self.md.add_heading(text, level, flush)
        self.html.add_heading(text, level, flush)

    def add_infobox(self, text: str, flush: bool | None = None) -> None:
        """
        Add an infobox to the document.
        """
        self.md.add_infobox(text, flush)
        self.html.add_infobox(text, flush)

    def add_paragraph(self, text: str, flush: bool | None = None) -> None:
        """
        Add a text to the document.
        """
        self.md.add_paragraph(text, flush)
        self.html.add_paragraph(text, flush)

    def add_code(self, text: str, flush: bool | None = None) -> None:
        """
        Add a preformated code section to the document.
        """
        self.md.add_code(text, flush)
        self.html.add_code(text, flush)

    def add_exception(self, flush: bool | None = None) -> None:
        """
        Add an exception to the document.
        """
        self.md.add_exception(flush)
        self.html.add_exception(flush)

    def add_image(self, image: np.ndarray, bgr=False, embed=True, encoding: str = "jpg", style: str = "", new_line=True, flush: bool | None = None) -> None:
        """
        Add a numpy image to the document.
        """
        self.md.add_image(image, bgr, embed, encoding, style, new_line, flush)
        self.html.add_image(image, bgr, embed, encoding, style, new_line, flush)

    def add_plt(self, no_close=False, embed=True, style: str = "", new_line=True, flush: bool | None = None) -> None:
        """
        Add a matplotlib plot to the document.

        Use this instead of the `plt.show()` or `plt.imsave()` call.
        """
        fig = plt.gcf()
        canvas = fig.canvas
        plt.tight_layout()
        canvas.draw()
        width, height = canvas.get_width_height()
        img_arr = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
        img_arr = img_arr.reshape(int(height), int(width), -1)
        if not no_close:
            plt.close()
        self.add_image(np.array(img_arr), embed=embed, style=style, new_line=new_line, flush=flush)

    def add_video(self, images: List[str], fps: float, style: str = "", new_line=True, flush: bool | None = None) -> None:
        """
        Add a numpy image to the document.
        """
        assert len(images) > 2
        self.md.add_video(images[:2], fps, style, new_line, flush)
        self.html.add_video(images, fps, style, new_line, flush)

    def add_table(self, header: list[Any], body: list[list[Any]], flush: bool | None = None) -> None:
        self.md.add_table(header, body, flush)
        self.html.add_table(header, body, flush)

    def add_separator(self, flush: bool | None = None) -> None:
        self.md.add_separator(flush)
        self.html.add_separator(flush)
