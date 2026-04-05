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
            {'title': 'Music Concerts', 'slug': 'music-concerts', 'image': 'https://picsum.photos/seed/music/800/600'},
            {'title': 'Standup Comedy', 'slug': 'standup-comedy', 'image': 'https://picsum.photos/seed/comedy/800/600'},
            {'title': 'Live Sports', 'slug': 'live-sports', 'image': 'https://picsum.photos/seed/sports/800/600'},
            {'title': 'Tech Conferences', 'slug': 'tech-conferences', 'image': 'https://picsum.photos/seed/tech/800/600'},
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
                'title': 'Sunburn Arena ft. Martin Garrix',
                'description': 'The biggest EDM festival returns to India. Get ready for an electrifying night with Martin Garrix performing his top hits live in Mumbai.',
                'category': categories['music-concerts'],
                'location': 'Jio World Garden, BKC, Mumbai',
                'price': 2500.00,
                'total_tickets': 5000,
                'available_tickets': 150, # Filling Fast
                'is_featured': True,
                'image_url': 'https://picsum.photos/seed/sunburn/1000/600',
                'days_from_now': 15
            },
            {
                'title': 'Zakir Khan Live - Sakht Launda',
                'description': 'Witness the sakht launda Zakir Khan in his brand new comedy special. An evening full of relatable stories and unstoppable laughs.',
                'category': categories['standup-comedy'],
                'location': 'Siri Fort Auditorium, New Delhi',
                'price': 999.00,
                'total_tickets': 1500,
                'available_tickets': 0, # Sold Out
                'is_featured': True,
                'image_url': 'https://picsum.photos/seed/zakir/1000/600',
                'days_from_now': 5
            },
            {
                'title': 'IPL 2026: MI vs CSK',
                'description': 'The ultimate clash of the titans. Watch Mumbai Indians take on Chennai Super Kings in an electrifying league match of the Indian Premier League.',
                'category': categories['live-sports'],
                'location': 'Wankhede Stadium, Mumbai',
                'price': 3500.00,
                'total_tickets': 33000,
                'available_tickets': 33000, # Available
                'is_featured': True,
                'image_url': 'https://picsum.photos/seed/ipl2/1000/600',
                'days_from_now': 45
            },
            {
                'title': 'Arijit Singh India Tour',
                'description': 'Soulful melodies and romantic tracks. Experience Arijit Singh live in concert for a night you will never forget.',
                'category': categories['music-concerts'],
                'location': 'Bhartiya City, Bengaluru',
                'price': 1500.00,
                'total_tickets': 10000,
                'available_tickets': 1200, # Filling Fast
                'is_featured': False,
                'image_url': 'https://picsum.photos/seed/arijit/1000/600',
                'days_from_now': 20
            },
            {
                'title': 'React India 2026',
                'description': 'The premier international React.js conference in India. Join core team members and industry experts for 3 days of talks and workshops.',
                'category': categories['tech-conferences'],
                'location': 'Grand Hyatt, Goa',
                'price': 7500.00,
                'total_tickets': 800,
                'available_tickets': 450, # Available
                'is_featured': False,
                'image_url': 'https://picsum.photos/seed/react/1000/600',
                'days_from_now': 60
            },
            {
                'title': 'Vir Das: Mind Fool Tour',
                'description': 'International Emmy Award winner Vir Das brings his new world tour to Pune. Get ready for an hour of fresh, unfiltered comedy.',
                'category': categories['standup-comedy'],
                'location': 'Phoenix Marketcity, Pune',
                'price': 1200.00,
                'total_tickets': 1200,
                'available_tickets': 0, # Sold Out
                'is_featured': False,
                'image_url': 'https://picsum.photos/seed/virdas/1000/600',
                'days_from_now': 10
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
