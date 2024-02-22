; Auto-generated. Do not edit!


(cl:in-package basic_msg-msg)


;//! \htmlinclude GlobalPlan.msg.html

(cl:defclass <GlobalPlan> (roslisp-msg-protocol:ros-message)
  ((speed
    :reader speed
    :initarg :speed
    :type cl:float
    :initform 0.0)
   (position
    :reader position
    :initarg :position
    :type cl:float
    :initform 0.0))
)

(cl:defclass GlobalPlan (<GlobalPlan>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GlobalPlan>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GlobalPlan)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name basic_msg-msg:<GlobalPlan> is deprecated: use basic_msg-msg:GlobalPlan instead.")))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <GlobalPlan>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader basic_msg-msg:speed-val is deprecated.  Use basic_msg-msg:speed instead.")
  (speed m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <GlobalPlan>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader basic_msg-msg:position-val is deprecated.  Use basic_msg-msg:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GlobalPlan>) ostream)
  "Serializes a message object of type '<GlobalPlan>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'speed))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'position))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GlobalPlan>) istream)
  "Deserializes a message object of type '<GlobalPlan>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'speed) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'position) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GlobalPlan>)))
  "Returns string type for a message object of type '<GlobalPlan>"
  "basic_msg/GlobalPlan")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GlobalPlan)))
  "Returns string type for a message object of type 'GlobalPlan"
  "basic_msg/GlobalPlan")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GlobalPlan>)))
  "Returns md5sum for a message object of type '<GlobalPlan>"
  "787c706e4401319aeae0fad83914b3d0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GlobalPlan)))
  "Returns md5sum for a message object of type 'GlobalPlan"
  "787c706e4401319aeae0fad83914b3d0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GlobalPlan>)))
  "Returns full string definition for message of type '<GlobalPlan>"
  (cl:format cl:nil "float64 speed~%float64 position~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GlobalPlan)))
  "Returns full string definition for message of type 'GlobalPlan"
  (cl:format cl:nil "float64 speed~%float64 position~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GlobalPlan>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GlobalPlan>))
  "Converts a ROS message object to a list"
  (cl:list 'GlobalPlan
    (cl:cons ':speed (speed msg))
    (cl:cons ':position (position msg))
))
