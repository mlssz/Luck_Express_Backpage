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

    account = FixedCharField(max_length=11)
    name = models.CharField(max_length=128, default="无名", null=True)
    signup_time = models.DateField(auto_now=True)
    token = models.CharField(max_length=64, null=True)
    u_type = TinyIntField(default=0, choices=UserTypes, db_column="type")

    class Meta:
        db_table = "user"


# id	用户表外键	int	primary key not null
# position	即时位置	varchar(128)
# score	用户积分	int	not null default 0
class Rental(models.Model):
    """Model about rental user"""

    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="id"
    )
    position = models.CharField(max_length=128, null=True)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = "rental"

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
        db_column="id"
    )
    position = models.CharField(max_length=128, null=True)
    score = models.IntegerField(default=0)
    realname = models.CharField(max_length=128)
    ci = models.CharField(max_length=18, null=True)

    class Meta:
        db_table = "lessee"

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
    )
    lessee = models.ForeignKey(
        Lessee,
        on_delete=models.CASCADE,
        null=True,
        db_column="lessee",
    )

    starttime = models.DateField(auto_now=True)
    endtime = models.DateField(null=True)
    startplace = models.CharField(max_length=32, null=True)
    endplace = models.CharField(max_length=32, null=True)
    fee = models.FloatField(default=0)
    score = models.IntegerField(default=0)
    accepttime = models.DateField(null=True)
    finishtime = models.DateField(null=True)
    remark = models.CharField(max_length=256)
    status = TinyIntField(default=0, choices=OrderStatus)

    class Meta:
        db_table = "orders"

# rental	租车人id	int	foreign key not null
# lessee	承租人id	int foreign key
# startplace	起始地点	varchar(32)
# endplace	结束地点	varchar(32)
# center	中间节点	varchar(256)
# createtime	创建时间	datetime
# remark	备注	varchar(128)
class Line:
    """Model about car lines"""

    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        db_column="rental"
    )
    lessee = models.ForeignKey(
        Lessee,
        on_delete=models.CASCADE,
        null=True,
        db_column="lessee"
    )

    startplace = models.CharField(max_length=32, null=True)
    endplace = models.CharField(max_length=32, null=True)
    center = models.CharField(max_length=256, null=True)

    createtime = models.DateField(null=True)
    remark = models.CharField(max_length=128)

    class Meta:
        db_table = "line"

# lessee	车主id	int	 foreign key not null
# no	车牌号	varchar(18)	 not null
# load	载重	double	default 0
# width	宽	double	default 0
# height	高	double	default 0
# length	长	double	default 0
# type	汽车类型	int	default 0	0待审核1无类型2普通货车3厢式货车4封闭货车5罐式货车6平板货车7集装厢车8自卸货车9特殊结构货车
# modelinfo	其他信息	varchar(256)		可以添加一些其他如车型号
# remark	备注信息	varchar(32)		用户自定义的车名
class Truck(models.Model):
    """Models about trucks"""

    CarTypes = (
        (0, "待审核"),
        (1, "无类型"),
        (2, "普通货车"),
        (3, "厢式货车"),
        (4, "封闭货车"),
        (5, "罐式货车"),
        (6, "平板货车"),
        (7, "集装厢车"),
        (8, "自卸货车"),
        (9, "特殊结构货车"),
    )

    lessee = models.ForeignKey(
        Lessee,
        on_delete=models.CASCADE,
        db_column="lessee"
    )

    no = models.CharField(max_length=18)
    load = models.FloatField(default=0)
    width = models.FloatField(default=0)
    heigth = models.FloatField(default=0)
    length = models.FloatField(default=0)
    ctype = TinyIntField(default=0, db_column="type", choices=CarTypes)
    modelinfo = models.CharField(max_length=256, null=True)
    remark = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = "truck"

# info	广告信息	varchar(128)
# fee	广告费用	double	default 0
# time	导入时间	datetime	default now()
class Advertisement(models.Model):
    """Model about Advertisements"""

    info = models.CharField(max_length=128)
    fee = models.FloatField(default=0)
    time = models.DateField(auto_now=True)

    class Meta:
        db_table = "advertisement"


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
        db_column="offer"
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="customer"
    )
    time = models.DateField(auto_now=True)
    remark = models.CharField(max_length=512)
    score = models.IntegerField(default=-1)

    class Meta:
        db_table = "service"
