import flet as ft
import cv2
import numpy as np
import base64

def to_base64(image):
    base64_image = cv2.imencode('.png', image)[1]
    base64_image = base64.b64encode(base64_image).decode('utf-8') 
    return base64_image


def main(page):

    # Create a blank image for the initial display,
    # image element does not support None for src_base64
    init_image = np.zeros((480, 640, 3), dtype=np.uint8) + 128
    init_base64_image = to_base64(init_image)

    image_src = ft.Image(src_base64=init_base64_image, width=640, height=480)
    image_dst = ft.Image(src_base64=init_base64_image, width=640, height=480)

    image_row = ft.Row([image_src, image_dst])

    image = None

    def edge_detection(e):
        nonlocal image
        if image is None:
            return
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 10, 200)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        base64_image = to_base64(edges)
        image_dst.src_base64 = base64_image
        image_dst.update()

    def on_file_selected(e):
        nonlocal image
        file_path = e.files[0].path
        print("file selected :", file_path)
        image = cv2.imread(file_path)
        base64_image = to_base64(image)
        image_src.src_base64 = base64_image
        image_src.update()


    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)


    def on_click(e):
        file_picker.pick_files(allow_multiple=False, 
                               file_type=ft.FilePickerFileType.IMAGE)

    button = ft.ElevatedButton("Select Image File", on_click=on_click)
    button_edge_detection = ft.ElevatedButton("Edge Detection", on_click=edge_detection)
    page.add(button)
    page.add(image_row)
    page.add(button_edge_detection)


ft.app(target=main)
