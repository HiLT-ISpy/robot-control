import math
import time
import os

import numpy as np
from naoqi import ALModule, ALProxy, ALBroker

def connect(address="bobby.local", port=9559, name="r", brokername="broker"):
	global broker
	broker = ALBroker(brokername, "0.0.0.0", 0, address, 9559)
	global r
	r = Robot(name, address, 9559)

def robot():
	global r
	return r

def broker():
	global broker
	if not broker:
		broker = ALBroker("broker", "0.0.0.0", 0, "bobby.local", 9559)
	return broker

class Robot(ALModule):
	def __init__( self, strName, address = "bobby.local", port = 9559):
		ALModule.__init__( self, strName )

		# text to speech
		self.tts = ALProxy("ALTextToSpeech", address, port)

		# memory
		self.mem = ALProxy("ALMemory", address, port)

		# robot movement
		self.motion = ALProxy("ALMotion", address, port)
		self.pose = ALProxy("ALRobotPosture", address, port)

		# face tracking
		self.track = ALProxy("ALFaceTracker", address, port)
		# initialize face-tracking to following with head movement only
		self.track.setWholeBodyOn(False)

		# gaze analysis
		self.gaze = ALProxy("ALGazeAnalysis", address, port)
		# set highest tolerance for determining if people are looking at the robot because those people's IDs are the only ones stored
		self.gaze.setTolerance(1)
		# start writing gaze data to robot memory
		self.gaze.subscribe("_")

		# camera
		self.cam = ALProxy("ALVideoDevice", address, port)

		# leds
		self.leds = ALProxy("ALLeds", address, port)

		self.colors = {
			"pink": 0x00FF00A2,
			"red": 0x00FF0000,
			"orange": 0x00FF7300,
			"yellow": 0x00FFFB00,
			"green": 0x000DFF00,
			"blue": 0x000D00FF,
			"purple": 0x009D00FF
		}

		# sound detection
		self.sound = ALProxy("ALSoundDetection", address, port)
		# initialize sound sensitivity
		self.sound.setParameter("Sensibility", 0.95)

	def __del__(self):
		print "End Robot Class"


	def say(self, text, block = True):
		"""
		Uses ALTextToSpeech to vocalize the given string.
		If "block" argument is False, makes call asynchronous,
		i.e. does not wait until it finishes talking to move on to next part of the code.
		"""

		if block:
			self.tts.say(text)

		else:
			self.tts.post.say(text)

	def wake(self, stiffness = 1.0):
		"""
		Turns stiffnesses on, goes to Crouch position, and lifts head
		"""

		self.motion.stiffnessInterpolation("Body", stiffness, 1.0)
		self.pose.goToPosture("Crouch", 0.2)
		self.turnHead(pitch = math.radians(-10))

	def rest(self):
		"""
		Goes to Crouch position and turns robot stiffnesses off
		"""

		self.motion.rest()

	def sit(self):
		"""
		Goes to Crouch position
		"""

		self.pose.goToPosture("Crouch")

	def stand(self):
		"""
		Robot stands
		"""

		self.pose.goToPosture("Stand", 0.4)

	def turnHead(self, yaw = None, pitch = None, speed = 0.2):
		"""
		Turns robot head to the specified yaw and/or pitch in degrees at the given speed.
		Yaw can range from 119.5 deg (left) to -119.5 deg (right) and pitch can range from 38.5 deg (down) to -29.5 deg (up).
		"""

		if not yaw is None:
			self.motion.setAngles("HeadYaw", math.radians(yaw), speed)
		if not pitch is None:
			self.motion.setAngles("HeadPitch", math.radians(pitch), speed)

	def moveRightArm(self, pitch): # add yaw!
		"""
		Extends robot's right arm to point at the specified yaw and pitch in degrees.
		The angles below are RShoulderPitch, RShoulderRoll, RElbowRoll, RWristYaw, and RHand.
		The angle ranges can be found at http://doc.aldebaran.com/1-14/family/robots/joints_robot.html#right-arm-joints
		For example, the pitch ranges from 119.5 (down) to 0 (horizontal) to -119.5 (up).
		"""

		angles = [pitch, 12, 39, 3, -8] # angles in degrees
		angles = [math.radians(angle) for angle in angles] # convert to radians
		angles.append(1) # also open hand
		times = [1, 1, 1.5, 1.5, 1.5, 1.5]
		self.motion.angleInterpolation("RArm", angles, times, True) # move to those arm angles and open hand

	def moveLeftArm(self, pitch): # add yaw!
		"""
		Extends robot's left arm to point at the specified yaw and pitch in degrees.
		The angles below are LShoulderPitch, LShoulderRoll, LElbowRoll, LWristYaw, and LHand.
		The angle ranges can be found at http://doc.aldebaran.com/1-14/family/robots/joints_robot.html#left-arm-joints
		For example, the pitch ranges from 119.5 (down) to 0 (horizontal) to -119.5 (up).
		"""

		angles = [pitch, -12, -39, -3, 8] # angles in degrees
		angles = [math.radians(angle) for angle in angles] # convert to radians
		angles.append(1) # also open hand
		times = [1, 1, 1.5, 1.5, 1.5, 1.5]
		self.motion.angleInterpolation("LArm", angles, times, True) # move to those arm angles and open hand

	def colorEyes(self, color, fade_duration = 0.2):
		"""
		Fades eye LEDs to specified color over the given duration.
		"Color" argument should be either in hex format (e.g. 0x0063e6c0) or one of the following
		strings: pink, red, orange, yellow, green, blue, purple
		"""

		if color in self.colors:
			color = self.colors[color]

		self.leds.fadeRGB("FaceLeds", color, fade_duration)

	def getHeadAngles(self):
		"""
		Returns current robot head angles in radians as a list of yaw, pitch.
		For yaw, from the robot's POV, left is positive and right is negative. For pitch, up is positive and down is negative.
		See http://doc.aldebaran.com/2-1/family/robots/joints_robot.html for info on the range of its yaw and pitch.
		"""

		robot_head_yaw, robot_head_pitch = self.motion.getAngles("Head", False)

		# return adjusted robot head angles
		return [robot_head_yaw, -robot_head_pitch]

	def getArmAngles(self):
		"""
		Returns all arm angles in radians as a list in the following order.
		[[LShoulderPitch, LShoulderRoll, LElbowRoll, LWristYaw, LHand],
		[RShoulderPitch, RShoulderRoll, RElbowRoll, RWristYaw, RHand]]
		"""

		return [self.motion.getAngles("LArm", True), self.motion.getAngles("RArm", True)]

	def resetEyes(self):
		"""
		Turns eye LEDs white.
		"""

		self.leds.on("FaceLeds")

	def trackFace(self):
		"""
		Sets face tracker to just head and starts.
		"""

		# start face tracker
		self.track.setWholeBodyOn(False)
		self.track.startTracker()

	def stopTrackingFace(self):
		"""
		Stops face tracker.
		"""

		self.track.stopTracker()

#------------------------Main------------------------#

if __name__ == "__main__":

	print "#----------Audio Script----------#"

	connect("bobby.local")
	obj_name = r.ask_object()
	print obj_name

	broker.shutdown()
	exit(0)
