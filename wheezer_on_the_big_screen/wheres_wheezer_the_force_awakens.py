import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np
import json
import face_recognition
import math
from unpack_json_ooga_booga import get_refined_loads

refined_loads = get_refined_loads()

def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

known_face_encodings = [
]
known_face_names = [
]

def read_db_encodings_json(filename):
    with open(filename, 'r') as json_file:
        reconstructed_encodings_dict = json.load(json_file)
    for item in reconstructed_encodings_dict:
        reconstructed_encodings_dict[item] = np.asarray(reconstructed_encodings_dict[item])
    return reconstructed_encodings_dict

foo = read_db_encodings_json(r"C:\Users\izack\OneDrive\Documents\GitHub\slohacks20-heroku\data\db_encoding_jsons\20200301-064716.json")

for item in foo:
    known_face_names.append(item)
    known_face_encodings.append(foo[item])



class App:

    def __init__(self, window, window_title, video_source=0):

        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        scrollbar = tkinter.Scrollbar()
        scrollbar.pack(side='right', fill='y')

        Details1 = ""

        self.outputwindow = tkinter.Text(yscrollcommand=scrollbar.set, wrap="word", width=200,
                                    font="{Times new Roman} 9")
        self.outputwindow.pack(side='left', fill='y')
        scrollbar.config(command=self.outputwindow.yview)


        self.outputwindow.yview('end')
        self.outputwindow.config(yscrollcommand=scrollbar.set)
        self.outputwindow.insert('end', Details1)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame, updated_text = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

        self.outputwindow.insert('end', updated_text)
        self.outputwindow.see('end')


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        conf_value = 0
        matched_image = 0
        formatted_id = 0
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            if ret:

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    conf_value = face_distance_to_conf(face_distances[best_match_index])
                    if matches[best_match_index] and face_distance_to_conf(face_distances[best_match_index])>.91:
                        id = known_face_names[best_match_index][11:-4]
                        formatted_id = "MP" + str(id)
                        name = refined_loads[formatted_id]["firstname"] + " " + refined_loads[formatted_id]["lastname"]
                        matched_image = name


                    face_names.append(name)

                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4

                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                        # Draw a label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                # Return a boolean success flag and the current frame converted to BGR

                updated_text = ""
                if formatted_id:
                    updated_text += """
                    Matched Image:        %s \n
                    First Name:           %s \n
                    Last Name:            %s \n
                    Gender:               %s \n
                    Race / Ethnicity:     %s \n
                    Age:                  %s \n
                    Date of Last Contact: %s \n
                    City Last Seen In:    %s \n
                    State Last Seen In:   %s \n
                    NAMUS Case Link:      %s \n
                    """ % (matched_image,
                           refined_loads[formatted_id]["firstname"],
                           refined_loads[formatted_id]["lastname"],
                           refined_loads[formatted_id]["gender"],
                           refined_loads[formatted_id]["raceethnicity"],
                           refined_loads[formatted_id]["currentage"],
                           refined_loads[formatted_id]["dateoflastcontact"],
                           refined_loads[formatted_id]["cityoflastcontact"],
                           refined_loads[formatted_id]["stateoflastcontact"],
                           refined_loads[formatted_id]["link"]
                           )
                if conf_value:
                    updated_text += "confidence-value: %f \n" % conf_value

                if len(updated_text)>0:
                    updated_text += "\n"

                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), updated_text)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")