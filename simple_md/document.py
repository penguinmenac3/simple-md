from typing import List, Any
import numpy as np
import matplotlib.pyplot as plt


DEFAULT_STYLE = """
body {
    background-color: #AAAAAA;
}
.content {
    max-width: 800px;
    background-color: #FFFFFF;
    margin: auto;
    margin-top: 1em;
    margin-bottom: 1em;
    padding-top: 0em;
    padding-left: 2em;
    padding-right: 2em;
    padding-bottom: 3em;
    border-radius: 0.3em;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}
img, video {
    max-width: 100%;
    border-radius: 0.3em;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    padding-bottom: 0em;
    padding-top: 0em;
    margin-top: 0.75em;
    margin-bottom: 0.75em;
    line-height:1.5em;
}
p {
    padding-bottom: 0em;
    padding-top: 0em;
    margin-top: 0.2em;
    margin-bottom: 0.5em;
    line-height:1.5em;
}
h1, h2, h3, h4, h5, h6 {
    color: {brand_color};
    padding-bottom: 0em;
    padding-top: 2em;
    margin-top: 0em;
    margin-bottom: 0.5em;
}
h1:first-child {
    padding-top: 1.2em;
}
h1 {
    border-bottom: 1px solid gray;
}
h2, h3, h4, h5, h6 {
    border-bottom: 0px solid gray;
}
blockquote {
    border-left: 4px solid {brand_color};
    padding: 0.6em;
    padding-left: 1em;
    border-radius: 0.3em;
    margin-left: 0.5em;
    margin-right: 0.5em;
    background-color: whitesmoke;
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
blockquote p {
    margin-bottom: 0.1em;
}
pre {
    max-width: 100%;
    overflow: auto;
    background-color: #EEEEEE;
    border-radius: 0.3em;
    padding: 1em;
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);
    margin-top: 0.75em;
    margin-bottom: 0.75em;
    line-height:1.5em;
}
table {
    border-collapse: collapse;
    font-size: 0.9em;
    font-family: sans-serif;
    min-width: 400px;
    max-width: 100%;
    overflow: auto;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    padding-bottom: 0em;
    padding-top: 0em;
    margin-top: 0.75em;
    margin-bottom: 0.75em;
    line-height:1.5em;
}
thead tr {
    background-color: {brand_color};
    color: #ffffff;
    text-align: left;
}
th,
td {
    padding: 12px 15px;
}
tbody tr {
    border-bottom: 1px solid #dddddd;
}

tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}

tbody tr:last-of-type {
    border-bottom: 2px solid {brand_color};
}
"""


class Document(object):
    def __init__(self,
                 document_path: str,
                 title: str = "",
                 author: str = "",
                 brand_color: str = "#071C4C",
                 autoflush: bool = False,
                 echo: bool = False):
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
        """
        self._document_path = document_path
        self._title = title
        self._brand_color = brand_color
        self._autoflush = autoflush
        self._echo = echo
        self.appendix_id = 1
        if title != "":
            self.add_heading(title, level=1)
        if author != "":
            self.add_infobox(f"Author: {author}")

    def flush(self) -> None:
        """
        Write the document to disk.
         
        Automatically done after each add, unless you specify differently.
        """
        raise NotImplementedError("Must be implemented by child class.")

    def _maybe_flush(self, flush: bool | None):
        if flush is None:
            flush = self._autoflush
        if flush:
            self.flush()

    def add_heading(self, text: str, level: int = 2, flush: bool | None = None) -> None:
        """
        Add a heading to the document.
        """
        raise NotImplementedError("Must be implemented by child class.")

    def add_infobox(self, text: str, flush: bool | None = None) -> None:
        """
        Add an infobox to the document.
        """
        raise NotImplementedError("Must be implemented by child class.")

    def add_paragraph(self, text: str, flush: bool | None = None) -> None:
        """
        Add a text to the document.
        """
        pass

    def add_code(self, text: str, flush: bool | None = None) -> None:
        """
        Add a preformated code section to the document.
        """
        raise NotImplementedError("Must be implemented by child class.")

    def add_exception(self, flush: bool | None = None) -> None:
        """
        Add an exception to the document.
        """
        raise NotImplementedError("Must be implemented by child class.")

    def add_image(self, image: np.ndarray, bgr=False, embed=True, encoding: str = "jpg", style: str = "", new_line=True, flush: bool | None = None) -> None:
        """
        Add a numpy image to the document.
        """
        pass

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
        pass

    def add_table(self, header: list[Any], body: list[list[Any]], flush: bool | None = None) -> None:
        pass

    def add_separator(self, flush: bool | None = None) -> None:
        pass


def fmt(
        text: str,
        color: str = "",
        background: str = "",
        size: str = "",
        bold: bool = False,
        italic: bool = False,
        style: str = "",
        css_class: str = "") -> str:
    """
    Wrap a text in a span allowing it to be formated.

    Provided attributes allow you to quickly set styles.
    For a specific, uncommon attribute use the style
    parameter and specify a html style string.
    You can also specify a css_class if you provide
    some styles in the header of the document.
    
    Returns a string containing the formatted message as HTML.
    """
    if color != "":
        style = f"color:{color};{style}"
    if background != "":
        style = f"background-color:{background};{style}"
    if size != "":
        style = f"font-size:{size};{style}"
    if bold:
        style = f"font-weight:bold;{style}"
    if italic:
        style = f"font-style:italic;{style}"
    if style != "":
        style = f" style='{style}'"
    if css_class != "":
        css_class = f" class='{css_class}'"
    return f"<span{style}{css_class}>{text}</span>"
