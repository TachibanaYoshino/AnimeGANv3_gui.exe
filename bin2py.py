import base64
import os.path
from Crypto.Cipher import AES
from config import image_to_base64

# Content that needs to be encrypted
filename = {
"background.png":"bg",
"kitsune.ico":"ico",
"FaceDetector0.onnx":"faceDet",
}

'''
AES symmetric encryption algorithm
'''
# Encrypt plain text with AES
def AES_en(data, key='saidfjkk0ksio455',iv = '1234567887654321'):
    # Complete strings less than 16 bytes long
    while len(data) % 16 != 0:
        data+=b'\0'
    # Create encrypted objects
    AES_obj = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    # Complete encryption data: bytes
    AES_en_str = AES_obj.encrypt(data)
    # Encode it with base64 AES_en_str: bytes
    AES_en_str = base64.b64encode(AES_en_str)
    # Finally, convert the ciphertext into a string str
    AES_en_str = AES_en_str.decode("utf-8")
    return AES_en_str



def pic2py(files, py_name):
    write_data = []
    for f in files:
        if f.endswith('.onnx'): # Use encryption
            print(f,  filename[os.path.basename(f)])
            open_pic = open("%s" % f, 'rb')
            # b64str = base64.b64encode(open_pic.read())
            # write_data.append('%s = "%s"\n' % (filename[os.path.basename(f)], b64str.decode('utf-8')))
            encryptstr = AES_en(open_pic.read()) # The default key it uses will also be encrypted again.
            open_pic.close()
            write_data.append('%s = """%s"""\n' % (filename[os.path.basename(f)], encryptstr))
        else:
            if (f.endswith('.png') or f.endswith('.ico')) and os.path.basename(f) in list(filename.keys()): # Use base64
                print(f, filename[os.path.basename(f)])
                b64str = image_to_base64(f)
                write_data.append('%s = "%s"\n' % (filename[os.path.basename(f)], b64str))

    f = open('%s.py' % py_name, 'w+')
    f.write("#cython: language_level=3 \n")
    f.write(f"Author='{AES_en('saidfjkk0ksio455'.encode('utf-8'), key='uae06dk7mcki632j', iv='1234567887654321')}' \n")
    f.write(f"Key   ='{AES_en('miyaoxuyao16ziji'.encode('utf-8'), key='uae06dk7mc4i632j')}' \n")
    f.write(f"vi    ='{AES_en('0102030405060708'.encode('utf-8'), key='uae06dk7m1ki632j')}' \n")
    f.write("Time  ='2023.11' \n")
    for data in write_data:
        f.write(data)
    f.close()


if __name__ == '__main__':
    fd =r'./assets'
    pics = [os.path.join(fd,x) for x in os.listdir(fd) if x.split('.')[-1] in ['onnx', "png", "ico"]]
    print(pics)
    sorted(pics)
    pic2py(pics, 'assets_bin')
    print("ok")
