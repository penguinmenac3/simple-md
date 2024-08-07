# Simple MD

> A library to help generate simple documents with ease.


## Getting Started

### Installation

Install the library using pip.

```bash
pip install simple-md
```


### Usage

The following example shows you how to create a basic document in HTML or Markdown.
When choosing HTML or MD, note that HTML can embed images, while MD needs them to be stored separately.
However, MD is easier to process with AI language models downstream.

```python
from simple_md import HTMLDocument, MDDocument, MultiDocument, fmt

# Create a new document HTMLDocument, MDDocument or MultiDocument
document = MDDocument(document_path="test.md")

document.add_heading("Features")
document.add_paragraph("Add an image from a numpy opencv image.")
document.add_image(img, bgr=True)

document.add_paragraph("Add a matplotlib plot.")
plt.imshow(img[:,:,::-1])  # Plot image using matplotlib.
document.add_plt()

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
```


## Contributing

Currently there are no guidelines on how to contribute, so the best thing you can do is open up an issue and get in contact that way.
In the issue we can discuss how you can implement your new feature or how to fix that nasty bug.

To contribute, please fork the repositroy on github, then clone your fork. Make your changes and submit a merge request.


## License

This repository is under MIT License. Please see the [full license here](LICENSE).
