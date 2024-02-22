// Auto-generated. Do not edit!

// (in-package ta_lab4.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Detection {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x = null;
      this.y = null;
      this.w = null;
      this.h = null;
      this.error_center = null;
      this.error_size = null;
    }
    else {
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = 0.0;
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = 0.0;
      }
      if (initObj.hasOwnProperty('w')) {
        this.w = initObj.w
      }
      else {
        this.w = 0.0;
      }
      if (initObj.hasOwnProperty('h')) {
        this.h = initObj.h
      }
      else {
        this.h = 0.0;
      }
      if (initObj.hasOwnProperty('error_center')) {
        this.error_center = initObj.error_center
      }
      else {
        this.error_center = 0.0;
      }
      if (initObj.hasOwnProperty('error_size')) {
        this.error_size = initObj.error_size
      }
      else {
        this.error_size = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Detection
    // Serialize message field [x]
    bufferOffset = _serializer.float64(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.float64(obj.y, buffer, bufferOffset);
    // Serialize message field [w]
    bufferOffset = _serializer.float64(obj.w, buffer, bufferOffset);
    // Serialize message field [h]
    bufferOffset = _serializer.float64(obj.h, buffer, bufferOffset);
    // Serialize message field [error_center]
    bufferOffset = _serializer.float64(obj.error_center, buffer, bufferOffset);
    // Serialize message field [error_size]
    bufferOffset = _serializer.float64(obj.error_size, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Detection
    let len;
    let data = new Detection(null);
    // Deserialize message field [x]
    data.x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [w]
    data.w = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [h]
    data.h = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [error_center]
    data.error_center = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [error_size]
    data.error_size = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 48;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ta_lab4/Detection';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e34f6a3e4ec965d0bc49da004c6abdbc';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 x
    float64 y
    float64 w
    float64 h
    float64 error_center
    float64 error_size
    
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Detection(null);
    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = 0.0
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = 0.0
    }

    if (msg.w !== undefined) {
      resolved.w = msg.w;
    }
    else {
      resolved.w = 0.0
    }

    if (msg.h !== undefined) {
      resolved.h = msg.h;
    }
    else {
      resolved.h = 0.0
    }

    if (msg.error_center !== undefined) {
      resolved.error_center = msg.error_center;
    }
    else {
      resolved.error_center = 0.0
    }

    if (msg.error_size !== undefined) {
      resolved.error_size = msg.error_size;
    }
    else {
      resolved.error_size = 0.0
    }

    return resolved;
    }
};

module.exports = Detection;
