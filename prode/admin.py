from core.admin import BaseAdmin

# Auto register each model in this app to django admin.
BaseAdmin.register_admin_classes("prode", globals())
