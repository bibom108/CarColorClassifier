# Car's Color Classifier
Các bước giải quyết bài toán:
1. Nhận diện ô tô có trong hình.
2. Lấy phần hình của ô tô nhận diện được ở bước 1 và nhận diện màu sắc.  
3. Đóng gói kết quả trên giao diện **PYQT5**
  
Chi tiết các bước được trình bày bên dưới.

## Nhận diện ô tô trong hình
Sử dụng **YOLOV5** để nhận diện ô tô có trong hình.  
Vì trong model đã được trained sẵn của **YOLOV5** đã có chứa class _car_, nên
ta chỉ việc sử dụng lại model và áp dụng vào bài toán.  
  
Qua bước này, ta có có tập tọa độ các xe có trong hình để chuyển sang bước 
tiếp theo.

## Nhận diện màu sắc của xe
Trước tiên ta sử dụng thuật toán _k-means_ với hằng số cứng là 10 đối tượng màu
(có nghĩa là 10 màu xuất hiện nhiều nhất trong hình).  
Sau đó ta chọn ra màu xuất hiện nhiều nhất, chuyển tiếp 3 giá trị _RGB_ của nó
sang phần xử lý tiếp theo.  
  
Có được giá trị _RGB_ của một màu, việc tiếp theo ta cần làm là nhận diện được
đó là màu gì. Việc này được thực hiện thông qua việc train một model để nhận
diện một màu sắc từ mã _RGB_ tương ứng.
  
Sau cùng ta vẽ bounding của xe và text màu tương ứng với từng xe.

## Xây dựng giao diện trên PYQT5
Giao diện gồm các thành phần:
- Thay đổi level 2 hoặc 3: có thể chọn level 2 để tự vẽ bounding box kiểm tra
màu sắc.
- Button để upload ảnh.
- Button để Run/ Process/ Save.

## Tham khảo
1. Model nhận diện màu từ mã _RGB_: https://github.com/AjinkyaChavan9/RGB-Color-Classifier-with-Deep-Learning-using-Keras-and-Tensorflow
2. Thư viện **YOLOV5**: https://github.com/ultralytics/yolov5
