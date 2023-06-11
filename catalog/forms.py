from django import forms
from catalog.models import Book, BookInstance, Author
from django.views.generic.edit import CreateView

class LoanBookForm(forms.ModelForm):
    """Form for a librarian to loan books."""

    # Disable the book field to prevent the user from entering a book
    # book_title is for display purposes only - set required=False
    book_title = forms.CharField(disabled=True, required=False)

    class Meta:
        # Display only the book title and the borrower to the librarian
        model = BookInstance
        fields = ('book_title', 'borrower',)

from django import forms
from catalog.models import Book, Author

class BookForm(forms.ModelForm):
    author_first_name = forms.CharField(max_length=100)
    author_last_name = forms.CharField(max_length=100)

    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'genre', 'image']

    def save(self, commit=True):
        book = super().save(commit=False)
        author_first_name = self.cleaned_data['author_first_name']
        author_last_name = self.cleaned_data['author_last_name']

        if author_first_name and author_last_name:
            author, _ = Author.objects.get_or_create(
                first_name=author_first_name,
                last_name=author_last_name
            )
            book.author = author

        if commit:
            book.save()
        return book




class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'catalog/book_form.html'

    def form_valid(self, form):
        form.instance.author_first_name = form.cleaned_data['author_first_name']
        form.instance.author_last_name = form.cleaned_data['author_last_name']
        return super().form_valid(form)