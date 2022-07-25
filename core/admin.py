import sys

from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import Textarea
from rest_framework_simplejwt import token_blacklist


# General admin class override with different featuresSacar CreateView de todos menos forecast
class BaseAdmin(admin.ModelAdmin):
    """Base ModelAdmin defining reasonable default admin panel behaviors"""

    def _init_(self, model, admin_site):
        # models.Autofield is the field type for the primary key
        # automatically added to all models by django.
        SEARCHABLE_FIELDS = [
            models.UUIDField,
            models.CharField,
            models.IntegerField,
            models.EmailField,
        ]

        # Decrease the size of the TextField input box, which is massive by default
        self.formfield_overrides = {
            models.TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 80})},
        }

        # By default, the only column in the admin table is the name of the object
        # Auto list display will add all fields to this table
        # If the child class sets list display, auto_list_display will be false
        auto_list_display = False
        if len(self.list_display) == 1:
            self.list_display = ["_str_"]
            auto_list_display = True

        # Initialize list_filter and search_fields fields to empty list,
        # But don't do this if it was already initialized by the child class.
        if len(self.search_fields) == 0:
            self.search_fields = []
        if len(self.list_filter) == 0:
            self.list_filter = []
        if len(self.raw_id_fields) == 0:
            self.raw_id_fields = []

        # Loop through all fields on the model and setup the admin panel to handle them
        for field in model._meta.fields:
            # Add all fields other than id to the
            # table overview if auto_list_display is on
            if (
                field.name not in self.list_display
                and field.name != "id"
                and auto_list_display
            ):
                self.list_display.append(field.name)

            if type(field) == models.ForeignKey or type(field) == models.OneToOneField:
                # All Foriegn keys should be searchable by ID
                self.search_fields.append(f"{field.name}__id")
                # All Foriegn keys should be raw_id_fields
                self.raw_id_fields.append(field.name)
                # Enable searching by the name of a foriegn model
                for foriegnField in field.related_model._meta.fields:
                    if foriegnField.name == "name":
                        self.search_fields.append(f"{field.name}__name")
                    if foriegnField.name == "title":
                        self.search_fields.append(f"{field.name}__title")

            # Enable search on all search fields specified above
            if type(field) in SEARCHABLE_FIELDS:
                self.search_fields.append(field.name)
            # Enable filtering on all boolean fields
            if type(field) == models.BooleanField:
                self.list_filter.append(field.name)

            # Enable searching by related candidate profiles name
            if field.name == "candidate_profile" or field.name == "candidate":
                self.search_fields.append(f"{field.name}__name")
                self.search_fields.append(f"{field.name}__display_email")

            # Enable searching by user email
            if field.related_model == get_user_model():
                self.search_fields.append(f"{field.name}__email")

        # This moves created at and is active to the last column
        if "is_active" in self.list_display:
            self.list_display.remove("is_active")
            self.list_display.append("is_active")
        if "created_at" in self.list_display:
            self.list_display.remove("created_at")
            self.list_display.append("created_at")
        super(BaseAdmin, self)._init_(model, admin_site)

    @classmethod
    def register_admin_classes(cls, app_name, context):
        """Register application admin classes into Django admin site"""
        if not app_name:
            raise Exception("No app name was provided for registering admin classes")

        app_models = apps.get_app_config(app_name).get_models()
        if not app_models:
            print(f"No models were found for the app '{app_name}'", file=sys.stderr)
            return

        if not context or not isinstance(context, dict):
            raise Exception(f"No context was provided for the app '{app_name}'")

        for model in app_models:
            admin_class = cls
            model_admin_class = f"{model.__name__}Admin"
            # if the admin class is defined in the app, override the default one
            if model_admin_class in context:
                admin_class = context[f"{model.__name__}Admin"]
            admin.site.register(model, admin_class)
