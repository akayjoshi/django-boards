from django.test import TestCase
from django import forms
from boards.templatetags.form_tags import field_type, input_class

class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['name', 'password']

class FieldTypeTests(TestCase):
    def test_field_widget_name(self):
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))

class InputClassTests(TestCase):
    def test_unbound_form_initial_state(self):
        form = ExampleForm() # un bound form
        self.assertEquals('form-control ', input_class(form['name']))
    
    def test_bound_field_invalid_state(self):
        form = ExampleForm({'name': '', 'password': 123})
        self.assertEquals('form-control is-invalid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))
    
    def test_valid_bound_field(self):
        form = ExampleForm({'name': 'ajay', 'password': '123'})
        self.assertEquals('form-control is-valid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))