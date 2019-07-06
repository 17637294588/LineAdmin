from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modify_time =  models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        abstract = True


# 课程分类
class CourseType(BaseModel):

    name = models.CharField(max_length=20,verbose_name='课程分类')


    class Meta:
        db_table = 'coursetype'
      
        verbose_name_plural = '分类表'

    def __str__(self):
        return self.name



# 课程表
class Course(BaseModel):

    name = models.CharField(max_length=20,verbose_name='课程名称')
    coursetype = models.ForeignKey(CourseType,on_delete=models.CASCADE,verbose_name='分类')
    image = models.ImageField(verbose_name='图片')
    discrib = models.CharField(max_length=20,verbose_name='课程描述')
    price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='价钱')
    watched = models.IntegerField(verbose_name='观看人数',default=0)
    learned = models.IntegerField(verbose_name='收藏人数',default=0)
    is_pay = models.IntegerField(verbose_name='是否付费')
    score = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='热度值',default=0)

    class Meta:
        ordering = ('score',)
        verbose_name_plural = '课程表'

    def __str__(self):
        return self.name


# 课程章节表
class Chapter(BaseModel):

    order_id = models.IntegerField(verbose_name='章节ID')
    name = models.CharField(max_length=20,verbose_name='章节名')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='所属课程')

    class Meta:
        db_table = 'chapter'
        
        verbose_name_plural = '课程章节表'

    def __str__(self):
        return self.name


# 每章节小节
class CourseCell(BaseModel):

    order_id = models.IntegerField(verbose_name='小节ID')
    name = models.CharField(max_length=20,verbose_name='小节名称')
    detail_url = models.SlugField(verbose_name='内容地址')
    content_choices = (
        (1,'直博'),
        (2,'录播'),
        (3,'作业'),
        (4,'在线联系'),
    )
    choices = models.IntegerField(verbose_name='小节分类')
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,verbose_name='关联章节')

    class Meta:
        db_table = 'coursecell'
      
        verbose_name_plural = '章节小节表'

    def __str__(self):
        return self.name





