from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='events', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    total_tickets = models.PositiveIntegerField(default=100)
    available_tickets = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.marketplace_tickets == 0:
            return 'Sold Out'
        elif self.marketplace_tickets <= 50:
            return 'Filling Fast'
        return 'Available'

    @property
    def marketplace_tickets(self):
        return sum(listing.quantity for listing in self.listings.filter(is_active=True))

    @property
    def starting_price(self):
        active_listings = self.listings.filter(is_active=True)
        if active_listings.exists():
            return active_listings.order_by('price_per_ticket').first().price_per_ticket
        return None

class TicketListing(models.Model):
    seller = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='listings', on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100, default='General Admission')
    quantity = models.PositiveIntegerField(default=1)
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    authentication_image = models.ImageField(upload_to='ticket_proofs/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    listed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.ticket_type} for {self.event.title} by {self.seller.username}"

class Order(models.Model):
    buyer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    listing = models.ForeignKey(TicketListing, related_name='orders', on_delete=models.CASCADE)
    tickets_bought = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') # Pending, Completed, Failed

    def __str__(self):
        return f"Order #{self.id} - {self.tickets_bought} tickets by {self.buyer.username}"

class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=50, default='Pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_status}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    listing = models.ForeignKey(TicketListing, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    
    @property
    def average_rating(self):
        reviews = self.user.received_reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0
        
    @property
    def total_reviews(self):
        return self.user.received_reviews.count()
        
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'order')

    def __str__(self):
        return f"{self.rating} Stars by {self.reviewer.username} for {self.seller.username}"
