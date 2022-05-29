import PIL.Image
import io

# JPG files end by FF D9
class JPGHider:
    def jpg_hide_message(self, img_path, message):
        with open(img_path, "ab") as f:  # ab -> append bytes
            f.write(bytes(message, "utf-8"))

    def decode_hidden_message(self, img_path):
        with open(img_path, "rb") as f:  # rb -> read bytes
            content = f.read()
            offset = content.index(bytes.fromhex("FFD9"))  # index konca pliku jpg
            f.seek(offset + 2)  # FFD9 zajmuje 2 bajty
            return f.read()  # czytanie ukrytej wiadomosci

    def hide_image(self, main_image_path, hidden_image_path):
        with open(main_image_path, "ab") as main_image, open(hidden_image_path, "rb") as hidden_image:
            hidden_content = hidden_image.read()
            main_image.write(hidden_content)
            

    def unload_and_save_hidden_image(self, img_path: str, new_file_name: str):
        with open(img_path, "rb") as f:
            content = f.read()
            offset = content.index(bytes.fromhex("FFD9"))

            f.seek(offset + 2)

            new_img = PIL.Image.open(io.BytesIO(f.read()))
            new_img.save(new_file_name + ".png")

    def cleanup_image(self, img_path):
        content = None
        with open(img_path, "rb") as f:
            content = f.read()
            offset = content.index(bytes.fromhex("FFD9"))

            f.seek(offset + 2)
            hidden_bytes = f.read()
            content = content.replace(hidden_bytes, b"")

        with open(img_path, "wb") as file:
            file.write(content)


anon_path = "anonymous.jpg"
linux_path = "linux.png"
hider = JPGHider()
