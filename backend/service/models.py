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
    # db_table = 'user'
    class Meta:
        db_table="user"