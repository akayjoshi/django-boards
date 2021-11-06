from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(
        attrs={"rows":5, 'placeholder': 'dekho single m h ik double m'}
    ),
         max_length=4000,
         help_text="help text model me v de ska"
     ) # we need this to save in Post model

    class Meta:
        model = Topic
        fields = ['subject', 'message']  #subject field is related to Topic model

        # override default attributes
        # def __init__(self, *args, **kwargs):
        #     super(NewTopicForm, self).__init__(*args,**kwargs)
        #     placeholder = 'subject'
        #     self.fields['subject'].widget.attrs['placeholder']= placeholder