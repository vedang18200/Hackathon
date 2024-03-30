from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import time
from my_functions import *  # Import your functions from my_functions.py
import cv2

def rec(request):
    return render(request,'index1.html')
def login(request):
    return render(request,'login.html')
def auth(request):

    user_name = request.GET['username']
    password = request.GET['password']
    if user_name == "Admin" and password == "admin":
        return render(request, 'index1.html')  # Replace 'base.html' with 'index.html' if needed
    else:
            return HttpResponse("Invalid Username and password, try again.")

# def face(request):
#     return render(request,'deepfake.html')
def base(request):
    return render(request, 'base1.html')
def helmet(request):
    return render(request,'Helmet.html')
def accident(request):
    return render (request,'accident.html')

def process_video(request):
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']

            # Save the uploaded video file to a temporary location
        with open('uploaded_video.mp4', 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

        source = 'uploaded_video.mp4'  # Use the uploaded video file as the source


        save_video = True # want to save video? (when video as source)
        show_video=True # set true when using video file
        save_img=False  # set true when using only image file to save the image
        # when using image as input, lower the threshold value of image classification

        #saveing video as output
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, frame_size)

        cap = cv2.VideoCapture(source)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.resize(frame, frame_size)  # resizing image
                orifinal_frame = frame.copy()
                frame, results = object_detection(frame) 

                rider_list = []
                head_list = []
                number_list = []

                for result in results:
                    x1,y1,x2,y2,cnf, clas = result
                    if clas == 0:
                        rider_list.append(result)
                    elif clas == 1:
                        head_list.append(result)
                    elif clas == 2:
                        number_list.append(result)

                for rdr in rider_list:
                    time_stamp = str(time.time())
                    x1r, y1r, x2r, y2r, cnfr, clasr = rdr
                    for hd in head_list:
                        x1h, y1h, x2h, y2h, cnfh, clash = hd
                        if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): 
                            try:
                                head_img = orifinal_frame[y1h:y2h, x1h:x2h]
                                helmet_present = img_classify(head_img)
                            except:
                                helmet_present[0] = None

                            if  helmet_present[0] == True: # if helmet present
                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
                                frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                            elif helmet_present[0] == None: # Poor prediction
                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                                frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                            elif helmet_present[0] == False: # if helmet absent 
                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                                frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                                try:
                                    cv2.imwrite(f'riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
                                except:
                                    print('could not save rider')

                                for num in number_list:
                                    x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                                    if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
                                        try:
                                            num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                                            cv2.imwrite(f'number_plates/{time_stamp}_{conf_num}.jpg', num_img)
                                        except:
                                            print('could not save number plate')
                                            
                if save_video: # save video
                    out.write(frame)
                if save_img: #save img
                    cv2.imwrite('saved_frame.jpg', frame)
                if show_video: # show video
                    frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
                    cv2.imshow('Frame', frame)


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
        print('Execution completed')
        return render(request,'output.html')
    else:
         return HttpResponse('Please upload a video file.')
#==================================================================================================================================
    
def crash(request):
    
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']

        # Save the uploaded video file to a temporary location
        with open('accident_video.mp4', 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        import cv2
        import pandas as pd
        from ultralytics import YOLO
        import cvzone
        import pygame
        from plyer import notification

        model = YOLO('best.pt')

        pygame.init()
        alarm_sound = pygame.mixer.Sound('alarm_sound.mp3')


        def RGB(event, x, y, flags, param):
            if event == cv2.EVENT_MOUSEMOVE:
                point = [x, y]
                print(point)


        def play_alarm_sound():
            # Play an alarm sound when an accident is detected
            alarm_sound.play()


        def send_notification(message):
            # Send a notification when an accident is detected
            notification.notify(
                title='Accident Detected!',
                message=message,
                app_icon=None,
                timeout=10
            )


        cv2.namedWindow('RGB')
        cv2.setMouseCallback('RGB', RGB)

        cap = cv2.VideoCapture('accident_video.mp4')

        my_file = open("coco1.txt", "r")
        data = my_file.read()
        class_list = data.split("\n")

        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            count += 1
            if count % 3 != 0:
                continue

            frame = cv2.resize(frame, (1020, 500))
            results = model.predict(frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")

            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)

                if c == 'Accident':
                    play_alarm_sound()
                    print('Accident Detected!')
                    send_notification("An accident has been detected!")

            cv2.imshow("RGB", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        print('Execution completed')
        return render(request,'output.html')
    else:
        return HttpResponse('Please upload a video file.')
