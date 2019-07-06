from app.models import *
from rest_framework import serializers


# 分类序列化器
class CateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseType
        fields = '__all__'



# 课程序列化器
class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'




# 章节序列化器
class ChapterSerializer(serializers.ModelSerializer):

    # course=CourseSerializer()

    class Meta:
        model = Chapter
        fields = ('name','id')


# 小节序列化器
class CourseCellSerializer(serializers.ModelSerializer):


    class Meta:
        model = CourseCell
        fields = '__all__'