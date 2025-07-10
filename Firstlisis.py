import cv2
import numpy as np
import random
from stegano import lsb
import glob

def encrypt(what_to_hide):

    print("Images to choose from:")
    available_images = glob.glob("*.png")
    for file in available_images:
        if file != "FirstPhoto.png" and file != "SecondPhoto.png" and file != "IzlezenSoText.png" and file != "CombinedPhotos.png" :
            print(file)

    if what_to_hide == 2:

        img1 = input("Input the source of the image\n")
        message = input("Input the secret message\n")
        out_file = "IzlezenSoText.png"

        secret = lsb.hide(img1, message)
        secret.save(out_file)

    else :
        input1 = input("Input the source of the first image\n")
        img1 = cv2.imread(input1)
        input2 = input("Input the source of the image you want to be hidden in the first one\n")
        img2 = cv2.imread(input2)

        for i in range(img2.shape[0]):
            for j in range(img2.shape[1]):
                for l in range(3):

                    v1 = format(img1[i][j][l], '08b')
                    v2 = format(img2[i][j][l], '08b')
                    v3 = v1[:4] + v2[:4]

                    img1[i][j][l] = int(v3, 2)

        cv2.imwrite('CombinedPhotos.png', img1)
        cv2.imshow( 'Combined Photo', img1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def decrypt(what_to_hide):

    if what_to_hide == 2:

        out_path = "IzlezenSoText.png"
        secret_mess = lsb.reveal(out_path)
        print("The secret message was: " + secret_mess)

    else :
        img = cv2.imread('CombinedPhotos.png')
        width = img.shape[0]
        height = img.shape[1]

        img1 = np.zeros((width, height, 3), np.uint8)
        img2 = np.zeros((width, height, 3), np.uint8)

        for i in range(width):
            for j in range(height):
                for l in range(3):
                    v1 = format(img[i][j][l], '08b')
                    v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                    v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4

                    img1[i][j][l] = int(v2, 2)
                    img2[i][j][l] = int(v3, 2)

        cv2.imwrite('FirstPhoto.png', img1)
        cv2.imwrite('SecondPhoto.png', img2)

        cv2.imshow( 'First Photo', img1)
        cv2.imshow( 'Second Photo', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


whatToHide = int( input ("What do you want to hide?\nIf you want to hide an image type 1, if you want to hide a text message type 2: "))
encrypt(whatToHide)
wantDecrypt = input("Would you like to decrypt the photos? yes/no\n")
if wantDecrypt.lower() == "yes" :
    decrypt(whatToHide)
else :
    print("You chose to stay secretive")



















