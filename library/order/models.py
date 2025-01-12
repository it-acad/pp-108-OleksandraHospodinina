from django.db import models, DataError
from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    """
    This class represents an Order.
    Attributes:
    -----------
    param book: foreign key Book
    type book: ForeignKey
    param user: foreign key CustomUser
    type user: ForeignKey
    param created_at: Describes the date when the order was created. Can't be changed.
    type created_at: datetime
    param end_at: Describes the actual return date of the book. (`None` if not returned)
    type end_at: datetime
    param plated_end_at: Describes the planned return period of the book (2 weeks from the moment of creation).
    type plated_end_at: datetime
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()

    def __str__(self):
        """
        Magic method to show information about the Order.
        :return: Order details including book id, user id, and timestamps
        """
        return f"Order(id={self.pk}, user={self.user.pk}, book={self.book.pk}, created_at={self.created_at}, end_at={self.end_at}, plated_end_at={self.plated_end_at})"

    def __repr__(self):
        """
        Magic method to show the class and id of the Order object.
        :return: class name and id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
        Returns order data as a dictionary.
        :return: order id, book id, user id, created_at, end_at, plated_end_at
        :Example:
        | {
        |   'id': 8,
        |   'book': 8,
        |   'user': 8,
        |   'created_at': '2025-01-01T12:00:00',
        |   'end_at': '2025-01-15T12:00:00',
        |   'plated_end_at': '2025-01-14T12:00:00',
        | }
        """
        return {
            'id': self.pk,
            'book': self.book.pk,
            'user': self.user.pk,
            'created_at': self.created_at.isoformat(),
            'end_at': self.end_at.isoformat() if self.end_at else None,
            'plated_end_at': self.plated_end_at.isoformat(),
        }

    @staticmethod
    def create(user, book, plated_end_at):
        """
        Create an order for a user and a book with a planned end date.
        :param user: CustomUser instance
        :param book: Book instance
        :param plated_end_at: Planned end date for the book return
        :return: the created order or None if the order cannot be created
        """
        if book.count == 1 and Order.objects.filter(book=book, end_at__isnull=True).exists():
            return None  # No available books for borrowing

        try:
            order = Order(user=user, book=book, plated_end_at=plated_end_at)
            order.save()
            return order
        except (ValueError, DataError) as e:
            # Handle any errors during order creation
            return None

    @staticmethod
    def get_by_id(order_id):
        """
        Get an order by its id.
        :param order_id: the id of the order to fetch
        :return: the Order instance or None if not found
        """
        try:
            return Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        """
        Update the order's return dates.
        :param plated_end_at: Updated planned return date
        :param end_at: Actual return date
        :return: None
        """
        if plated_end_at:
            self.plated_end_at = plated_end_at
        if end_at:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        """
        Get all orders.
        :return: List of all orders
        """
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        """
        Get all orders where books have not been returned yet.
        :return: Queryset of orders with null end_at
        """
        return Order.objects.filter(end_at=None)

    @staticmethod
    def delete_by_id(order_id):
        """
        Delete an order by its id.
        :param order_id: the id of the order to delete
        :return: True if deleted successfully, False if not found
        """
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False
