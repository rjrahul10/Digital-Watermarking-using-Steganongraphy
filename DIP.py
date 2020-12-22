# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:01:24 2020

@author: Rahul Kumar
"""
import cv2
from PIL import Image
import numpy as np
def imageacq():
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while(result):
        ret,frame = videoCaptureObject.read()
        cv2.imwrite("Pic.png",frame)
        result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()
def Enhancement(img):
    image = cv2.imread(img)
    gamma = 1.2
    gamma_corrected = np.array(255*(image / 255) ** gamma, dtype = 'uint8') 
    cv2.imwrite("Pic.png", gamma_corrected)

def sharpness(img):
    im = cv2.imread("Pic.png")
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    im = cv2.filter2D(im, -1, kernel)
   
class TextSteganography(object):
    def encode(img, msg):
        image = Image.open(img,'r')
        w,h = image.size
        arr = np.array(list(image.getdata()))
        if image.mode == 'RGB':
            n = 3
            m = 0
        elif image.mode == 'RGBA':
            n = 4
            m = 1
        tot_pix = arr.size//n
        msg += "stgno"
        code = ''.join([format(ord(i), "08b") for i in msg])
        req_pix = len(code)
        if req_pix > tot_pix:
            print("ERROR: Need larger file size")
        else:
            index=0
            for p in range(tot_pix):
                for q in range(m, n):
                    if index < req_pix:
                        arr[p][q] = int(bin(arr[p][q])[2:9] + code[index], 2)
                        index += 1

            arr=arr.reshape(h, w, n)
            out_img= Image.fromarray(arr.astype('uint8'), image.mode)
        return out_img
    def decode(img):
        image = Image.open(img, 'r')
        arr = np.array(list(image.getdata()))
        if image.mode == 'RGB':
            n = 3
            m = 0
        elif image.mode == 'RGBA':
            n = 4
            m = 1
        tot_pix = arr.size//n
        hid_bits = ""
        for p in range(tot_pix):
            for q in range(m, n):
                hid_bits += (bin(arr[p][q])[2:][-1])

        hid_bits = [hid_bits[i:i+8] for i in range(0, len(hid_bits), 8)]
        msg = ""
        for i in range(len(hid_bits)):
            if (msg[-5:]=="stgno"):
                break
            else:
                msg += chr(int(hid_bits[i], 2))
        return msg[:-5]
    def __init__(self):
        print("1.Encode text to the image\n2.Decode text from the image")
        ans = int(input())
        if(ans ==1):
            img = input("Enter the image with extension: ")
            msg = input("Enter the secret message: ")
            out = TextSteganography.encode(img,msg)
            img = input("Enter the image name to be saved: ")
            out.save(img)
        else:
            img = input("Enter the image with extension ")
            msg = TextSteganography.decode(img)
            print("The hidden message is ", msg)

class ImageSteganography(object):
    def i2b(rgb):
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))
    def b2i(rgb):
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))
    def merge_rgb(rgb1,rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb
    def merge(img1, img2):
       
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()
        print("Processing....")
        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = ImageSteganography.i2b(pixel_map1[i, j])
                rgb2 = ImageSteganography.i2b(( 0, 0, 0))
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = ImageSteganography.i2b(pixel_map2[i, j])
                rgb = ImageSteganography.merge_rgb(rgb1, rgb2)
                pixels_new[i, j] = ImageSteganography.b2i(rgb)
        print("Processed...")
        return new_image
    def __init__(self):
        img = input("Enter image name(with extension) : ")
        img1 = Image.open(img, 'r')
        img  = input("Enter the hiding image: ")
        img2 = Image.open(img,'r')
        Enhancement(img)
        img = input("Enter the output name : ")
        img3 = Image.open("Pic.png",'r')
        output = ImageSteganography.merge(img1,img3)
        output.save(img)
    
def main():
    print("Digital Watermarking")
    print("1.Text Steganography\n2.Image Steganography")
    choice = int(input())
    print("Want to click photo from webcam(1/0)")
    ans = int(input())
    if(ans ==1):
        print("Image saved as Pic.png")
        imageacq()
        img ="Pic.png"
        Enhancement(img)
        sharpness()
    if(choice==1):
        TextSteganography()
    else:
        ImageSteganography()

main()