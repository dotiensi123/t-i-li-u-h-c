# Main.py

import cv2
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication
from Main import drawRedRectangleAroundPlate, writeLicensePlateCharsOnImage
from giaodien import LicensePlateRecognition
import DetectChars
import DetectPlates
import PossiblePlate

# module level variables ##########################################################################
# biến cấp mô-đun
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False
imgOriginalScene=""
namelink=""
global hu
# licPlate.strChars=""
tinh_thanh = {
    "01": "Hà Nội",
    "02": "Hà Giang",
    "03": "Cao Bằng",
    "04": "Lạng Sơn",
    "05": "Tuyên Quang",
    "06": "Thái Nguyên",
    "07": "Yên Bái",
    "08": "Lào Cai",
    "09": "Điện Biên",
    "10": "Lai Châu",
    "11": "Sơn La",
    "12": "Hòa Bình",
    "14": "Hải Phòng",
    "15": "Quảng Ninh",
    "16": "Ninh Bình",
    "17": "Thanh Hóa",
    "18": "Nghệ An",
    "19": "Hà Tĩnh",
    "20": "Quảng Bình",
    "21": "Quảng Trị",
    "22": "Thừa Thiên Huế",
    "23": "Đà Nẵng",
    "24": "Quảng Nam",
    "25": "Quảng Ngãi",
    "26": "Bình Định",
    "27": "Phú Yên",
    "28": "Khánh Hòa",
    "29": "Ninh Thuận",
    "30": "Bình Thuận",
    "31": "Kon Tum",
    "32": "Gia Lai",
    "33": "Đắk Lắk",
    "34": "Đắk Nông",
    "35": "Lâm Đồng",
    "36": "Bình Phước",
    "37": "Tây Ninh",
    "38": "Bình Dương",
    "39": "Đồng Nai",
    "40": "Bà Rịa - Vũng Tàu",
    "41": "Hồ Chí Minh",
    "42": "Long An",
    "43": "Tiền Giang",
    "44": "Bến Tre",
    "45": "Trà Vinh",
    "46": "Vĩnh Long",
    "47": "Đồng Tháp",
    "48": "An Giang",
    "49": "Kiên Giang",
    "50": "Cần Thơ",
    "51": "Hậu Giang",
    "52": "Sóc Trăng",
    "53": "Bạc Liêu",
    "64": "Cà Mau"
}

###################################################################################################

