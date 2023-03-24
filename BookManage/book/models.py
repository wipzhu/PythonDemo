from django.db import models


# Create your models here.
class BookInfo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    pub_date = models.DateField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'book_info'
        verbose_name = '书籍管理'

    def __str__(self):
        return self.name


class PeopleInfo(models.Model):
    GENDER_CHOICE = {
        (1, 'male'),
        (2, 'female')
    }
    name = models.CharField(max_length=255, unique=True)
    gender = models.SmallIntegerField(GENDER_CHOICE, default=1)
    description = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    # 外键：主表数据删除，从表有关联的数据怎么办
    # CASCADE，级联操作
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'people_info'

    def __str__(self):
        return self.name
