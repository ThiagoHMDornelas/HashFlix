import re

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


LISTA_CATEGORIAS = (
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros")
)


# criar filme
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo


def converter_para_embed(url):
    """Converte URLs do YouTube para o formato de embed (usado no player).

    Aceita watch, youtu.be, shorts e embed. URLs que não são do YouTube são
    retornadas sem alteração.

    Ex.: https://www.youtube.com/watch?v=ZFdrlOlFE6Q
         -> https://www.youtube.com/embed/ZFdrlOlFE6Q
    """
    if not url:
        return url
    padrao = r'(?:youtube\.com/(?:watch\?v=|embed/|shorts/|v/)|youtu\.be/)([\w-]{11})'
    match = re.search(padrao, url)
    if match:
        return f'https://www.youtube.com/embed/{match.group(1)}'
    return url


# criar os episodios
class Episodio(models.Model):
    filme = models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def save(self, *args, **kwargs):
        self.video = converter_para_embed(self.video)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filme.titulo + ' - ' + self.titulo


class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")
