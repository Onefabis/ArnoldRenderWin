import os
import sys
import warnings
import time

paths = (os.getenv("Path"))
arnoldPaths = [ x for x in paths.split(";") if "Arnold" in x ]
for a in arnoldPaths:
	sys.path.append(a)

try:
	from arnold import *
except:
	# Will warn you if Arnold render path is not assigned in your environment
	warnings.warn("Add Arnold to environment variable and re-open this window")

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

class Ui_AR_Win(object):

	def setupUi(self, AR_Win):

		# Create main Windet
		AR_Win.setObjectName("Arnold Win")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
		AR_Win.setSizePolicy(sizePolicy)
		AR_Win.setMinimumSize(QtCore.QSize(900, 685))
		AR_Win.setMaximumSize(QtCore.QSize(900, 16777215))

		# Set the main Windet as central widget
		self.centralwidget = QtWidgets.QWidget(AR_Win)
		self.centralwidget.setObjectName("centralwidget")
		AR_Win.setCentralWidget(self.centralwidget)

		# Create vertical layout and attach it to the central widget
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setObjectName("verticalLayout")

		# Create horizontal layout to hold Rnder, Color and Browse Line with label and button
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")

		# Add Render button
		self.Render_Button = QtWidgets.QPushButton(self.centralwidget)
		self.Render_Button.setMinimumSize(QtCore.QSize(80, 30))
		self.Render_Button.setObjectName("Render_Button")

		# Attach render button to Horizontal layout
		self.horizontalLayout.addWidget(self.Render_Button)

		self.progress = QtWidgets.QProgressBar(self.centralwidget)
		self.progress.setGeometry(20, 20, 20, 20)

		# Attach render button to Horizontal layout
		self.horizontalLayout.addWidget(self.progress)

		# Add Color picker button
		self.Color_Button = QtWidgets.QPushButton(self.centralwidget)
		self.Color_Button.setMinimumSize(QtCore.QSize(80, 30))
		self.Color_Button.setObjectName("Color_Button")

		# Attach color button to Horizontal layout
		self.horizontalLayout.addWidget(self.Color_Button)

		# Attach horizontal that holds all buttons to the main vertical one
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.Render_result = QtWidgets.QFrame(self.centralwidget)

		# Render result widget that will show rendered jpeg
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Render_result.sizePolicy().hasHeightForWidth())
		self.Render_result.setSizePolicy(sizePolicy)
		self.Render_result.setMinimumSize(QtCore.QSize(880, 550))
		self.Render_result.setObjectName("Render_result")

		# Attach Render result widget to the vertical layout
		self.verticalLayout.addWidget(self.Render_result)

		# LogOutput scroll area that will show the scrollable result of log output widget
		self.LogOutput = QtWidgets.QScrollArea(self.centralwidget)
		self.LogOutput.setWidgetResizable(True)
		self.LogOutput.setObjectName("LogOutput")

		# Create log output widget content that will be shown from log file
		self.scrollAreaWidgetContents = QtWidgets.QTextEdit()
		self.scrollAreaWidgetContents.setReadOnly(True)
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 878, 69))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		self.LogOutput.setWidget(self.scrollAreaWidgetContents)
		self.verticalLayout.addWidget(self.LogOutput)

		# Call retranslateUi function that sets all names to the buttons and labe
		self.retranslateUi(AR_Win)
		QtCore.QMetaObject.connectSlotsByName(AR_Win)

	def retranslateUi(self, AR_Win):
		_translate = QtCore.QCoreApplication.translate
		AR_Win.setWindowTitle(_translate("Arnold Win", "Arnold Win"))
		self.Render_Button.setText(_translate("Arnold Win", "Render"))
		self.Color_Button.setText(_translate("Arnold Win", "Object color"))


class QThread1(QtCore.QThread):

	sig1 = pyqtSignal(str)
	tempPath = os.environ['TEMP'].replace( '\\', '/') + "/"
	logFile = tempPath + 'scene1.log'

	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.lineCount = 0

	def run(self):
		self.running = True
		while self.running:
			try:
				thefile = open(self.logFile, 'rb')

				lines = thefile.readlines()

				if self.lineCount == len(lines):
					time.sleep(0.1)
					continue

				for x in range( self.lineCount, len(lines) ):
					self.sig1.emit(str(lines[x]))
				self.lineCount = len(lines)

			except Exception as err:
				pass


