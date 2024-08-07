import matplotlib.pyplot as plt
import cv2
import os
import shutil

from simple_md import Document, HTMLDocument, MDDocument, MultiDocument, fmt


LOREM_IPSUM = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et
ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem
ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing
elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna
aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo
dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus
est Lorem ipsum dolor sit amet."""


def _test_common(document: Document, base_path: str):
    document.add_heading("Formatted Text")
    special_text = fmt('World', color='#6278AA',
                       bold=True, italic=True, size='1.2em')
    document.add_paragraph(f"Hello {special_text}!")
    document.add_paragraph(LOREM_IPSUM)
    document.add_paragraph(LOREM_IPSUM)

    document.add_heading("Code / Exceptions")
    document.add_code("""pip install simple-md""")
    try:
        raise RuntimeError("Foobar")
    except:
        document.add_exception()

    document.add_heading("Table")
    document.add_paragraph("Add a table.")
    document.add_table(
        header=["Feature", "Code"],
        body=[
            ["Heading", "document.add_image(text)"],
            ["SubHeading", "document.add_image(text, indent=3)"],
            ["Paragraph", "document.add_paragraph(text)"],
            ["Info", "document.add_infobox(text)"],
            ["Image", "document.add_image(image, bgr=True)"],
            ["Matplotlib", "document.add_plt()"],
            ["Video", "document.add_video(images, fps=30)"],
            ["Code", "document.add_code(code)"],
            ["Separator", "document.add_separator()"],
            ["Exceptions", "document.add_exception()"],
        ]
    )

    document.add_separator()
    document.add_heading("Media")
    
    document.add_paragraph("Add image direct, external and as png.")
    img = cv2.imread(f"{base_path}/data/image.jpg")
    document.add_image(img, bgr=True, style="width:32%", new_line=False)
    document.add_image(img, bgr=True, embed=False, style="width:32%", new_line=False)
    document.add_image(img, bgr=True, embed=False, encoding="png", style="width:32%")
    
    document.add_paragraph("Add a plot from matplotlib and create a video from frames.")
    
    plt.imshow(img[:,:,::-1])
    document.add_plt(style="width:49%", new_line=False)

    folder = f"{base_path}/data/video"
    paths = [os.path.join(folder, x) for x in os.listdir(folder) if x.endswith(".png") or x.endswith(".jpg")]
    document.add_video(sorted(paths), fps=30, style="width:49%")


def test_html(base_path):
    document_path = os.path.join(base_path, "html")
    if os.path.exists(document_path):
        shutil.rmtree(document_path)
    os.mkdir(document_path)
    _test_common(HTMLDocument(
        document_path=os.path.join(document_path, "test.html"),
        title="HTML Test",
        author="Michael Fürst",
        brand_color="#FF0000",
        autoflush=True,
        echo=True,
        css=""
    ), base_path=base_path)

def test_md(base_path):
    document_path = os.path.join(base_path, "md")
    if os.path.exists(document_path):
        shutil.rmtree(document_path)
    os.mkdir(document_path)
    _test_common(MDDocument(
        document_path=os.path.join(document_path, "test.md"),
        title="Markdown Test",
        author="Michael Fürst",
        brand_color="green",
        autoflush=True,
        echo=True,
        css=""
    ), base_path=base_path)

def test_multi(base_path):
    document_path = os.path.join(base_path, "multi")
    if os.path.exists(document_path):
        shutil.rmtree(document_path)
    os.mkdir(document_path)
    _test_common(MultiDocument(
        document_path=os.path.join(document_path, "test.*"),
        title="Multioutput Test",
        author="Michael Fürst",
        brand_color="#071C4C",
        autoflush=True,
        echo=True,
        css=""
    ), base_path=base_path)

if __name__ == "__main__":
    test_md(os.path.dirname(__file__))
    test_html(os.path.dirname(__file__))
    test_multi(os.path.dirname(__file__))
