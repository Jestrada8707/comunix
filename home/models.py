from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import InlinePanel, MultiFieldPanel, FieldPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from projects.models import BlogPost, Categorias


class HomePage(RoutablePageMixin, Page):
    template = "index/index.html", "projects/_portfolio_items.html"
    max_count = 1

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('logo_image', max_num=6, min_num=0),
        ], heading='Sección logos clientes, formato PNG y resolución de 220px X 80px. Máximo de 6 logos.'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['projects'] = BlogPost.objects.all().order_by('-id')[:6]
        context['categorias'] = Categorias.objects.all()
        return context

    @route(r'^cat/(?P<cat_slug>[-\w]*)/$', name="category_view")
    def category_view(self, request, cat_slug):
        """Encontrar publicaciones por categoria"""

        context = self.get_context(request)

        try:
            category = Categorias.objects.get(slug=cat_slug)

        except Categorias.DoesNotExist:
            return render(request, "projects/category_not_found.html")

        context["projects"] = BlogPost.objects.live().public().filter(categoria__in=[category])
        return render(request, "projects/category_filter_page.html", context)


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
