#!/usr/bin/env python
# ROS와 OpenCV를 활용한 자율주행 차선 검출 코드

import rospy
import cv2
import numpy as np
from math import floor
from std_msgs.msg import Float64
from sensor_msgs.msg import CompressedImage

# 각도를 라디안 값으로 변환하는 함수
def degTorad(deg):
    rad_diff = 0.5304  # 추가적인 오프셋 값
    rad = deg * (3.14 / 180)  # 각도를 라디안으로 변환
    return rad + rad_diff

# Bird's eye view(탑다운 뷰)로 이미지를 변환하는 함수
def bird_eye_view_scale(image):

    #src_points = np.float32([[105, 135], [215, 135], [10, 225], [310, 225]])  
    #src_points = np.float32([[55, 135], [265, 135], [10, 225], [310, 225]])  
    #src_points = np.float32([[50, 100], [270, 100], [20, 230], [300, 230]])

    # 원본 이미지에서 관심 영역의 좌표 설정 
    src_points = np.float32([[210, 270], [430, 270], [50, 450], [590, 450]])
    # 변환 후 이미지의 목표 영역 좌표
    dst_points = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])
    
    # Homography 행렬 계산
    homography_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    # Bird's eye view 변환 적용
    bird_eye_image = cv2.warpPerspective(image, homography_matrix, (640, 480))
    return bird_eye_image

# 카메라 이미지 콜백 함수
def callback_camera(image):
    # ROS 퍼블리셔 설정: 모터 속도와 서보 위치
    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)

    # 압축된 이미지 데이터를 numpy 배열로 변환
    np_arr = np.fromstring(image.data, np.uint8)
    # numpy 배열을 OpenCV 이미지로 디코딩
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 이미지를 YCrCb 색공간으로 변환
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

    # YCrCb 채널 분리
    Y, Cr, Cb = cv2.split(ycrcb)
    # 노란색 영역 검출을 위한 Thresholding
    _, Cr_thresh = cv2.threshold(Cr, 135, 255, cv2.THRESH_BINARY)
    _, Cb_thresh = cv2.threshold(Cb, 85, 255, cv2.THRESH_BINARY_INV)
    yellow_thresh = cv2.bitwise_and(Cr_thresh, Cb_thresh)
    
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 흰색 영역 검출을 위한 Thresholding
    _, white_thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    # 노란색과 흰색 영역을 결합
    combine = cv2.bitwise_or(yellow_thresh, white_thresh, mask=None)

    # Bird's eye view 변환 적용
    bird_eye = bird_eye_view_scale(combine)

    # 차량의 이미지 상 중심 x좌표 계산
    car_center_x = bird_eye.shape[1] // 2

    # Bird's eye view 이미지에서 외곽선 검출
    _, contours, _ = cv2.findContours(bird_eye, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 시각화를 위한 빈 이미지 생성
    blank = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    
    # 차선 위치를 찾기 위한 y좌표 설정
    y_lane_pos = 350

    # 차선의 왼쪽과 오른쪽 경계 초기화
    left_lane = 0
    right_lane = bird_eye.shape[1]

    # 오른쪽 차선 경계 탐색
    for i in range(car_center_x, bird_eye.shape[1]):
        if bird_eye[y_lane_pos][i] == 255:
            right_lane = i
            break

    # 왼쪽 차선 경계 탐색
    for i in range(car_center_x, 0, -1):
        if bird_eye[y_lane_pos][i] == 255:
            left_lane = i
            break

    # 차선의 중심 x좌표 계산
    x_center_lane = (right_lane + left_lane) / 2
    # 시각화를 위해 차선 중심과 차량 중심에 원 그리기
    cv2.circle(blank, (int(x_center_lane), y_lane_pos), 3, 255, 3)
    cv2.circle(blank, (car_center_x, y_lane_pos), 3, 255, 3)

    # 차량 중심과 차선 중심 간의 오프셋 계산
    offset = x_center_lane - car_center_x
    # PID 컨트롤러를 사용하여 조향 각도 계산
    steering_output = pid.update(offset)

    # 조향 값을 라디안으로 변환하고 오프셋 추가
    steering_output = degTorad(floor(steering_output))

    # ROS 토픽으로 조향 각도와 속도 퍼블리시
    position_pub.publish(steering_output)
    speed_pub.publish(5000)

    # 시각화를 위해 외곽선을 그리고 결과를 표시
    cv2.drawContours(blank, contours, -1, 255, 1)
    cv2.imshow('contour', blank)
    cv2.imshow('filter', combine)
    cv2.imshow('Bird Eye View', bird_eye)  # Bird's eye view 이미지 출력
    cv2.waitKey(1) 

# 메인 함수
if __name__ == '__main__':
    # PID 컨트롤러 클래스 정의
    class PID:
        def __init__(self, Kp, Ki, Kd, max_output, min_output):
            self.Kp = Kp    # 비례 게인
            self.Ki = Ki    # 적분 게인 (오랜 시간 동안의 오프셋 누적)
            self.Kd = Kd    # 미분 게인 (빠른 변화에 대한 반응)
            self.max_output = max_output  # 출력의 최대값
            self.min_output = min_output  # 출력의 최소값
            self.prev_error = 0           # 이전 에러 값
            self.integral = []            # 에러 누적 값

        def update(self, error):
            self.integral.append(error)
            if len(self.integral) > 100:  # 적분 값의 크기를 제한
                self.integral.pop(0)

            # PID 공식 적용
            derivative = error - self.prev_error
            output = (self.Kp * error) + (self.Ki * sum(self.integral) / len(self.integral)) + (self.Kd * derivative)
            # 출력값을 최소/최대 범위로 제한
            output = max(min(output, self.max_output), self.min_output)
            self.prev_error = error
            return output

    try:
        # ROS 노드 초기화
        rospy.init_node("find_lane")
        # PID 컨트롤러 생성
        global pid
        pid = PID(0.2, 0.0001, 0.2, 30, -30)
        # 카메라 이미지 구독 설정
        camera_sub = rospy.Subscriber("/image_jpeg/compressed", CompressedImage, callback_camera)
        # ROS 루프 실행
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
