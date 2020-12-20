from django import forms
from django.contrib.auth.models import Group as Role


class RoleForm(forms.ModelForm):
    """
    Form for creating and modifying user role objects
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        #: The model of this :class:`django.forms.ModelForm`
        model = Role
        #: The fields of the model which should be handled by this form
        fields = ["name", "permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: Derive size from view height (fill complete available space with select field)
        self.fields["permissions"].widget.attrs["size"] = "20"
