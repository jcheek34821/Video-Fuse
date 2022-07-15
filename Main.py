# Importing all necessary libraries from multiprocessing.connection import Listener
import cv2
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from datetime import datetime

destination_string = ""


def time_to_seconds(hr, mn, sc):
    return sc + (mn * 60) + (60 * 60 * hr)


def seconds_to_time(sc):
    hr = int(sc / (60 * 60))
    mn = int((sc - (hr * 60 * 60)) / 60)
    sec = sc - ((hr * 60 * 60) + (mn * 60))
    return str(hr) + ":" + str(mn) + ":" + str(sec)


def save_video():
    now = datetime.now()
    start_hour = int(now.strftime("%H"))
    start_min = int(now.strftime("%M"))
    start_sec = int(now.strftime("%S"))
    print("Saving video...")

    videos_in_dir = os.listdir(destination_label["text"])

    mp4string = "new_video.mp4"

    # frame
    currentframe = 0
    width = 1920
    height = 1080

    # choose codec according to format needed
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(destination_string + "/" + mp4string, fourcc, 30, (width, height))

    for x in videos_in_dir:
        # Read the video from specified path
        cam = cv2.VideoCapture(destination_label["text"] + "/" + x)

        path_count = 1

        while os.path.exists(destination_string + "/" + mp4string):
            mp4string = "new_video(" + str(path_count) + ").mp4"
            path_count += 1

        while True:
            # reading from frame
            ret, frame = cam.read()
            if ret:
                # writing the extracted images
                video.write(frame)

                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1
            else:
                break

    video.release()
    print("Video saved")
    now = datetime.now()
    end_hour = int(now.strftime("%H"))
    end_min = int(now.strftime("%M"))
    end_sec = int(now.strftime("%S"))
    print(seconds_to_time(time_to_seconds(end_hour, end_min, end_sec) - time_to_seconds(start_hour, start_min, start_sec)))


def choose_directory():
    global destination_string
    destination_string = fd.askdirectory(
        title='Select Destination')
    if destination_string != "":
        destination_label["text"] = destination_string


# create the root window
root = tk.Tk()
root.title('Video Fuse')
root.resizable(False, False)
root.geometry('1000x300')

# space label
space_label = ttk.Label(
    root,
    text="")
space_label.pack()

# space label
space_label = ttk.Label(
    root,
    text="")
space_label.pack()

# select destination label
destination_label = ttk.Label(
    root,
    text="Choose Directory")
destination_label.pack()

# choose directory button
choose_directory_button = ttk.Button(
    root,
    text='Open',
    command=choose_directory
)
choose_directory_button.pack(expand=True)

# space label
space_label = ttk.Label(
    root,
    text="")
space_label.pack()

# go button
go_button = ttk.Button(
    root,
    text='Go',
    command=save_video
)
go_button.pack(expand=True)

# run the application
root.mainloop()

# Release all space and windows once done
cv2.destroyAllWindows()
