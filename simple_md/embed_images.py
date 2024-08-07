import cv2
import base64
import os


def main():
    import sys
    path = sys.argv[1]
    if os.path.isdir(path):
        for fname in os.listdir(path):
            if fname.endswith(".md"):
                embed_images(os.path.join(path, fname))
    else:
        embed_images(path)


def embed_images(fname: str) -> None:
    folder = os.path.dirname(fname)
    has_changes = False
    with open(fname, "r") as f:
        data = f.read().split("\n")
    images = []
    for idx in range(len(data)):
        line = data[idx]
        content = ""
        if "<image " in line:
            content = _find_tag_content(line, "<image ", ">")
        if "<img " in line:
            content = _find_tag_content(line, "<img ", ">")
        if "![" in line:
            content = _find_tag_content(line, "![", ")")
            url = _find_tag_content(content + ")", "](", ")")
            line = line.replace(f"![{content})", f"<img src='{url}' />")
            data[idx] = line
            content = f"src='{url}'"
        if "src" in content and "src='data" not in content and "src=\"data" not in content:
            url_start = content.index("src=") + len("src=")
            url_end = content.index(content[url_start], url_start + 1)
            url = content[url_start + 1:url_end]
            image_path = os.path.join(folder, url)
            images.append(image_path)
            encoded = _encode_image(image_path)
            data[idx] = line.replace(url, encoded)
            has_changes = True
    if has_changes:
        #backup(fname, images)
        _remove_files(images)
        with open(fname, "w") as f:
            f.write("\n".join(data))


def _find_tag_content(line: str, start_str: str, end_str: str) -> str:
    start = line.index(start_str)
    end = line.index(end_str, start)
    if start < 0:
        print("ERROR: Cannot find start of image tag. Skipping...")
        return ""
    if end < 0:
        print("ERROR: Cannot find end of image tag. Skipping...")
        return ""
    return line[start+len(start_str):end]


def _encode_image(fname: str, encoding: str = "jpg") -> str:
    image = cv2.imread(fname)
    encoded_img = cv2.imencode(f".{encoding}", image)
    b64_string = base64.b64encode(encoded_img[1]).decode('utf-8')
    return f"data:image/{encoding};base64,{b64_string}"


def _backup(fname, images):
    folder = os.path.dirname(fname)
    backup_folder = os.path.join(folder, "backup")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    with open(fname, "r") as f:
        original = f.read().split("\n")
    with open(fname.replace(folder, backup_folder), "w") as f:
        f.write("\n".join(original))
    for image in images:
        os.rename(image, image.replace(folder, backup_folder))


def _remove_files(files):
    for fpath in files:
        os.remove(fpath)


if __name__ == "__main__":
    main()
