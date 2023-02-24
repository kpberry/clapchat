import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy as np
import pyaudio
from cv2 import VideoCapture, imwrite


FORMAT = pyaudio.paFloat32
CHANNELS = 2
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
WINDOW_SIZE = 128
THRESHOLD = 0.15


def has_clap(data: np.ndarray, window_size: int, threshold: float):
    sums = np.cumsum(np.abs(data))
    moving_averages = (sums[window_size:] - sums[:-window_size]) / window_size
    return np.any(moving_averages > threshold)


audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE
)

while True:
    cur_chunk = np.frombuffer(stream.read(CHUNK_SIZE), dtype='float32')
    if has_clap(cur_chunk, WINDOW_SIZE, THRESHOLD):
        vc = VideoCapture(0)

        if vc.isOpened():
            rval, frame = vc.read()
            if rval:
                imwrite('/tmp/.out-clapchat.png', frame)
                vc.release()
                break

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
