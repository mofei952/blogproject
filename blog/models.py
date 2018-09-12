from django.db import models


class TimeStampModel(models.Model):
    """
    abstract base class, 提供创建时间和修改时间两个通用的field
    """
    create_at = models.DateTimeField(u'生成时间', auto_now_add=True)
    update_at = models.DateTimeField(u'修改时间', auto_now=True)

    class Meta:
        abstract = True


class ProfilePicture(TimeStampModel):
    image = models.ImageField(default='img/default_profile_picture.jpg')
    is_system = models.BooleanField()


class User(TimeStampModel):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, '男'),
        (FEMALE, '女'),
    )
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default=MALE)
    profile_picture = models.ForeignKey(ProfilePicture, on_delete=models.SET_NULL, null=True, default=None)

    # follow_users = models.ManyToManyField('self', through='Follow')

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class Article(TimeStampModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(TimeStampModel):
    content = models.TextField()
    user = models.ForeignKey(User, models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Follow(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_user')
    follow_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_user')