class LicensePlateRecognition(QWidget):
    def __init__(self):
        super().__init__()
        
        self.biensoxe=""
        # Tạo các thành phần giao diện
        self.label = QLabel("Chọn ảnh để nhận diện biển số:", self)
        self.label.setAlignment(Qt.Qt.AlignCenter)

        self.button = QPushButton("Chọn ảnh", self)
        self.button.setCursor(Qt.Qt.PointingHandCursor)
        self.button.clicked.connect(self.open_file_dialog)

        # Bố trí các thành phần giao diện
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.button)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)
        if file_name:
            
            print("Đã chọn ảnh:", file_name)
            # print(namelink)
            self.button.setEnabled(False)
            self.button.setCursor(Qt.Qt.ArrowCursor)
            # imgOriginalScene=namelink
            namelink="/".join(file_name.split("/")[5:])
            # namelink=namelink
            print(namelink)
           
            blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training      # cố gắng đào tạo KNN

            if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful        # nếu đào tạo KNN không thành công
                print("\nerror: KNN traning was not successful\n")  # show error message        # hiển thị thông báo lỗi
                return                                                          # and exit program      # và thoát khỏi chương trình
    # end if

            imgOriginalScene  = cv2.imread(namelink) 
    # print(imgOriginalScene)
    # open image

            if imgOriginalScene is None:                            # if image was not read successfully        # nếu hình ảnh không được đọc thành công
                print("\nerror: image not read from file \n\n")  # print error message to std out       # in thông báo lỗi ra thiết bị xuất chuẩn
                os.system("pause")                                  # pause so user can see error message       # tạm dừng để người dùng có thể thấy thông báo lỗi
                return                                              # and exit program      # và thoát khỏi chương trình
    # end if

            listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)          # phát hiện tấm

            listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # phát hiện ký tự trong tấm

            cv2.imshow("imgOriginalScene", imgOriginalScene)            # show scene image      # hiển thị hình ảnh cảnh

            if len(listOfPossiblePlates) == 0:                          # nếu không có tấm nào được tìm thấy
                print("\nno license plates were detected\n")  # thông báo cho người dùng không tìm thấy tấm nào
            else:                                                       # else
                # if we get in here list of possible plates has at leat one plate       # nếu chúng tôi vào đây, danh sách các tấm có thể có ít nhất một tấm

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)      # sắp xếp danh sách các biển số có thể theo thứ tự GIẢM MỨC (số ký tự nhiều nhất đến số ký tự ít nhất)
                listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate        # giả sử đĩa có nhiều ký tự được nhận dạng nhất (bảng đầu tiên được sắp xếp theo thứ tự giảm dần độ dài chuỗi) là đĩa thực tế
                licPlate = listOfPossiblePlates[0]

                cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate         # hiển thị phần cắt của tấm và ngưỡng của tấm
                cv2.imshow("imgThresh", licPlate.imgThresh)

                if len(licPlate.strChars) == 0:                     # if no chars were found in the plate       # nếu không tìm thấy ký tự nào trong tấm
                    print("\nno characters were detected\n\n")  # show message      # hiện thị thông điệp
                    return                                          # and exit program      # và thoát chương trình
        # end if

                drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # draw red rectangle around plate       # vẽ hình chữ nhật màu đỏ quanh đĩa

                print("\nlicense plate read from image = " + licPlate.strChars + "\n") 
                
                print(licPlate.strChars)
               
                global hu 
                hu=licPlate.strChars
                # write license plate text to std out       # ghi văn bản biển số vào thiết bị xuất chuẩn
                print("----------------------------------------")
                
                writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           # write license plate text on the image         # ghi chữ biển số lên ảnh

                cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image       # hiển thị lại hình ảnh cảnh

                cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           # write image out to file       # ghi ảnh ra file

    # end if else

            cv2.waitKey(0)					# hold windows open until user presses a key        # giữ cửa sổ mở cho đến khi người dùng nhấn phím
         
        mavung=hu[:2]
        tentinh=tinh_thanh.get(mavung)
        print(hu+ " là biển số của tỉnh "+ tentinh)   
        return
    def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    
        p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect        # lấy 4 đỉnh của hình chữ nhật xoay

        cv2.line(imgOriginalScene, tuple(int(x) for x in p2fRectPoints[0]), tuple(int(x) for x in p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines      # vẽ 4 đường màu đỏ
        cv2.line(imgOriginalScene, tuple(int(x) for x in p2fRectPoints[1]), tuple(int(x) for x in p2fRectPoints[2]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(int(x) for x in p2fRectPoints[2]), tuple(int(x) for x in p2fRectPoints[3]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(int(x) for x in p2fRectPoints[3]), tuple(int(x) for x in p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################
    def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
        ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to       # đây sẽ là trung tâm của khu vực mà văn bản sẽ được ghi vào
        ptCenterOfTextAreaY = 0

        ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to         # đây sẽ là phía dưới bên trái của khu vực mà văn bản sẽ được ghi vào
        ptLowerLeftTextOriginY = 0

        sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
        plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

        intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font          # chọn phông chữ jane đơn giản
        fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area       # tỷ lệ phông chữ cơ sở trên chiều cao của khu vực tấm
        intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale         # độ dày phông chữ cơ sở trên tỷ lệ phông chữ

        textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle       # giải nén đã xoay rect thành tâm điểm, chiều rộng và chiều cao và góc
        ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

        intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer        # đảm bảo tâm là một số nguyên
        intPlateCenterY = int(intPlateCenterY)

        ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate      # vị trí ngang của vùng văn bản giống như tấm

        if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image         # nếu biển số xe nằm ở 3/4 phía trên của ảnh
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate         # write the chars in below the plate
        else:                                                                                       # else if the license plate is in the lower 1/4 of the image        # khác nếu biển số xe nằm ở 1/4 phía dưới của hình ảnh
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate         # viết các ký tự ở phía trên tấm
    # end if

        textSizeWidth, textSizeHeight = textSize                # unpack text size width and height     # giải nén kích thước văn bản chiều rộng và chiều cao

        ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area        # tính điểm gốc phía dưới bên trái của vùng văn bản
        ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height        # dựa trên tâm, chiều rộng và chiều cao của vùng văn bản

            # write the text on the image       # viết văn bản trên hình ảnh
        cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
        
# end function
if __name__ == "__main__":
   
    app = QApplication(sys.argv)
    window = LicensePlateRecognition()
    window.show()
    # print(window.biensoxe +"manh dep trai")
    # print(window.biensoxe1 +"manh dep trai")
    # main()
    # print(hu)
    sys.exit(app.exec_())
    
    





