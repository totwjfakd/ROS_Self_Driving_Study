;; Auto-generated. Do not edit!


(when (boundp 'basic_msg::GlobalPlan)
  (if (not (find-package "BASIC_MSG"))
    (make-package "BASIC_MSG"))
  (shadow 'GlobalPlan (find-package "BASIC_MSG")))
(unless (find-package "BASIC_MSG::GLOBALPLAN")
  (make-package "BASIC_MSG::GLOBALPLAN"))

(in-package "ROS")
;;//! \htmlinclude GlobalPlan.msg.html


(defclass basic_msg::GlobalPlan
  :super ros::object
  :slots (_speed _position ))

(defmethod basic_msg::GlobalPlan
  (:init
   (&key
    ((:speed __speed) 0.0)
    ((:position __position) 0.0)
    )
   (send-super :init)
   (setq _speed (float __speed))
   (setq _position (float __position))
   self)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:serialization-length
   ()
   (+
    ;; float64 _speed
    8
    ;; float64 _position
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _position
       (sys::poke _position (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _speed
     (setq _speed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _position
     (setq _position (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get basic_msg::GlobalPlan :md5sum-) "787c706e4401319aeae0fad83914b3d0")
(setf (get basic_msg::GlobalPlan :datatype-) "basic_msg/GlobalPlan")
(setf (get basic_msg::GlobalPlan :definition-)
      "float64 speed
float64 position
")



(provide :basic_msg/GlobalPlan "787c706e4401319aeae0fad83914b3d0")


