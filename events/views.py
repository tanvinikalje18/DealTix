from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
import razorpay
from .models import Event, Category, TicketListing, Order, Payment, Message, UserProfile, Review

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome to DealTix!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    featured_events = Event.objects.filter(is_featured=True).order_by('-date')[:3]
    categories = Category.objects.all()
    recent_events = Event.objects.all().order_by('-created_at')[:6]
    context = {
        'featured_events': featured_events,
        'categories': categories,
        'recent_events': recent_events
    }
    return render(request, 'events/home.html', context)

def event_list(request):
    events = Event.objects.all().order_by('date')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        events = events.filter(title__icontains=query)
        
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        events = events.filter(category__slug=category_slug)
        
    categories = Category.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'current_category': category_slug,
        'query': query
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Marketplace Filters
    listings = event.listings.filter(is_active=True)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    ticket_type = request.GET.get('ticket_type')
    
    if min_price:
        listings = listings.filter(price_per_ticket__gte=min_price)
    if max_price:
        listings = listings.filter(price_per_ticket__lte=max_price)
    if ticket_type:
        listings = listings.filter(ticket_type__icontains=ticket_type)
        
    return render(request, 'events/event_detail.html', {
        'event': event,
        'filtered_listings': listings,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'ticket_type': ticket_type or ''
    })

@login_required
def dashboard(request):
    orders = request.user.orders.all().order_by('-order_date')
    listings = request.user.listings.all().order_by('-listed_at')
    
    # Pre-fetch reviews for the user's orders to know if they've rated already
    rated_order_ids = set(request.user.given_reviews.values_list('order_id', flat=True))
    
    return render(request, 'events/dashboard.html', {
        'orders': orders, 
        'listings': listings,
        'rated_order_ids': rated_order_ids
    })

@login_required
def rate_seller(request, order_id):
    order = get_object_or_404(Order, pk=order_id, buyer=request.user, status='Completed')
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        
        Review.objects.update_or_create(
            reviewer=request.user,
            order=order,
            defaults={
                'seller': order.listing.seller,
                'rating': rating,
                'comment': comment
            }
        )
        messages.success(request, f"Review submitted for {order.listing.seller.username}!")
        
    return redirect('dashboard')

@login_required
def sell_ticket(request):
    events = Event.objects.all().order_by('date')
    import json
    
    events_data = {
        e.id: {
            'base_price': float(e.price),
            'starting_price': float(e.starting_price) if e.starting_price else float(e.price)
        } for e in events
    }
    
    events_json = json.dumps(events_data)
    
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        ticket_type = request.POST.get('ticket_type', 'General Admission')
        quantity = int(request.POST.get('quantity', 1))
        price_per_ticket = float(request.POST.get('price_per_ticket', 0.0))
        authentication_image = request.FILES.get('authentication_image')
        
        event = get_object_or_404(Event, id=event_id)
        
        if quantity > 0 and price_per_ticket >= 0:
            TicketListing.objects.create(
                seller=request.user,
                event=event,
                ticket_type=ticket_type,
                quantity=quantity,
                price_per_ticket=price_per_ticket,
                authentication_image=authentication_image
            )
            messages.success(request, f"Successfully listed {quantity} tickets for {event.title}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid details provided.")
            
    return render(request, 'events/sell_ticket.html', {
        'events': events,
        'events_json': events_json
    })

@login_required
def checkout(request, listing_id):
    listing = get_object_or_404(TicketListing, pk=listing_id, is_active=True)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if 0 < quantity <= listing.quantity:
            return render(request, 'events/checkout.html', {'listing': listing, 'quantity': quantity})
        else:
            messages.error(request, f"Only {listing.quantity} tickets available.")
            return redirect('event_detail', pk=listing.event.pk)
    return redirect('event_detail', pk=listing.event.pk)

@login_required
def buy_ticket(request, listing_id):
    listing = get_object_or_404(TicketListing, pk=listing_id, is_active=True)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        delivery_address = request.POST.get('delivery_address', '')
        
        if 0 < quantity <= listing.quantity:
            total_price = listing.price_per_ticket * quantity
            
            order = Order.objects.create(
                buyer=request.user,
                listing=listing,
                tickets_bought=quantity,
                total_price=total_price,
                delivery_address=delivery_address,
                status='Pending'
            )
            
            razorpay_amount = int(float(total_price) * 100)
            
            # Use mock order ID to bypass Razorpay API
            mock_order_id = f"order_mock_{order.id}"
            
            Payment.objects.create(
                user=request.user,
                order=order,
                payment_status='Pending',
                razorpay_order_id=mock_order_id
            )
            
            context = {
                'order': order,
                'listing': listing,
                'razorpay_order_id': mock_order_id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': razorpay_amount,
                'currency': "INR",
            }
            return render(request, 'events/payment.html', context)
        else:
            messages.error(request, f"Only {listing.quantity} tickets available from this seller.")
    return redirect('event_detail', pk=listing.event.pk)

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            
            if not razorpay_order_id.startswith('order_mock_'):
                razorpay_client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                })
            
            payment.payment_status = 'Success'
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.save()
            
            order = payment.order
            order.status = 'Completed'
            order.save()
            
            listing = order.listing
            listing.quantity -= order.tickets_bought
            if listing.quantity == 0:
                listing.is_active = False
            listing.save()
            
            messages.success(request, f"Payment successful! You bought {order.tickets_bought} tickets.")
            return redirect('dashboard')
            
        except razorpay.errors.SignatureVerificationError:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.payment_status = 'Failed'
            payment.save()
            
            payment.order.status = 'Failed'
            payment.order.save()
            
            messages.error(request, "Payment signature verification failed. Please try again.")
            return redirect('dashboard')
            
    return redirect('home')

@login_required
def inbox(request):
    messages_query = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
    
    threads = {}
    for msg in messages_query:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        buyer = msg.sender if msg.sender != msg.listing.seller else msg.receiver
        thread_key = f"{msg.listing.id}_{buyer.id}"
        
        if thread_key not in threads:
            threads[thread_key] = {
                'listing': msg.listing,
                'other_user': other_user,
                'buyer_id': buyer.id,
                'last_message': msg,
                'unread_count': 0
            }
        
        if msg.receiver == request.user and not msg.is_read:
            threads[thread_key]['unread_count'] += 1

    return render(request, 'events/inbox.html', {'threads': threads.values()})

@login_required
def chat_view(request, listing_id, buyer_id):
    listing = get_object_or_404(TicketListing, pk=listing_id)
    buyer = get_object_or_404(User, pk=buyer_id)
    seller = listing.seller
    
    if request.user != buyer and request.user != seller:
        messages.error(request, "You are not authorized to view this chat.")
        return redirect('inbox')
        
    other_user = seller if request.user == buyer else buyer

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                listing=listing,
                content=content
            )
            return redirect('chat_view', listing_id=listing.id, buyer_id=buyer.id)

    Message.objects.filter(
        listing=listing, 
        sender=other_user, 
        receiver=request.user, 
        is_read=False
    ).update(is_read=True)

    chat_messages = Message.objects.filter(
        listing=listing,
        sender__in=[buyer, seller],
        receiver__in=[buyer, seller]
    ).order_by('timestamp')

    return render(request, 'events/chat.html', {
        'listing': listing,
        'chat_messages': chat_messages,
        'other_user': other_user,
        'buyer': buyer
    })
