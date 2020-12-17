# Referencia
# Adrian Rosebrock, Measuring size of objects in an image with OpenCV, PyImageSearch, https://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/, accessed on 15 December 2020

# pacotes utilizados
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import matplotlib.pyplot as plt
import argparse
import imutils
import cv2
import math
import random as rng
rng.seed(12345)

# Desenha uma reta na imagem
def desenhaDistancia(pt1,pt2,imagem,linha,raio):
	p1 = [int(pt1[0]),int(pt1[1])]
	p2 = [int(pt2[0]),int(pt2[1])]
	cv2.line(imagem, (p1[0], p1[1]), (p2[0], p2[1]),(255, 0, 255), linha)
	cv2.circle(imagem, (p1[0], p1[1]), raio, (0, 0, 255), -1)
	cv2.circle(imagem, (p2[0], p2[1]), raio, (255, 0, 0), -1)

# Desenha um pixel na imagem
def pintarPixel(x,y,imagem,c,pe):
	if cv2.pointPolygonTest(c, (x,y), False) == 0:
		pe.append([x,y])

# Calcula a reta entre dois pontos
def linhaBresenham(pt1,pt2,imagem,c,pe):
	p1 = [int(pt1[0]),int(pt1[1])]
	p2 = [int(pt2[0]),int(pt2[1])]
	escala = imagem.shape[0]
	deltaX = 0
	deltaY = 0
	x = 0
	y =  0
	p = 0
	if p2[1] < p1[1]:
		if ((p2[0] + p2[1] < p1[0] + p1[1]) and p2[0] < p1[0]):
			linhaBresenham(p2,p1,imagem,c,pe)
			return
		
		p1[1] = (escala-1) - p1[1]
		p2[1] = (escala-1) - p2[1]
			
		deltaX = p2[0] - p1[0]
		deltaY = p2[1] - p1[1]
		
		if deltaX < deltaY:
			x = p1[0]
			p = (2*deltaX) - deltaY
			for y in range(p1[1],p2[1]+1):
				pintarPixel(x,(escala-1)-y,imagem,c,pe)
				if p >= 0:
					x = x+1
					p = p + (2*(deltaX-deltaY))
				else:
					p = p + (2*deltaX)
		else:
			y = p1[1]
			p = (2*deltaY) - deltaX
			for x in range(p1[0],p2[0]+1):
				pintarPixel(x,(escala-1)-y,imagem,c,pe)
				if p >= 0:
					y = y+1
					p = p + (2*(deltaY-deltaX))
				else:
					p = p + (2*deltaY)

	else:
		if p2[0] < p1[0]:
			linhaBresenham(p2,p1,imagem,c,pe)
			return
		deltaX = p2[0] - p1[0]
		deltaY = p2[1] - p1[1]

		if deltaX < deltaY:
			x = p1[0]
			p = (2 * deltaX) - deltaY
			for y in range(p1[1],p2[1]):
				pintarPixel(x,y,imagem,c,pe)
				if p >= 0:
					x = x + 1
					p = p + (2 * (deltaX - deltaY))
				else:
					p = p + (2 * deltaX)
		else:
			y = p1[1]
			p = (2* deltaY)- deltaX
			for x in range(p1[0],p2[0]):
				pintarPixel(x,y,imagem,c,pe)
				if p >= 0:
					y = y+1
					p = p + (2 * (deltaY-deltaX))
				else:
					p = p + (2 * deltaY)

# Retorna da distância em pixels entre dois pixels na imagem
def calculaDistanciaLargura(pt1,pt2,imagem,c,linha,raio):
	disPts = 0
	pontosBorda = []
	linhaBresenham(pt1, pt2, imagem,c,pontosBorda)
	if len(pontosBorda) > 1:
		print('bresenham')
		disPts = dist.euclidean(pontosBorda[0], pontosBorda[-1])
		desenhaDistancia(pontosBorda[0], pontosBorda[-1], imagem, linha, raio)
	else:
		print('normal')
		disPts = dist.euclidean(pt1, pt2)
		desenhaDistancia(pt1, pt2, imagem, linha, raio)
	return disPts

