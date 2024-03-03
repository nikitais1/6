from django import forms
from blog.models import Blog


class StyleMixin(forms.ModelForm):
    """Миксин для вывода формы для блога"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            try:
                input_type = field.widged.input_type
                if input_type == 'checkbox':
                    field.widged.attrs['class'] = 'form-check'
                else:
                    field.widged.attrs['class'] = 'form-control'
            except AttributeError:
                field.widged.attrs['class'] = 'form-control'


class BlogForm(StyleMixin):
    """Класс формы для блога"""

    class Meta:
        model = Blog
        exclude = ('slug', 'create_date', 'view_count',)
