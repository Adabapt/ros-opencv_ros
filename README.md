# OpenCV_ros package

## Nécessite:

OpenCV
CV_Bridge
ROS

## Installation:

Télecharger le dossier
Mettre le dossier dans le source de catkin workspace
Faire un catkin_make
Faire source devel/setup.bash

## Fonctionnements:

On lance la node avec :
Roslaunch opencv_ros opencv_ros_node.launch

Le package initialise donc le topic publisher et subscriber.
Dès qu'il reçoit une image sur le topic subscriber il la traduit au format d'OpenCV grâce à CV_Bridge.
Puis, pour y faire un petit traitement on analyse l'image pour trouver et traduire des éventuelles qr code ou code barre grâce à pyzbar. Puis on affiche un cadre autour ainsi que les infos déchiffrées.
Enfin, on retraduit l'image au format de ROS grâce à CV_Bridge et on la publie.

## Notes:

Lien Github vers CV_Bridge :
http://wiki.ros.org/vision_opencv?distro=noetic
