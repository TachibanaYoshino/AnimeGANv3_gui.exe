from Crypto.Cipher import AES
import base64, io
from PIL import Image

def AES_de(data, key = 'uae06dk7mcki632j',  vi = '1234567887654321'):
    # The decryption process is written in reverse of the encryption process
    # Re-encode the ciphertext string into binary form
    data = data.encode("utf-8")
    # Decode base64 encoding into byte
    data = base64.b64decode(data)
    # Create decryption object
    AES_de_obj = AES.new(key.encode("utf-8"), AES.MODE_ECB, )
    # Complete decryption
    AES_de_str = AES_de_obj.decrypt(data)
    # Remove padded spaces
    AES_de_str = AES_de_str.strip(b'\0')
    # Decode plaintext
    # AES_de_str = AES_de_str.decode("utf-8")
    return AES_de_str


def image_to_base64(path):
    with open(path, 'rb') as img:
        # Encode using base64
        b64encode = base64.b64encode(img.read())
        b64_encode = b64encode.decode()
        # Return base64 encoded string
        return b64_encode


def open_image(img_b64decode):
    image = io.BytesIO(img_b64decode)
    img = Image.open(image)
    img.show()


# Convert base64 to image
def base64_to_image(base64_encod_str):
    img_b64decode = base64.b64decode(base64_encod_str)
    open_image(img_b64decode)
