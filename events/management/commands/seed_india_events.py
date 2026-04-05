import os
import urllib.request
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import User
import random
from events.models import Category, Event, TicketListing

class Command(BaseCommand):
    help = 'Seed database with realistic Indian events'

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing old events, categories, and listings...")
        TicketListing.objects.all().delete()
        Event.objects.all().delete()
        Category.objects.all().delete()

        categories_data = [
            {'title': 'Music Concerts', 'slug': 'music-concerts', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Ed_Sheeran_2013.jpg/800px-Ed_Sheeran_2013.jpg'},
            {'title': 'Standup Comedy', 'slug': 'standup-comedy', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Microphone_in_a_dark_room.jpg/800px-Microphone_in_a_dark_room.jpg'},
            {'title': 'Live Sports', 'slug': 'live-sports', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/M._Chinnaswamy_Stadium.jpg/800px-M._Chinnaswamy_Stadium.jpg'},
            {'title': 'Tech Conferences', 'slug': 'tech-conferences', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Web_Summit_2018_-_Centre_Stage_%2831868580008%29.jpg/800px-Web_Summit_2018_-_Centre_Stage_%2831868580008%29.jpg'},
        ]

        categories = {}
        for cat in categories_data:
            c = Category.objects.create(title=cat['title'], slug=cat['slug'])
            categories[cat['slug']] = c
            
            self.stdout.write(f"Downloading image for Category: {c.title}...")
            try:
                req = urllib.request.Request(cat['image'], headers={'User-Agent': 'Mozilla/5.0'})
                result = urllib.request.urlopen(req)
                with open(f"temp_cat_{cat['slug']}.jpg", 'wb') as f:
                    f.write(result.read())
                    
                with open(f"temp_cat_{cat['slug']}.jpg", 'rb') as f:
                    c.image.save(f"{cat['slug']}.jpg", File(f), save=False)
                
                os.remove(f"temp_cat_{cat['slug']}.jpg")
                c.save()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to download image: {e}"))

        events_data = [
            {
                'title': 'Diljit Dosanjh - Dil-Luminati Tour',
                'description': 'The biggest Punjabi music tour hits India! Catch Diljit Dosanjh performing live in Mumbai with his blockbuster hits.',
                'category': categories['music-concerts'],
                'location': 'Jio World Garden, BKC, Mumbai',
                'price': 4500.00,
                'total_tickets': 15000,
                'available_tickets': 150, # Filling Fast
                'is_featured': True,
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Diljit_Dosanjh_at_the_Film_Fare_awards.jpg/800px-Diljit_Dosanjh_at_the_Film_Fare_awards.jpg',
                'days_from_now': 15
            },
            {
                'title': 'Anubhav Singh Bassi - Kisi Ko Batana Mat',
                'description': 'Bassi is back with a fresh set of hilarious stories. Grab your tickets before they sell out for the biggest comedy show of the year!',
                'category': categories['standup-comedy'],
                'location': 'Siri Fort Auditorium, New Delhi',
                'price': 1200.00,
                'total_tickets': 1800,
                'available_tickets': 0, # Sold Out
                'is_featured': True,
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Microphone_in_a_dark_room.jpg/800px-Microphone_in_a_dark_room.jpg',
                'days_from_now': 5
            },
            {
                'title': 'IPL 2026: RCB vs CSK',
                'description': 'The Southern Derby! Watch Royal Challengers Bangalore take on Chennai Super Kings in a thrilling group stage clash.',
                'category': categories['live-sports'],
                'location': 'M. Chinnaswamy Stadium, Bengaluru',
                'price': 3500.00,
                'total_tickets': 39000,
                'available_tickets': 33000, # Available
                'is_featured': True,
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/M._Chinnaswamy_Stadium.jpg/800px-M._Chinnaswamy_Stadium.jpg',
                'days_from_now': 8
            },
            {
                'title': 'Arijit Singh Live In Concert',
                'description': 'Soulful melodies and romantic tracks. Experience Arijit Singh live in concert for a night of musical magic.',
                'category': categories['music-concerts'],
                'location': 'EKA Arena, Ahmedabad',
                'price': 2500.00,
                'total_tickets': 12000,
                'available_tickets': 1200, # Filling Fast
                'is_featured': False,
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Arijit_Singh_at_Renault_Star_Guild_Awards_2014.jpg/800px-Arijit_Singh_at_Renault_Star_Guild_Awards_2014.jpg',
                'days_from_now': 20
            },
            {
                'title': 'Sunburn Arena ft. Alan Walker',
                'description': 'India, are you ready? Alan Walker brings the spectacular Walkerworld Tour to Pune for massive EDM night.',
                'category': categories['music-concerts'],
                'location': 'NESCO Center, Pune',
                'price': 3000.00,
                'total_tickets': 8000,
                'available_tickets': 450, # Available
                'is_featured': False,
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Alan_Walker_-_Stavernfestivalen_2018.jpg/800px-Alan_Walker_-_Stavernfestivalen_2018.jpg',
                'days_from_now': 60
            },
            {
                'title': 'India Blockchain Week 2026',
                'description': 'The hottest Web3 and tech conference in Asia. Join developers, founders, and investors for groundbreaking panel discussions.',
                'category': categories['tech-conferences'],
                'location': 'Grand Hyatt, Bengaluru',
                'price': 5500.00,
                'total_tickets': 1200,
                'available_tickets': 800, # Available
                'is_featured': False,
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Web_Summit_2018_-_Centre_Stage_%2831868580008%29.jpg/800px-Web_Summit_2018_-_Centre_Stage_%2831868580008%29.jpg',
                'days_from_now': 30
            }
        ]

        for ed in events_data:
            event_date = timezone.now().date() + timedelta(days=ed['days_from_now'])
            event_time = timezone.now().time()
            
            event = Event(
                title=ed['title'],
                description=ed['description'],
                category=ed['category'],
                date=event_date,
                time=event_time,
                location=ed['location'],
                price=ed['price'],
                total_tickets=ed['total_tickets'],
                available_tickets=ed['available_tickets'],
                is_featured=ed['is_featured']
            )
            
            self.stdout.write(f"Downloading image for {ed['title']}...")
            try:
                # Need user agent sometimes or Unsplash blocks standard urllib
                req = urllib.request.Request(ed['image_url'], headers={'User-Agent': 'Mozilla/5.0'})
                result = urllib.request.urlopen(req)
                with open(f"temp_{ed['title'][:5]}.jpg", 'wb') as f:
                    f.write(result.read())
                    
                with open(f"temp_{ed['title'][:5]}.jpg", 'rb') as f:
                    event.image.save(f"{ed['title'].replace(' ', '_')}.jpg", File(f), save=False)
                
                os.remove(f"temp_{ed['title'][:5]}.jpg")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to download image: {e}"))
                
            event.save()
            self.stdout.write(self.style.SUCCESS(f"Created event: {event.title}"))

        self.stdout.write("Seeding Marketplace Listings for the Events...")
        users = []
        for i in range(1, 6):
            u, created = User.objects.get_or_create(username=f'seller_{i}')
            if created:
                u.set_password('seller123')
                u.save()
            users.append(u)

        for event in Event.objects.all():
            for _ in range(random.randint(2, 6)):
                TicketListing.objects.create(
                    seller=random.choice(users),
                    event=event,
                    ticket_type=random.choice(['VIP Box', 'General Admission', 'Front Row', 'Balcony']),
                    quantity=random.randint(1, 4),
                    price_per_ticket=round(float(event.price) * random.uniform(0.8, 2.5), 2),
                    is_active=True
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Database with Indian Events and Live Reselling Listings!"))
