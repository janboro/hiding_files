import numpy as np
import PIL.Image

def hide_bytes(img_path, bytes_to_hide, least_significant_bits_len, hidden_img_path):
    image = PIL.Image.open(img_path, 'r')
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode == "P": # P for palette
        print("Not suported")
        exit()
    channels = 4 if image.mode == "RGBA" else 3
    pixels = img_arr.size // channels

    bits = len(bytes_to_hide)
    if bits > pixels:
        print("Not enough space to hide message")
    else:
        index = 0
        for i in range(pixels):
            for j in range(channels):
                if index < bits:
                    # 0b11111111 reprezantacji zawiera jako pierwsze dwa znaki 0b, wiec od tego indeksu kopiujemy bity
                    img_arr[i][j] = int(bin(img_arr[i][j])[2:-least_significant_bits_len] + bytes_to_hide[index], base=2)
                    index += 1

    img_arr = img_arr.reshape((height, width, channels))
    result = PIL.Image.fromarray(img_arr.astype('uint8'), image.mode)
    result.save(hidden_img_path)
    
def encode_message(img_path, message_to_hide,least_significant_bits_len, hidden_img_path):
    stop_indicator = "$KONIEC$"
    message_to_hide += stop_indicator
    byte_message = ''.join(f"{ord(character):08b}" for character in message_to_hide) # 08b wyznacza znaki ASCII z funkcji ord jako bity
    hide_bytes(img_path=img_path, bytes_to_hide=byte_message, least_significant_bits_len=least_significant_bits_len, hidden_img_path=hidden_img_path)

def extract_bits(img_path, least_significant_bits_len):
    image = PIL.Image.open(img_path, 'r')
    image_arr = np.array(list(image.getdata()))

    channels = 4 if image.mode == "RGBA" else 3
    pixels = image_arr.size // channels

    secret_bits = [bin(image_arr[i][j])[-least_significant_bits_len] for i in range(pixels) for j in range(channels)]
    secret_bits = ''.join(secret_bits)
    secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]
    return secret_bits

def extract_message(img_path, least_significant_bits_len):
    secret_bits = extract_bits(img_path,least_significant_bits_len)

    secret_message = [chr(int(secret_bits[i],base=2)) for i in range(len(secret_bits))]
    secret_message = ''.join(secret_message)
    stop_indicator = "$KONIEC$"
    if stop_indicator in secret_message:
        print(secret_message[:secret_message.index(stop_indicator)])
    else:
        print("Hidden message not found")

# def hide_file(img_path, file_to_hide_path):
#     with open(file_to_hide_path, 'rb') as file_to_hide:
#         bytes = file_to_hide.read()
# def extract_hidden_file(img_path):
#     pass
 
img_path = 'linux.png'
message_to_hide = "Moja ukryta wiadomosc"

encode_message(img_path=img_path, message_to_hide=message_to_hide, least_significant_bits_len=1, hidden_img_path='LSB_encoded.png')

print("Encoded")

decode_img = 'LSB_encoded.png'
extract_message(decode_img, 1)
