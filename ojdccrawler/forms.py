from django import forms


class SearchDicForm(forms.Form):
    query = forms.CharField(min_length=1, max_length=20, strip=True, required=True, label='',
                            help_text='請輸入想搜尋的字詞（ 1 - 20 字）。',
                            widget=forms.TextInput(attrs={'lang': 'jp', 'autofocus': '',
                                                          'placeholder': '言葉を入力して検索する'}))

    def clean_query(self):
        data = self.cleaned_data['query']

        return data
