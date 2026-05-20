from django import forms


class CompetitorSearchForm(forms.Form):
    query = forms.CharField(
        label="Ключевая фраза",
        max_length=120,
        error_messages={"required": "Введите ключевую фразу для поиска."},
        widget=forms.TextInput(
            attrs={
                "placeholder": "Например: черная шапка",
                "autocomplete": "off",
            }
        ),
    )

    def clean_query(self):
        return " ".join(self.cleaned_data["query"].strip().split())
