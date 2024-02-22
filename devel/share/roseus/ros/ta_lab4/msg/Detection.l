;; Auto-generated. Do not edit!


(when (boundp 'ta_lab4::Detection)
  (if (not (find-package "TA_LAB4"))
    (make-package "TA_LAB4"))
  (shadow 'Detection (find-package "TA_LAB4")))
(unless (find-package "TA_LAB4::DETECTION")
  (make-package "TA_LAB4::DETECTION"))

(in-package "ROS")
;;//! \htmlinclude Detection.msg.html


(defclass ta_lab4::Detection
  :super ros::object
  :slots (_x _y _w _h _error_center _error_size ))

(defmethod ta_lab4::Detection
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:w __w) 0.0)
    ((:h __h) 0.0)
    ((:error_center __error_center) 0.0)
    ((:error_size __error_size) 0.0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _w (float __w))
   (setq _h (float __h))
   (setq _error_center (float __error_center))
   (setq _error_size (float __error_size))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:w
   (&optional __w)
   (if __w (setq _w __w)) _w)
  (:h
   (&optional __h)
   (if __h (setq _h __h)) _h)
  (:error_center
   (&optional __error_center)
   (if __error_center (setq _error_center __error_center)) _error_center)
  (:error_size
   (&optional __error_size)
   (if __error_size (setq _error_size __error_size)) _error_size)
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _w
    8
    ;; float64 _h
    8
    ;; float64 _error_center
    8
    ;; float64 _error_size
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _w
       (sys::poke _w (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _h
       (sys::poke _h (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _error_center
       (sys::poke _error_center (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _error_size
       (sys::poke _error_size (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _w
     (setq _w (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _h
     (setq _h (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _error_center
     (setq _error_center (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _error_size
     (setq _error_size (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get ta_lab4::Detection :md5sum-) "e34f6a3e4ec965d0bc49da004c6abdbc")
(setf (get ta_lab4::Detection :datatype-) "ta_lab4/Detection")
(setf (get ta_lab4::Detection :definition-)
      "float64 x
float64 y
float64 w
float64 h
float64 error_center
float64 error_size



")



(provide :ta_lab4/Detection "e34f6a3e4ec965d0bc49da004c6abdbc")


