from django import forms
from .models import Task

#Django Form
class TaskForm(forms.Form):
    title = forms.CharField(label="Task Title")
    description = forms.CharField(widget=forms.Textarea,label="Task Description") 
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])
    

# database theke employee anar jonno constructor
    def __init__(self,*args, **kwargs):
        employees = kwargs.pop("employees",[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id, emp.name) for emp in employees
        ]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
    
            base_class = 'w-full border border-gray-300 rounded px-3 py-2 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500'
            
            if field_name == 'description':
                field.widget.attrs.update({
                    'class': base_class,
                    'rows': 4,
                    'placeholder': 'Enter task description'
                })
                
            elif field_name == 'due_date':
                field.widget.attrs.update({'class': base_class})
                
            elif field_name == 'assigned_to':
                field.widget.attrs.update({'class': 'mb-3 space-y-2'})
                
            elif field_name == 'title':
                field.widget.attrs.update({
                    'class': base_class,
                    'placeholder': 'Enter task title'
                })
                
            else:
                field.widget.attrs.update({'class': base_class})

# Django Model Form
class TaskModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']

        # or
        # exclude = ['project', 'is_completed'] # egula bade baki sob
        
        widgets = {
            'due_date': forms.SelectDateWidget(),
            'assigned_to': forms.CheckboxSelectMultiple(),
        }