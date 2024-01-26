from django.db import models


class DefaultModel(models.Model):
    """Абстракная модель для всех моделей проекта."""

    name = models.CharField(max_length=128, verbose_name="название")

    class Meta:
        abstract = True
        ordering = ("id",)

    def __str__(self):
        return self.name
