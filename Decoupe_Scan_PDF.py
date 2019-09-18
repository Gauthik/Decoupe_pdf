#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      GAUTHIER
#
# Created:     18/09/2019
# Copyright:   (c) GAUTHIER 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import cv2
import numpy as np
##import fitz
from pdf2image import convert_from_path

#pip install pymupdf
#pip install fitz
#Visual C++ 14 required

def conversion_pdf_png(file, path_dossier_png=""):
    if not verification_fichier_est_pdf(file):
        assert False, "Le fichier n'est pas un pdf"

    filename = os.path.basename(file[:-4])
    sortie_pil = convert_from_path(file)
    sortie_pil[0].save(str(path_dossier_png) + "\\" + str(filename) + ".png")


def decoupe_png(file):
    if not verification_fichier_est_pdf(file):
        assert False, "Le fichier n'est pas un pdf"

    filename = file[:-4]

    img = cv2.imread(str(filename) + ".png")
    ## (1) Convert to gray, and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    ## (4) Crop and save it
    x,y,w,h = cv2.boundingRect(cnt)
    dst = img[y:y+h, x:x+w]
    cv2.imwrite(str(filename) + ".png", dst)
    pass

def verification_fichier_est_pdf(file):
    if file[-4:] != ".pdf":
        return False
    return True

def recuperation_liste_fichiers_pdf(path_dossier):
    #On récupère la liste des pdf présents dans le dossier
    liste_fichiers = os.listdir(path_dossier)

    liste_fichiers_pdf = []
    for fichier in liste_fichiers:
        if fichier[-4:] == ".pdf":
            liste_fichiers_pdf.append(fichier)

    return liste_fichiers_pdf


if __name__ == '__main__':
    PATH_DOSSIER = r"Scans_PDF"
    PATH_DOSSIER_PNG = r"Fichiers_PNG"
    liste_fichiers_pdf = recuperation_liste_fichiers_pdf(PATH_DOSSIER)

    for fichier in liste_fichiers_pdf:
        conversion_pdf_png(PATH_DOSSIER + "\\" + fichier, PATH_DOSSIER_PNG)
        decoupe_png(PATH_DOSSIER_PNG + "\\" + fichier)

