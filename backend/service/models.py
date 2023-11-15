from django.db import models

class UserManager():
    def create_user(self, id, **kwargs):
        if not id:
            raise ValueError("ID is required")

        user = self.model(
            id = id,
            **kwargs
        )

        user.save(using = self._db)
        return user
    def create_superuser(self, id, **kwargs):
        superuser = self.create_user(
            id = id
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using = self._db)
        return superuser
#hello my name is grace kim, i am 바보에요
# nice to meet ya
# gutentag
# did you see the match of bayern munich?
class User(models.Model):
    id = models.IntegerField(primary_key= True)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default = False)
    joined_date =models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'id'
    
    class Meta:
        db_table="user"

class VODInfo(models.Model):
    vod_id = models.IntegerField(unique=True)  # VOD ID 또는 비디오 고유 식별자 (고유값)
    title = models.CharField(max_length=200)  # 작품명
    category = models.CharField(max_length=50)  # VOD 분류
    viewers = models.IntegerField()  # 시청자수
    total_watch_time = models.IntegerField()  # 총 시청시간 (분)
    class Meta:
        db_table="vodinfo"


class UserLog(models.Model):
    subsr = models.IntegerField()
    use_tms = models.IntegerField(default=0)  # 누적 시청시간 (기본값 0)
    vod_id = models.ForeignKey(VODInfo, on_delete=models.CASCADE)  # 'VODInfo' 모델과 연결 # VOD ID 또는 비디오 고유 식별자
    class Meta:
        db_table='userlog'