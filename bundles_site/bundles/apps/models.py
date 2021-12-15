from django.db import models

class Folders(models.Model):
    name_folder = models.CharField("Название папки", max_length=255, unique=True)

class Apps(models.Model):
    app_name = models.CharField("Название приложения", max_length=255)
    start_time = models.CharField("Дата/время добавления", max_length=50, default="None")
    folder = models.ForeignKey(Folders, on_delete = models.CASCADE)
    last_time = models.CharField("Последнее обновление", max_length=50)
    status = models.CharField("Статус", max_length=255, default="Не опубликовано")
    next_check = models.CharField("Следующее обновление", max_length=50, default="None")