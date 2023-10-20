from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.authorUser.username

class Ad(models.Model):
    adAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    adTitle = models.CharField(max_length=255)
    adText = models.TextField()
    adFile = models.FileField(upload_to='files/')
    TANKS = 'TS'
    HILLS = 'HS'
    DD = 'DD'
    SELLER = 'SR'
    GILDMASTER = 'GM'
    QUESTGIVER = 'QG'
    BLACKSMITH = 'BS'
    TANNER = 'TR'
    POTION = 'PN'
    SPELLMASTER = 'SM'
    CHOICES = [
        (TANKS, 'Танки'),
        (HILLS, 'Хилы'),
        (DD, 'ДД'),
        (SELLER, 'Торговцы'),
        (GILDMASTER, 'Гилдмастер'),
        (QUESTGIVER, 'Квестгиверы'),
        (BLACKSMITH, 'Кузнецы'),
        (TANNER, 'Кожевники'),
        (POTION, 'Зельевары'),
        (SPELLMASTER, 'Мастера заклинаний')
    ]
    adCategory = models.CharField(max_length=2, choices=CHOICES, default=TANKS)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.adTitle}'

    def get_absolute_url(self):
        return f'/notices/{self.id}'



class Reply(models.Model):
    replyText = models.TextField()
    replyAd = models.ForeignKey(Ad, on_delete=models.CASCADE)
    replyAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)


