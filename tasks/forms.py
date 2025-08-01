from django import forms
from .models import Task, TaskDetail

# ===============================
# Plain Django Form (Not ModelForm)
# ===============================
class TaskForm(forms.Form):
    title = forms.CharField(label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description") 
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])
    
    # Constructor to load employees dynamically
    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id, emp.name) for emp in employees
        ]

# ===============================
# Style Mixin for Tailwind CSS
# ===============================
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

# ===============================
# ModelForm for Task
# ===============================
class TaskModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget(),
            'assigned_to': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# ===============================
# ModelForm for TaskDetail
# ===============================
class TaskDetailModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes']
