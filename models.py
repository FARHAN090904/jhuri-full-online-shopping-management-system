from django.db import models


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'
        managed = False  # Table already exists in XAMPP


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, db_column='role_id')
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Required by DRF's IsAuthenticated permission check
    is_authenticated = True          # ← plain class attribute, NOT a property
    is_anonymous = False

    class Meta:
        db_table = 'users'
        managed = False

    @property
    def pk(self):
        return self.user_id

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='addresses')
    label = models.CharField(max_length=50, default='Home')
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, default='Bangladesh')
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'
        managed = False
