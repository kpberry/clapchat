import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from math import pi, sqrt

import numpy as np
import pyaudio
from cv2 import VideoCapture, imwrite

FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
CHUNK = 256

# Parameters determined through grid search on about 700 test examples
SIGMA = 0.6
KERNEL_BASE = np.arange(-50, 50, 1)
KERNEL = np.exp(-KERNEL_BASE ** 2 / (2 * SIGMA ** 2)) / sqrt(pi * 2) / SIGMA
KERNEL -= 0.01
THRESHOLD = 1e-4

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

while True:
    cur_chunk = np.abs(np.fromstring(stream.read(CHUNK)))
    convolved = np.convolve(KERNEL, cur_chunk)
    if np.max(convolved) > THRESHOLD:
        vc = VideoCapture(0)

        if vc.isOpened():
            rval, frame = vc.read()
            if rval:
                imwrite('/tmp/.out-clapchat.png', frame)
                vc.release()
                break

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

toaddr = input("Enter recipient email addresses separated by spaces: ").split()
fromaddr = "clapchat.mailer@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ', '.join(toaddr)
msg['Subject'] = "Incoming Clapchat!"

body = u"👏 👏 👏"
msg.attach(MIMEText(body, 'plain'))

filename = "clapchat.png"
attachment = open("/tmp/.out-" + filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= " + filename)
msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "vitrified crwth elk parade")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
