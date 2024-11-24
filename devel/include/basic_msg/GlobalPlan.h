// Generated by gencpp from file basic_msg/GlobalPlan.msg
// DO NOT EDIT!


#ifndef BASIC_MSG_MESSAGE_GLOBALPLAN_H
#define BASIC_MSG_MESSAGE_GLOBALPLAN_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace basic_msg
{
template <class ContainerAllocator>
struct GlobalPlan_
{
  typedef GlobalPlan_<ContainerAllocator> Type;

  GlobalPlan_()
    : speed(0.0)
    , position(0.0)  {
    }
  GlobalPlan_(const ContainerAllocator& _alloc)
    : speed(0.0)
    , position(0.0)  {
  (void)_alloc;
    }



   typedef double _speed_type;
  _speed_type speed;

   typedef double _position_type;
  _position_type position;





  typedef boost::shared_ptr< ::basic_msg::GlobalPlan_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::basic_msg::GlobalPlan_<ContainerAllocator> const> ConstPtr;

}; // struct GlobalPlan_

typedef ::basic_msg::GlobalPlan_<std::allocator<void> > GlobalPlan;

typedef boost::shared_ptr< ::basic_msg::GlobalPlan > GlobalPlanPtr;
typedef boost::shared_ptr< ::basic_msg::GlobalPlan const> GlobalPlanConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::basic_msg::GlobalPlan_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::basic_msg::GlobalPlan_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::basic_msg::GlobalPlan_<ContainerAllocator1> & lhs, const ::basic_msg::GlobalPlan_<ContainerAllocator2> & rhs)
{
  return lhs.speed == rhs.speed &&
    lhs.position == rhs.position;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::basic_msg::GlobalPlan_<ContainerAllocator1> & lhs, const ::basic_msg::GlobalPlan_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace basic_msg

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::basic_msg::GlobalPlan_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::basic_msg::GlobalPlan_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::basic_msg::GlobalPlan_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::basic_msg::GlobalPlan_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::basic_msg::GlobalPlan_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::basic_msg::GlobalPlan_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::basic_msg::GlobalPlan_<ContainerAllocator> >
{
  static const char* value()
  {
    return "787c706e4401319aeae0fad83914b3d0";
  }

  static const char* value(const ::basic_msg::GlobalPlan_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x787c706e4401319aULL;
  static const uint64_t static_value2 = 0xeae0fad83914b3d0ULL;
};

template<class ContainerAllocator>
struct DataType< ::basic_msg::GlobalPlan_<ContainerAllocator> >
{
  static const char* value()
  {
    return "basic_msg/GlobalPlan";
  }

  static const char* value(const ::basic_msg::GlobalPlan_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::basic_msg::GlobalPlan_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 speed\n"
"float64 position\n"
;
  }

  static const char* value(const ::basic_msg::GlobalPlan_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::basic_msg::GlobalPlan_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.speed);
      stream.next(m.position);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GlobalPlan_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::basic_msg::GlobalPlan_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::basic_msg::GlobalPlan_<ContainerAllocator>& v)
  {
    s << indent << "speed: ";
    Printer<double>::stream(s, indent + "  ", v.speed);
    s << indent << "position: ";
    Printer<double>::stream(s, indent + "  ", v.position);
  }
};

} // namespace message_operations
} // namespace ros

#endif // BASIC_MSG_MESSAGE_GLOBALPLAN_H