class QThread2(QtCore.QThread):

	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)

	def run(self):
		self.running = True

		while self.running:
			tempPath = os.environ['TEMP'].replace( '\\', '/') + "/"
			logFile = tempPath + 'scene1.log'
			jpgFile = tempPath + 'scene1.jpg'

			AiBegin()
			AiMsgSetLogFileName(logFile)
			AiMsgSetConsoleFlags(AI_LOG_ALL)

			# create sphere
			sph = AiNode("sphere")
			AiNodeSetStr( sph, "name", "mysphere")
			AiNodeSetVec( sph, "center", 0.0, 4.0, 0.0)
			AiNodeSetFlt( sph, "radius", 4.0)

			# create red shader
			shader1 = AiNode("standard")
			AiNodeSetStr(shader1, "name", "myshader1")
			AiNodeSetRGB( shader1, "Kd_color", self.col[0], self.col[1], self.col[2] )
			AiNodeSetFlt( shader1, "Ks", 0.05 )

			# assign the red shader to the sphere
			AiNodeSetPtr(sph, "shader", shader1)

			# create a perspective camera
			camera = AiNode("persp_camera")
			AiNodeSetStr(camera, "name", "mycamera")

			# position the camera (alternatively you can set 'matrix')
			AiNodeSetVec(camera, "position", 0., 10., 35.)
			AiNodeSetVec(camera, "look_at", 0., 3., 0.)
			AiNodeSetFlt(camera, "fov", 45.)

			# create a point light source
			light = AiNode("point_light")
			AiNodeSetStr(light, "name", "mylight")

			# position the light (alternatively use 'matrix')
			AiNodeSetVec(light, "position", 15., 30., 15.)
			AiNodeSetFlt(light, "intensity", 4500.) # alternatively, use 'exposure'
			AiNodeSetFlt(light, "radius", 4.) # for soft shadows

			# get the global options node and set some options
			options = AiUniverseGetOptions()
			AiNodeSetInt(options, "AA_samples", 8)
			AiNodeSetInt(options, "xres", 880)
			AiNodeSetInt(options, "yres", 550)
			AiNodeSetInt(options, "GI_diffuse_depth", 4)

			# set the active camera (optional, since there is only one camera)
			AiNodeSetPtr(options, "camera", camera)

			# create an output driver node
			driver = AiNode("driver_jpeg")
			AiNodeSetStr(driver, "name", "mydriver")
			AiNodeSetStr(driver, "filename", jpgFile)
			AiNodeSetFlt(driver, "gamma", 2.2)

			# create a gaussian filter node
			filter = AiNode("gaussian_filter")
			AiNodeSetStr(filter, "name", "myfilter")

			# assign the driver and filter to the main (beauty) AOV,
			# which is called "RGBA" and is of type RGBA
			outputs_array = AiArrayAllocate(1, 1, AI_TYPE_STRING)
			AiArraySetStr(outputs_array, 0, "RGBA RGBA myfilter mydriver")
			AiNodeSetArray(options, "outputs", outputs_array)

			# finally, render the image!
			AiRender(AI_RENDER_MODE_CAMERA)

			# Arnold session shutdown
			AiEnd()

			self.running = False


class MyWin(QtWidgets.QMainWindow):

	# Initialize the main window
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.ui = Ui_AR_Win()
		self.ui.setupUi(self)

		# Connect functions to the buttons
		self.ui.Render_Button.clicked.connect(self.Render)
		self.ui.Color_Button.clicked.connect(self.Picker)

		# Set dark grey color to the main window
		self.setStyleSheet( 'QMainWindow{ background-color:#1f1f1f }' )

		# Set dark grey color to tehe Render button
		self.ui.Render_Button.setStyleSheet( 'QPushButton{ background-color: #444444; border: 1px solid #4d4d4d; color: #919c9c }' )

		# Set the initial color as red one
		self.col = (1.0, 0.02, 0.02)
		init_Color_Button = [ x * 255.0 for x in self.col ]
		self.ui.Color_Button.setStyleSheet( 'QPushButton{ background-color:rgb(%s,%s,%s); border: 1px solid #4d4d4d }' % ( init_Color_Button[0], init_Color_Button[1], init_Color_Button[2] ) )

		# Set Render Image widget color
		self.ui.Render_result.setStyleSheet( 'QFrame { border: 1px solid #414141 }' )

		# Set Log Output text color
		self.ui.scrollAreaWidgetContents.setStyleSheet( 'QTextEdit { background-color: #444444; border: 1px solid #414141; color: #919c9c }' )

		# Set Log Output text color
		self.ui.progress.setStyleSheet( 'QProgressBar { text-align: center; background-color: #444444; border-color: #414141; color: #919c9c} QProgressBar::chunk{background-color: #646464;} ' )

		self.tempPath = os.environ['TEMP'].replace( '\\', '/') + "/"
		open(self.tempPath + 'scene1.log' , 'w').close()

		sig1 = pyqtSignal(str)
		self.thread1 = QThread1()
		self.thread1.start()
		self.thread1.sig1.connect(self.on_info)

	# Called when the Render button is pressed
	def Render(self):
		self.on_but3()
		self.thread1.lineCount = 0

	def on_but3(self):
		self.thread3 = QThread2()
		self.thread3.start()
		self.thread3.col = self.col

	def on_info(self, info ):

		self.ui.scrollAreaWidgetContents.append(str(info))
		self.ui.scrollAreaWidgetContents.moveCursor(QtGui.QTextCursor.End)
		if 'Arnold shutdown' in info:
			jpgFile = self.tempPath + 'scene1.jpg'
			self.ui.Render_result.setStyleSheet( "QFrame{ background-image: url(%s);}" %jpgFile )
			self.ui.Render_result.repaint()
			self.ui.Render_result.show()
		elif '% done' in info:
			words = info.split( ' ' )
			num = [ x for x in words if '%' in x ]
			progressPer = float(num[0].replace( '%', '' ) )
			if progressPer == 100:
				self.ui.progress.setValue( 0 )
			else:
				self.ui.progress.setValue( progressPer )

	# Function to set shader color
	def Picker( self ):

		# Launch Color picker window
		color = QtWidgets.QColorDialog.getColor()
		rgba = color.getRgb()

		# Transform QColor to appropriate rgb color
		self.col = ( rgba[0] / 255.0, rgba[1] / 255.0, rgba[2] / 255.0 )

		# Set color of the Color button font depending on the background color
		if rgba[0] * 0.299 + rgba[1] * 0.587 + rgba[2] * 0.114 > 105:
			tColor = '#000000'
		else:
			tColor = '#bebebe'
		self.ui.Color_Button.setStyleSheet( 'QPushButton{background-color: %s; color: %s; border: 1px solid #4d4d4d }' %( color.name(), tColor ) )


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	myapp = MyWin()
	myapp.show()
	sys.exit(app.exec_())
