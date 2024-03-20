from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import InlinePanel, MultiFieldPanel, FieldPanel



class HomePage(Page):
    template = "index/index.html"
    max_count = 1

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('logo_image', max_num=6, min_num=0),
        ], heading='Sección logos clientes, formato PNG y resolución de 220px X 80px. Máximo de 6 logos.'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        return context



class LogoClientes(Orderable):
    """Logos Clientes para carousel"""

    page = ParentalKey("home.HomePage", related_name="logo_image")
    logo_cliente = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('logo_cliente'),
    ]
