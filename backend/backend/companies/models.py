from django.db import models


# Note: I don't know what is the "future" purpose of storing the quote data.
# I assume it is better to model/normalize the data at a later date.
class CompanyStockQuote(models.Model):
    # Note: this field could be replaced by a foreign key in future to
    # a related "Company" model.
    symbol = models.CharField(max_length=8)
    open = models.DecimalField(max_digits=10, decimal_places=4)
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    # Note: I am not sure how big can a volume get but Int should suffice,
    # if not we could use BigInt here.
    volume = models.IntegerField()
