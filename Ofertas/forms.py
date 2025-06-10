from django import forms
from .models import Oferta
from django.forms.widgets import HiddenInput

ESTADO_CHOICES =(
    ("", "<Todos>"),
    ("Nuevo", "Nuevo"),
    ("Activo", "Activo"),
    ("Baja", "Baja")
)

class BuscaOfertaForm(forms.Form):
    titulo = forms.CharField()
    autor = forms.CharField()
    estado = forms.ChoiceField(choices = ESTADO_CHOICES)

    def __init__(self, *args, **kwargs):
        super(BuscaOfertaForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].required = False
        self.fields['autor'].required = False
        self.fields['estado'].required = False
        self.fields["titulo"].widget.attrs.update({"autofocus": "autofocus"})

