# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import operator
import functools
from string import ascii_uppercase
from csv_schema import models
from django.views.generic import (
    ListView, RedirectView, DetailView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q
from django.conf import settings
from django.apps import apps


if getattr(settings, "SITE_PREFIX", ""):
    SITE_PREFIX = "/{}".format(settings.SITE_PREFIX.strip("/"))
else:
    SITE_PREFIX = ""


class EditView(LoginRequiredMixin, ListView):
    paginate_by = 100
    template_name = "forms/edit_form.html"

    def get_queryset(self):
        m = apps.get_model("csv_schema", self.kwargs["model_name"])
        return m.objects.all()

    def get_context_data(self, *args, **kwargs):
        ctx = super(EditView, self).get_context_data(*args, **kwargs)
        ctx["model"] = apps.get_model("csv_schema", self.kwargs["model_name"])
        return ctx


class AddView(LoginRequiredMixin, TemplateView):
    template_name = "forms/add_form.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(AddView, self).get_context_data(*args, **kwargs)
        ctx["model"] = apps.get_model("csv_schema", self.kwargs["model_name"])
        return ctx


class IndexView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return SITE_PREFIX + reverse('database_list')


class ColumnDetail(DetailView):
    model = models.Column
    template_name = "column_detail.html"


class DatabaseList(ListView):
    model = models.Database
    template_name = "database_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(DatabaseList, self).get_queryset()
        return qs.all_populated()


class DatabaseDetail(DetailView):
    model = models.Database
    slug_url_kwarg = 'db_name'
    slug_field = 'name'
    template_name = "database_detail.html"


class TableDetail(DetailView):
    model = models.Table
    template_name = "table_detail.html"

    def get_object(self, *args, **kwargs):
        return models.Table.objects.get(
            name=self.kwargs["table_name"],
            database__name=self.kwargs["db_name"]
        )

    def get_context_data(self, *args, **kwargs):
        # get the list of tables in this database
        ctx = super(TableDetail, self).get_context_data(*args, **kwargs)
        ctx["tables"] = self.object.database.table_set.all_populated()
        return ctx


class NcdrReferenceRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return SITE_PREFIX + reverse('ncdr_reference_list', kwargs=dict(letter="A"))


class NcdrReferenceList(ListView):
    model = models.Column
    template_name = "ncdr_reference_list.html"
    NUMERIC = "0-9"
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        references = super(
            NcdrReferenceList, self
        ).get_queryset()

        if self.kwargs["letter"] == self.NUMERIC:
            """ startswith 0, or 1, or 2 etc
            """
            startswith_args = [Q(name__startswith=str(i)) for i in range(10)]
            return references.filter(
                functools.reduce(operator.or_, startswith_args)
        )

        return references.filter(name__istartswith=self.kwargs["letter"][0])

    def get_context_data(self, *args, **kwargs):
        ctx = super(NcdrReferenceList, self).get_context_data(*args, **kwargs)
        symbols = [i for i in ascii_uppercase]
        symbols.append(self.NUMERIC)
        url = lambda x: reverse('ncdr_reference_list', kwargs=dict(letter=x))
        ctx['other_pages'] = ((symbol, SITE_PREFIX + url(symbol),) for symbol in symbols)
        return ctx


class GroupingRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('grouping_detail', kwargs=dict(
            slug=models.Grouping.objects.first().slug)
        )


class GroupingDetail(DetailView):
    model = models.Grouping
    template_name = "grouping_detail.html"

    def get_context_data(self, *args, **kwargs):
        # get the list of tables in this database
        ctx = super(GroupingDetail, self).get_context_data(*args, **kwargs)
        ctx["groupings"] = models.Grouping.objects.all().order_by('name')
        return ctx


class AboutView(TemplateView):
    template_name = "about.html"
