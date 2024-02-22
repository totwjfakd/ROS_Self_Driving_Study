
(cl:in-package :asdf)

(defsystem "basic_msg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "GlobalPlan" :depends-on ("_package_GlobalPlan"))
    (:file "_package_GlobalPlan" :depends-on ("_package"))
  ))