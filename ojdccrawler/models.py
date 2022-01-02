from django.db import models

# Create your models here.


class QueryRecord(models.Model):
    query = models.CharField(max_length=20, help_text='日文單字詞搜尋紀錄')
    time = models.DateTimeField(auto_now_add=True, help_text='查詢日期')

    def __str__(self):
        return f'[{self.time}] {self.query}'
