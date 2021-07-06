#!/usr/bin/env python3
from __future__ import print_function

import sys
import rospy
import cv2
import time
import numpy as np
from pyzbar.pyzbar import decode
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

################PARAMETERS####################

node_name = str(rospy.get_param('node_name'))
topic_src = str(rospy.get_param('topic_src'))
topic_dest = str(rospy.get_param('topic_dest'))

################IMAGE CONVERTER CLASS####################

class image_converter:

	#initialisation du topic de source et de sortie
	def __init__(self):
		self.image_pub = rospy.Publisher(topic_dest,Image, queue_size=1, latch=False)

		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber(topic_src,Image,self.callback)
		print("node init")

	#fonction qui traite l'image reçu sur le subscriber
	def callback(self,data):
		print("img reçu")
		print("time")
		print(time.time())
		
		#formatage de l'image du format image de ros vers un format exploitable par opencv
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
			print("img convert")
		except CvBridgeError as e:
			print(e)


		#Partie de l'algo qui analyse la frame
		cv_image = code_decoder(cv_image)

		print("img traite")
		cv2.waitKey(0)


		#reformatage et envoi sur le topic de publication
		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
			print("img send")
		except CvBridgeError as e:
			print(e)
		print("#####")



####################FONCTIONS ANALYSE IMAGE################################

#fonction qui repère et traduit un qr code ou un code barre dans la frame
def code_decoder(img):
	for barcode in decode(img):
		data = barcode.data.decode('utf-8')
		typecode = barcode.type
		print("code type : " + typecode)
		print("code lu : " + data)
		pts = np.array([barcode.polygon],np.int32)
		pts = pts.reshape((-1,1,2))
		cv2.polylines(img,[pts],True,(255,0,255),5)
		pts2 = barcode.rect
		cv2.putText(img,typecode+" : "+data,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
	return img

####################MAIN################################

def main(args):
	ic = image_converter()
	rospy.init_node(node_name, anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
