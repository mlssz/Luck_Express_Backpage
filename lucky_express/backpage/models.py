from django.db import models
from django.conf import settings

class FixedCharField(models.CharField):
    """FixedCharField use 'char' instead of 'varchar'"""

    def db_type(self, connection):
        return "char({})".format(self.max_length)

class TinyIntField(models.PositiveSmallIntegerField):
    """TinyIntField use 'tinyint' instead of 'smallint'"""

    def db_type(self, connection):
        return "tinyint"

class DateTimeDateField(models.DateTimeField):
    """DateTimeDateField use 'datetime' instead of 'date'"""

    def __init__(self, *arg, **karg):
        super(DateTimeDateField, self).__init__(*arg, **karg)
        self.mysql_now = karg.get("auto_now", False)

    def db_type(self, connection):
        return "datetime"


# id	用户编码	int	primark key auto_increment
# account	用户手机号	char(11)	not null
# name	用户昵称	varchar(128)	default '无名'
# signup_time	用户注册时间	datetime	not null default now()
# token	用户访问令牌	varchar(64)
# type	用户类型	tinyint	not null default 0	0未分组;1租车人;2货车司机;3待审核用户
class User(models.Model):
    """Model about user foundation"""

    UserTypes = (
        (0, "未分组"),
        (1, "租车人"),
        (2, "货车司机"),
        (3, "待审核用户"),
    )

    account = FixedCharField(max_length=11, verbose_name="账号")
    name = models.CharField(max_length=128, default="无名", null=True, verbose_name="名字")
    pre_login_time = DateTimeDateField(auto_now=True, verbose_name="上次登录时间")
    signup_time = DateTimeDateField(auto_now=True, verbose_name="登录时间")
    token = models.CharField(max_length=64, null=True)
    user_type = TinyIntField(default=0, choices=UserTypes, db_column="type", verbose_name="用户类型")

    def __str__(self):
        return "{}-{}".format(self.account, self.name)

    class Meta:
        db_table = "user"
        verbose_name="基础用户"
        verbose_name_plural="基础用户"



# 租车者
# id	用户表外键	int	primary key not null
# position	即时位置	varchar(128)
# score	用户积分	int	not null default 0
class Rental(models.Model):
    """Model about rental user"""

    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="id",
        verbose_name="用户id"
    )
    position_x = models.FloatField(default=0, verbose_name="即时位置 x")
    position_y = models.FloatField(default=0, verbose_name="即时位置 y")
    score = models.IntegerField(default=0, verbose_name="用户积分")

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        db_table = "rental"
        verbose_name="租车者"
        verbose_name_plural="租车者"

# 货车主
# id	用户表外键	int	primary key not null
# position	即时位置	varchar(128)
# score	用户信誉积分	int	not null default 0
# realname	用户真实姓名	varchar(128)	not null
# ci	用户身份证号	varchar(18)
class Lessee(models.Model):
    """Model about lessee user"""

    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="id",
        verbose_name="用户id"
    )
    position_x = models.FloatField(default=0, verbose_name="即时位置 x")
    position_y = models.FloatField(default=0, verbose_name="即时位置 y")
    score = models.IntegerField(default=3, verbose_name="信誉积分")
    order_count = models.IntegerField(default=0, verbose_name="订单完成数")
    password = models.CharField(max_length=256, verbose_name="密码")
    realname = models.CharField(max_length=128, verbose_name="真实姓名")
    ci = models.CharField(max_length=18, null=True, verbose_name="身份证号")

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        db_table = "lessee"
        verbose_name="货车主"
        verbose_name_plural="货车主"

# rental	租车人	int	foreign key not null
# lessee	承租人	int	foreign key
# starttime	订单发起时间	datetime	not null default now()
# endtime	订单结束时间	datetime
# startplace	起点	varchar(32)
# endplace	终点	varchar(32)
# fee	费用	double	default 0
# socre	租车人评分	int	default 0
# accepttime	承租人接单时间	datetime
# finishtime	承租人完成订单时间	datetime
# remark	租车人对订单的评价	varchar(256)
# status	订单状态	tinyint	default 0	0保存订单1预定订单2发起订单3订单被接受4完成订单5订单未完成结束
class Orders(models.Model):
    """Model about order"""

    OrderStatus = (
        (0, "保存订单"),
        (1, "预定订单"),
        (2, "发起订单"),
        (3, "订单被接受"),
        (4, "完成订单"),
        (5, "订单未完成结束"),
    )

    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        db_column="rental",
        verbose_name="租车者id"
    )
    lessee = models.ForeignKey(
        Lessee,
        on_delete=models.CASCADE,
        null=True,
        db_column="lessee",
        verbose_name="货车主id"
    )

    starttime = DateTimeDateField(auto_now=True, verbose_name="发起时间")
    endtime = DateTimeDateField(null=True, verbose_name="结束时间")
    startplace = models.CharField(max_length=32, null=True, verbose_name="起始地点")
    startplacey = models.FloatField(default=0, verbose_name="起始位置 y")
    startplacex = models.FloatField(default=0, verbose_name="起始位置 x")
    endplace = models.CharField(max_length=1024, null=True, verbose_name="终点")
    fee = models.FloatField(default=0, verbose_name="费用")
    score = models.IntegerField(default=0, verbose_name="租车人评分")
    accepttime = DateTimeDateField(null=True, verbose_name="接单时间")
    finishtime = DateTimeDateField(null=True, verbose_name="完成订单时间")
    remark = models.CharField(max_length=256, verbose_name="租车人评价")
    status = TinyIntField(default=0, choices=OrderStatus, verbose_name="订单状态")

    class Meta:
        db_table = "orders"
        verbose_name="订单"
        verbose_name_plural="订单"

