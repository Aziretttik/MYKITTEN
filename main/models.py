from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()

class Cat(models.Model):
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveIntegerField('Возраст')
    breed = models.CharField('Порода', max_length=100, blank=True)
    color = models.CharField('Окрас', max_length=50)
    description = models.TextField('Описание')
    photo = models.ImageField('Фотография', upload_to='cats/', blank=True, null=True)
    health_status = models.TextField('Состояние здоровья')
    is_adopted = models.BooleanField('Усыновлен', default=False)

    def __str__(self):
        return self.name

class AdoptionRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'На рассмотрении'), ('approved', 'Одобрено'), ('rejected', 'Отказано')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} -> {self.cat.name}"