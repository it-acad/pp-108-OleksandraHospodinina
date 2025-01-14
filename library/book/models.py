from django.db import models
from django.conf import settings

class Book(models.Model):
    name = models.CharField(blank=True, max_length=128)
    description = models.CharField(blank=True, max_length=256)
    count = models.IntegerField(default=10)
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='book_orders',
        verbose_name='User who borrowed the book'
    )
    author = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="Author"
    )

    def __str__(self):
        return f"Book(id={self.id}, name={self.name}, order={self.order})"

    def __repr__(self):
        return f"Book(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def delete_by_id(book_id):
        book = Book.get_by_id(book_id)
        if book:
            book.delete()
            return True
        return False

    @staticmethod
    def create(name, description, count=10):
        if len(name) > 128:
            return None
        book = Book.objects.create(name=name, description=description, count=count)
        return book

    def update(self, name=None, description=None, count=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if count:
            self.count = count
        self.save()

    @staticmethod
    def get_all():
        return list(Book.objects.all())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'order': self.order.id if self.order else None
        }
