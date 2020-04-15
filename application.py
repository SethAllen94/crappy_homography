import cv2
import numpy as np
import tkinter
import tkinter.filedialog
from homography_functions import get_destination_points, unwarp
from matplotlib import pyplot as plt


#TODO Make TKinter Work for Selecting Files
# Issue with Dialogbox not disappearing after selection made. 
# Tried root_udpate dit not work.

coords = []

def click_event(event, x, y, flags, param):
	font = cv2.FONT_HERSHEY_SIMPLEX

	if event == cv2.EVENT_LBUTTONDOWN:
		if len(coords) < 4:
			coords.append([x,y])
			strXY = f'{str(x)},{str(y)}'
			cv2.circle(img, (x, y), 4, (255,255,255), -1)
			cv2.circle(img, (x, y), 3, (255,0,255), -1)
			cv2.putText(img, str(len(coords)), (x+10,y), font, 0.5, (255, 255, 255), 1)
			cv2.imshow('image', img)

		else:
			original_corners = np.float32(coords)
			destination_corners, h, w = get_destination_points(original_corners)
			unwarped = unwarp(plot_img, original_corners, destination_corners)

			# plot
			fig, (ax1, ax2) = plt.subplots(1, 2)
			# convert image colors
			correct_img = cv2.cvtColor(plot_img, cv2.COLOR_BGR2RGB)
			correct_unwarped = cv2.cvtColor(unwarped, cv2.COLOR_BGR2RGB)

			ax1.imshow(correct_img)
			x = [original_corners[0][0], original_corners[2][0], original_corners[3][0], original_corners[1][0], original_corners[0][0]]
			y = [original_corners[0][1], original_corners[2][1], original_corners[3][1], original_corners[1][1], original_corners[0][1]]
			ax1.plot(x, y, color='fuchsia', linewidth=3)
			ax1.set_title('Region of Interest')
			ax2.imshow(correct_unwarped)
			ax2.set_title('Perspective Corrected Image')
			fig.suptitle('Homography Test')
			fig.show()

# def select_image():
# 	# hide root window
# 	root = tkinter.Tk()
# 	root.withdraw()

# 	# Get image path
# 	path = tkinter.filedialog.askopenfilename(filetypes = [('Windows Bitmaps', '*.bmp'),
# 										('JPEG', '*.jpeg'),
# 										('JPG', '*.jpg'),
# 										('Portable Network Graphic', '*png')])
# 	root.update()
# 	return path

					 
while True:
	#path = select_image()
	path = 'test images/cat-art.jpg'
	img = cv2.imread(path)
	# make image for plotting that will not have annotations from user.
	plot_img = img.copy()
	cv2.imshow('image', img)

	cv2.setMouseCallback('image', click_event)

	k = cv2.waitKey(0)

	if k == 27: # wait for ESC key to exit
	    break

cv2.destroyAllWindows()

