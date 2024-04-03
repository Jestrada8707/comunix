from django import forms
from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalManyToManyField

from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin


class BlogPost(RoutablePageMixin, Page):
    """Modelo para la pagina de los proyectos"""

    template = "projects/project_page.html"
    max_count = 18

    titulo_proyecto = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        help_text='Titulo principal. Maximo 30 caracteres. '
    )

    fecha_publicacion = models.DateField(
        blank=False,
        null=False,
        help_text='Fecha de publicacion del post.'
    )

    autor = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text='Nombre del autor. -Opcional '
    )

    categoria = ParentalManyToManyField("projects.Categorias", blank=False)

    client = models.CharField(
        max_length=35,
        blank=False,
        null=True,
        help_text='Nombre del cliente.'
    )

    descripcion_proyecto = RichTextField(
        blank=True,
        max_length=5000,
        features=['bold', 'italic', 'h3', 'h2', 'image', 'link'],
        help_text='Escriba aqui el contenido de su proyecto. Maximo 5000 caracteres.'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('img_project', max_num=1, min_num=1, label='Imagen del proyecto'),
        ], heading='Imagen para el Post proyecto, resolucion optima 1200px X 840px'),
        MultiFieldPanel([
            FieldPanel('titulo_proyecto'),
            FieldPanel('fecha_publicacion'),
            FieldPanel('autor'),
            FieldPanel('categoria', widget=forms.CheckboxSelectMultiple),
            FieldPanel('client'),
            FieldPanel('descripcion_proyecto'),
        ], heading='Datos del Proyecto'),

    ]


class ImagenFondoBlog(Orderable):
    """ Imagen de fondo para el proyecto"""

    page = ParentalKey("BlogPost", related_name="img_project")
    imagen_proyecto = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel("imagen_proyecto"),
    ]


class Categorias(models.Model):
    nombre_categoria = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre_categoria', editable=True)

    panels = [
        FieldPanel('nombre_categoria'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        verbose_name_plural = 'Categorias Proyectos'
        ordering = ["nombre_categoria"]


register_snippet(Categorias)