# rental	租车人id	int	foreign key not null
# lessee	承租人id	int foreign key
# startplace	起始地点	varchar(32)
# endplace	结束地点	varchar(32)
# center	中间节点	varchar(256)
# createtime	创建时间	datetime
# remark	备注	varchar(128)
class Line(models.Model):
    """Model about car lines"""

    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        db_column="rental",
        verbose_name="租车者id"
    )
    lessee = models.ForeignKey(
        Lessee,
        on_delete=models.CASCADE,
        null=True,
        db_column="lessee",
        verbose_name="货车主id"
    )

    startplace = models.CharField(max_length=32, null=True, verbose_name="起点")
    endplace = models.CharField(max_length=32, null=True, verbose_name="终点")
    center = models.CharField(max_length=256, null=True, verbose_name="中间节点")

    createtime = DateTimeDateField(null=True, verbose_name="创建时间")
    remark = models.CharField(max_length=128, verbose_name="备注")

    class Meta:
        db_table = "line"
        verbose_name="常用路线"
        verbose_name_plural="常用路线"

# lessee	车主id	int	 foreign key not null
# no	车牌号	varchar(18)	 not null
# load	载重	double	default 0
# width	宽	double	default 0
# height	高	double	default 0
# length	长	double	default 0
# type	汽车类型	int	default 0 (0, "小型货车"), (1, "大型货车"), (2, "小型平板"), (3, "中型平板"), (4, "大型平板"),
# morelinfo	其他信息	varchar(256)		可以添加一些其他如车型号
# remark	备注信息	varchar(32)		用户自定义的车名
class Truck(models.Model):
    """Models about trucks"""

    CarTypes = (
        (0, "小型货车"),
        (1, "大型货车"),
        (2, "小型平板"),
        (3, "中型平板"),
        (4, "大型平板"),
    )

    lessee = models.OneToOneField(
        Lessee,
        on_delete=models.CASCADE,
        db_column="lessee",
        verbose_name="货车主id"
    )

    no = models.CharField(max_length=18, verbose_name="车牌号")
    loads = models.FloatField(default=0, verbose_name="载重")
    width = models.FloatField(default=0, verbose_name="宽")
    heigth = models.FloatField(default=0, verbose_name="高")
    length = models.FloatField(default=0, verbose_name="长")
    car_type = TinyIntField(default=0, db_column="type", choices=CarTypes, verbose_name="车辆类型")
    moreinfo = models.CharField(max_length=256, null=True, verbose_name="其他信息")
    remark = models.CharField(max_length=32, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "truck"
        verbose_name="车辆"
        verbose_name_plural="车辆"

# info	广告信息	varchar(128)
# fee	广告费用	double	default 0
# time	导入时间	datetime	default now()
class Advertisement(models.Model):
    """Model about Advertisements"""

    info = models.CharField(max_length=128, verbose_name="广告信息")
    fee = models.FloatField(default=0, verbose_name="广告费用")
    time = DateTimeDateField(auto_now=True, verbose_name="导入时间")
    class Meta:
        db_table = "advertisement"
        verbose_name="广告"
        verbose_name_plural="广告"


# offer	服务人员id	int	foreign key not null
# customer	客户id	int	foreign key not null
# time	服务时间	datatime	default now()
# remark	备注	varchar(512)
# score	评分	int	default -1
class Service(models.Model):
    """Model about services"""

    offer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="offer",
        verbose_name="服务员id"
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="customer",
        verbose_name="客户id"
    )
    time = DateTimeDateField(auto_now=True, verbose_name="服务时间")
    remark = models.CharField(max_length=512, verbose_name="备注")
    score = models.IntegerField(default=-1, verbose_name="评分")

    class Meta:
        db_table = "service"
        verbose_name="服务信息"
        verbose_name_plural="服务信息"