# Retorna da distância em pixels entre dois pixels na imagem
def calculaDistanciaAltura(pt1,pt2,imagem,c,linha,raio):
	disPts = 0
	pontosBorda = []
	linhaBresenham(pt1, pt2, imagem,c,pontosBorda)
	if len(pontosBorda) > 1:
		print('bresenham')
		pontoAltura = [pontosBorda[0][0], pontosBorda[-1][1]]
		disPts = dist.euclidean(pontosBorda[0], pontoAltura)
		desenhaDistancia(pontosBorda[0], pontoAltura, imagem, linha, raio)
		desenhaDistancia(pontosBorda[-1], pontoAltura, imagem, linha, raio)
	else:
		print('normal')
		pontoAltura = [pt1[0], pt2[1]]
		disPts = dist.euclidean(pt1, pontoAltura)
		desenhaDistancia(pt1, pontoAltura, imagem, linha, raio)
		desenhaDistancia(pt2, pontoAltura, imagem, linha, raio)
	return disPts

# Retorna o ponto médio entre dois pontos
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# Comando no terminal
# python3 alturaPasto.py --i caminho da imagem --l largura da barra em cm --a altura da barra em cm
ap = argparse.ArgumentParser()
ap.add_argument("-imagem", "--i", required=True, help="caminho da imagem")
ap.add_argument("-largura", "--l", type=float, required=True, help="largura da barra(em cm)")
ap.add_argument("-altura", "--a", type=float, required=True, help="altura da barra(em cm)")
ap.add_argument("-pathResult", "--p", required=True, help="altura da barra(em cm)")
args = vars(ap.parse_args())

imagem = cv2.imread(args["i"])

imagemHSV = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

minRED = np.array([0, 120, 70])
maxRED = np.array([10, 255, 255])
maskRED1 = cv2.inRange(imagemHSV, minRED, maxRED)

minRED = np.array([170, 120, 70])
maxRED = np.array([180, 255, 255])
maskRED2 = cv2.inRange(imagemHSV, minRED, maxRED)
	
maskRED = maskRED1 + maskRED2
imagemCOR = cv2.bitwise_and(imagem, imagem, mask=maskRED)

imagemGRAY = cv2.cvtColor(imagemCOR, cv2.COLOR_BGR2GRAY)
imagemBLUR = cv2.GaussianBlur(imagemGRAY, (5, 5), 0)

thresh = 10
canny = cv2.Canny(imagemBLUR, thresh, 100)

contours, hierarchy = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

imagemCNTS = imagemCOR.copy()
for i in range(len(contours)):
	cv2.drawContours(canny, contours, i, 255, 2, cv2.LINE_8, hierarchy, 0)

contours, hierarchy = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for i in range(len(contours)):
	box = cv2.minAreaRect(contours[i])
	box = cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	box = perspective.order_points(box)
	
	color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
	cv2.drawContours(imagemCNTS, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)


alturaBarra = args["a"]
modoBresenham = True

linha = 3
raio = 2
imagemCopy = imagem.copy()

