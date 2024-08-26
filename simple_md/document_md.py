from typing import List, Any
import base64
import traceback
import imageio
import cv2
import numpy as np


from simple_md.document import Document, DEFAULT_STYLE


class MDDocument(Document):
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
        self.linebuffer = []
        if not document_path.endswith(".md"):
            raise RuntimeError("The document path must end on '.md' " +
                               "since it is a markdown document.")
        with open(document_path, "w") as f:
            if include_style:
                md_style = DEFAULT_STYLE.replace("{brand_color}", brand_color)
                md_style = md_style.replace(".content", "body") + css
                md_style = md_style.replace("\n", " ")
                while "  " in md_style:
                    md_style = md_style.replace("  ", " ")
                f.write(f"<style>{md_style}</style>\n\n")
            else:
                f.write("")
        super().__init__(document_path, title, author, brand_color, autoflush, echo)

    def flush(self):
        if len(self.linebuffer) > 0:
            with open(self._document_path, "a") as f:
                while len(self.linebuffer) > 0:
                    line = self.linebuffer.pop(0)
                    f.write(f"{line}\n")
                    if self._echo:
                        print(line)
    
    def add_heading(self, text: str, level: int = 2, flush: bool | None = None):
        indentation = "#" * level
        self.linebuffer.extend([
            f"{indentation} {text}",
            "",
        ])
        self._maybe_flush(flush)

    def add_infobox(self, text: str, flush: bool | None = None):
        self.linebuffer.extend([
            f"> {line}"
            for line in text.split("\n")
        ] + [
            ""
        ])
        self._maybe_flush(flush)

    def add_paragraph(self, text: str, flush: bool | None = None):
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")
        self.linebuffer.extend(
            text.split("\n") + [""])
        self._maybe_flush(flush)

    def add_code(self, text: str, flush: bool | None = None) -> None:
        """
        Add a preformated code section to the document.
        """
        self.linebuffer.extend(
            ["```"] + text.split("\n") + ["```", ""]
        )
        self._maybe_flush(flush)

    def add_exception(self, flush: bool | None = None) -> None:
        """
        Add an exception to the document.
        """
        text = traceback.format_exc()
        self.linebuffer.extend(
            ["```"] + text.split("\n") + ["```", ""]
        )
        self._maybe_flush(flush)

    def add_image(self, image: np.ndarray, bgr=False, embed=True, encoding: str = "jpg", style: str = "", new_line=True, flush: bool | None = None) -> None:
        """
        Add a numpy image to the document.
        """
        if not bgr and len(image.shape) == 3:
            # only do first 3 channels, as alpha needs to stay
            image = image.copy()
            image[:,:,0:3] = image[:,:,0:3][:,:,::-1]
        if style != "":
            style = f" style='{style}'"
        add_line = [""] if new_line else []
        if embed:
            encoded_img = cv2.imencode(f".{encoding}", image)
            b64_string = base64.b64encode(encoded_img[1]).decode('utf-8')
            self.linebuffer.extend([
                f"<image class='image' {style} src='data:image/{encoding};base64,{b64_string}' />",
            ] + add_line)
        else:
            path = self._document_path.replace(".md", f".{self.appendix_id:04d}.{encoding}")
            self.appendix_id += 1
            cv2.imwrite(path, image)
            relative_path = path.split('/')[-1]
            self.linebuffer.extend([f"<image {style} src='{relative_path}' />"] + add_line)
        self._maybe_flush(flush)


    def add_video(self, images: List[str], fps: float, style: str = "", new_line=True, autoplay: bool = True, flush: bool | None = None) -> None:
        """
        Add a numpy image to the document.
        """
        path = self._document_path.replace(".md", f".{self.appendix_id:04d}.mp4")
        self.appendix_id += 1
        with imageio.get_writer(path, mode='I', fps=fps) as writer:
            for filename in images:
                image = imageio.imread(filename)
                writer.append_data(image)
        if style != "":
            style = f" style='{style}'"
        add_line = [""] if new_line else []
        relative_path = path.split('/')[-1]
        autoplay_str = "autoplay " if autoplay else ""
        self.linebuffer.extend([
                f"<video class='image' {style} src='{relative_path}' controls {autoplay_str}loop muted></video>",
            ] + add_line)
        self._maybe_flush(flush)

    def add_table(self, header: list[Any], body: list[list[Any]], flush: bool | None = None):
        table = [
            "| " + " | ".join([str(x).replace("|", "/") for x in header]) + " |",
            "| " + " | ".join(["---" for _ in header]) + " |"
        ]
        for line in body:
            table.append("| " + " | ".join([str(x).replace("|", "/") for x in line]) + " |")
        self.linebuffer.extend(
            table + [""])
        self._maybe_flush(flush)

    def add_separator(self, flush: bool | None = None):
        self.linebuffer.extend(["", "---", ""])
        self._maybe_flush(flush)
