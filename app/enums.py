from enum import IntEnum


class NetFlagEnum(IntEnum):
    """
    网络类型标志枚举定义
    Attrs:
        inner:  内网
        public: 公网
    """
    inner = 0
    public = 1


# class IpVerEnum(IntEnum):
#     """
#     系统支持的IP版本，目前仅支持Ipv4协议。
#     Attrs:
#         ipv4:  只支持Ipv4
#         ipv6: 支持Ipv4&Ipv6
#     """
#     ipv4 = 4
#     ipv6 = 6


class UsedEnum(IntEnum):
    """
    是否使用开关枚举
    Attrs:
        no:  没有
        yes: 公网
    """
    no = 0
    yes = 1
