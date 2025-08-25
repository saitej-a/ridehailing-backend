from django.contrib.auth.models import BaseUserManager

class CustomBaseUserManager(BaseUserManager):
    def create_user(self,email,password,**kwargs):
        if not email:
            raise ValueError("Required fields is Missing")
        email=self.normalize_email(email=email)
        user=self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_staff',True)
        return self.create_user(email,password,**kwargs)
    def get_by_natural_key(self, email):
        return self.get(email=email)