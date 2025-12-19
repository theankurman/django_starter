from django import forms
from django.template.loader import render_to_string


class DaisyFormMixin(forms.Form):
    def as_div(self):
        html = render_to_string("core/partials/forms/daisy/as_div.html", {"form": self})
        return html

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            classes: set[str] = set(field.widget.attrs.get("class", "").split())

            has_error = field_name in self.errors

            is_checkbox = isinstance(field.widget, forms.widgets.CheckboxInput)
            is_select = isinstance(field.widget, forms.widgets.Select)
            is_textarea = isinstance(field.widget, forms.widgets.Textarea)
            is_input = isinstance(field.widget, forms.widgets.TextInput) or isinstance(
                field.widget, forms.widgets.NumberInput
            )

            classes.add("w-full")
            if is_input:
                classes.add("input")
                if has_error:
                    classes.add("input-error")

            elif is_textarea:
                classes.add("textarea")
                if has_error:
                    classes.add("textarea-error")

            elif is_select:
                classes.add("select")
                if has_error:
                    classes.add("select-error")

            elif is_checkbox:
                classes.remove("w-full")
                if "checkbox" not in classes and "toggle" not in classes:
                    classes.add("toggle")
                if has_error and "checkbox" in classes:
                    classes.add("checkbox-error")

            # apply the classes
            field.widget.attrs["class"] = " ".join(classes)