for c in contours:
	if cv2.contourArea(c) < 100:
		continue
	
	box = cv2.minAreaRect(c)
	box = cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	
	box = perspective.order_points(box)
	cv2.drawContours(imagemCopy, c, -1, (255, 255, 255), linha)
	cv2.drawContours(imagemCopy, [box.astype("int")], -1, (0, 255, 0), linha)
	
	(tl, tr, br, bl) = box
	
	imagemCopy2 = imagemCopy.copy()
	cv2.circle(imagemCopy2, (tl[0], tl[1]), raio, (255, 0, 0), -1)
	cv2.circle(imagemCopy2, (tr[0], tr[1]), raio, (255, 0, 0), -1)
	cv2.circle(imagemCopy2, (br[0], br[1]), raio, (255, 0, 0), -1)
	cv2.circle(imagemCopy2, (bl[0], bl[1]), raio, (255, 0, 0), -1)
	
	distaciaTLTR = dist.euclidean(tl, tr)
	distaciaTLBL = dist.euclidean(tl, bl)
	
	if distaciaTLTR > distaciaTLBL:
		if tl[1] < tr[1]:
			aux = tr
			tr = tl
			tl = bl
			bl = br
			br = aux
		else:
			aux = tl
			tl = tr
			tr = br
			br = bl
			bl = aux
			
	(tltrX, tltrY) = midpoint(tl, tr)
	pmt1 = midpoint(tl, tr)
	pmt2 = midpoint(tl, pmt1)
	pmt3 = midpoint(pmt1, tr)

	(blbrX, blbrY) = midpoint(bl, br)
	pmb1 = (blbrX, blbrY)
	pmb2 = midpoint(bl, pmb1)
	pmb3 = midpoint(pmb1, br)

	(tlblX, tlblY) = midpoint(tl, bl)
	pml1 = (tlblX, tlblY)
	pml2 = midpoint(tl, pml1)
	pml3 = midpoint(pml1, bl)

	(trbrX, trbrY) = midpoint(tr, br)
	pmr1 = (trbrX, trbrY)
	pmr2 = midpoint(tr, pmr1)
	pmr3 = midpoint(pmr1, br)

	if modoBresenham is True:
		print('largura')
		dlr1 = calculaDistanciaLargura(pml1, pmr1, imagemCopy, c, linha, raio)
		dlr2 = calculaDistanciaLargura(pml2, pmr2, imagemCopy, c, linha, raio)
		dlr3 = calculaDistanciaLargura(pml3, pmr3, imagemCopy, c, linha, raio)

		print('altura')
		dtb1 = calculaDistanciaAltura(pmt1, pmb1, imagemCopy, c, linha, raio)
		dtb2 = calculaDistanciaAltura(pmt2, pmb2, imagemCopy, c, linha, raio)
		dtb3 = calculaDistanciaAltura(pmt3, pmb3, imagemCopy, c, linha, raio)
	else:
		dlr1 = dist.euclidean(pml1, pmr1)
		desenhaDistancia(pml1,pmr1,imagemCopy,linha,raio)
		dlr2 = dist.euclidean(pml2, pmr2)
		desenhaDistancia(pml2,pmr2,imagemCopy,linha,raio)
		dlr3 = dist.euclidean(pml3, pmr3)
		desenhaDistancia(pml3,pmr3,imagemCopy,linha,raio)

		pontoAltura = [pmt1[0],pmb1[1]]
		dtb1 = dist.euclidean(pmt1, pontoAltura)
		desenhaDistancia(pmt1,pontoAltura,imagemCopy,linha,raio)
		desenhaDistancia(pmb1,pontoAltura,imagemCopy,linha,raio)

		pontoAltura = [pmt2[0],pmb2[1]]
		dtb2 = dist.euclidean(pmt2, pontoAltura)
		desenhaDistancia(pmt2,pontoAltura,imagemCopy,linha,raio)
		desenhaDistancia(pmb2,pontoAltura,imagemCopy,linha,raio)

		pontoAltura = [pmt3[0],pmb3[1]]
		dtb3 = dist.euclidean(pmt3, pontoAltura)
		desenhaDistancia(pmt3,pontoAltura,imagemCopy,linha,raio)
		desenhaDistancia(pmb3,pontoAltura,imagemCopy,linha,raio)

	if dtb1 == 0:
		continue
	if dtb2 == 0:
		continue
	if dtb3 == 0:
		continue
	if dlr1 == 0:
		continue
	if dlr2 == 0:
		continue
	if dlr3 == 0:
		continue

	distanciaPixelsTBMedia = (dtb1 + dtb2 + dtb3)/3
	distanciaPixelsLRMedia = (dlr1 + dlr2 + dlr3)/3

	pixelPorCMMedia = distanciaPixelsTBMedia * args["l"]
	
	disTB = pixelPorCMMedia / distanciaPixelsLRMedia
	disLR = pixelPorCMMedia / distanciaPixelsTBMedia

	alturaPasto = alturaBarra - disTB

	cv2.putText(imagemCopy, "{:.2f}".format(disTB), (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

	cv2.putText(imagemCopy, "{:.2f}".format(disLR), (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

	cv2.putText(imagemCopy, "{:.2f}".format(alturaPasto), (int(blbrX - 15), int(blbrY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
	
	cv2.putText(imagemCopy, "Altura do pasto: {:.2f}".format(alturaPasto), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 5, (0), 7)

	cv2.imwrite(args["p"], imagemCopy)


# Copyright (c) 2020 PyImageSearch.com
# SIMPLE VERSION
# Feel free to use this code for your own projects, whether they are
# purely educational, for fun, or for profit. THE EXCEPTION BEING if
# you are developing a course, book, or other educational product.
# Under *NO CIRCUMSTANCE* may you use this code for your own paid
# educational or self-promotional ventures without written consent
# from Adrian Rosebrock and PyImageSearch.com.
# LONGER, FORMAL VERSION
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# Notwithstanding the foregoing, you may not use, copy, modify, merge,
# publish, distribute, sublicense, create a derivative work, and/or
# sell copies of the Software in any work that is designed, intended,
# or marketed for pedagogical or instructional purposes related to
# programming, coding, application development, or information
# technology. Permission for such use, copying, modification, and
# merger, publication, distribution, sub-licensing, creation of
# derivative works, or sale is expressly withheld.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
