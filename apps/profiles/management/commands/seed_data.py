from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.themes.models import Theme
from apps.profiles.models import BirthdayProfile
from apps.memories.models import Memory
from apps.timeline.models import TimelineEvent
from apps.love_notes.models import LoveNote
from apps.music.models import BackgroundMusic
from apps.video_messages.models import VideoMessage
from apps.secret_message.models import SecretMessage
from apps.wishes.models import WishSubmission


class Command(BaseCommand):
    help = "Populate database with rich dummy demo data for backend and frontend testing."

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # 1. Create Superuser for Dashboard Access
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@birthdaywish.com", "is_staff": True, "is_superuser": True}
        )
        if created or not admin_user.check_password("admin123"):
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("✓ Superuser created: admin / admin123"))

        # 2. Get Default Theme
        theme = Theme.objects.filter(slug="luxury-dark").first() or Theme.objects.first()

        # 3. Create Main Birthday Profile (Slug: sneha)
        profile, p_created = BirthdayProfile.objects.get_or_create(
            slug="sneha",
            defaults={
                "full_name": "Sneha Sharma",
                "nickname": "Snehu",
                "birthday_date": date(1998, 9, 1),
                "relationship_start_date": date(2020, 2, 14),
                "first_meeting_date": date(2017, 8, 1),
                "intro_message": "Welcome to Sneha's Birthday Celebration! A magical journey of memories, love, and laughter.",
                "final_message": "Happy Birthday Snehu! May your year ahead be as bright and beautiful as your smile.",
                "special_letter": "Thank you for being my constant support and light.",
                "theme": theme,
                "is_active": True,
                "enable_animations": True,
            }
        )
        self.stdout.write(self.style.SUCCESS(f"✓ Birthday Profile created: /sneha/"))

        # 4. Create Memories for Sneha
        memories_data = [
            {
                "title": "Unforgettable Goa Sunset 🏖️",
                "memory_date": date(2023, 6, 15),
                "description": "Standing by the ocean waves watching the golden sunset together. Laughter, sea breeze, and endless late-night chats by the beach.",
                "display_order": 1,
            },
            {
                "title": "Graduation Day Triumph 🎓",
                "memory_date": date(2021, 8, 20),
                "description": "Tossing our graduation caps in the air after years of hard work, late-night study sessions, and cup noodles!",
                "display_order": 2,
            },
            {
                "title": "Surprise Birthday Party 🎉",
                "memory_date": date(2024, 9, 1),
                "description": "The look of utter shock and joy on your face when everyone shouted SURPRISE as you opened the lights!",
                "display_order": 3,
            },
        ]
        for m in memories_data:
            Memory.objects.get_or_create(
                birthday_profile=profile,
                title=m["title"],
                defaults=m
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Added {len(memories_data)} Memories"))

        # 5. Create Timeline Events for Sneha
        timeline_data = [
            {
                "title": "First Day at College",
                "event_date": date(2017, 8, 1),
                "description": "The day we met in the campus auditorium. Little did we know we would become best friends for life!",
                "icon": "🎓",
                "display_order": 1,
            },
            {
                "title": "First Backpacking Trip",
                "event_date": date(2019, 12, 24),
                "description": "Exploring the snowy peaks of Manali, sipping hot chai, and taking hundreds of photos.",
                "icon": "🏔️",
                "display_order": 2,
            },
            {
                "title": "First Job Offer Celebration",
                "event_date": date(2021, 6, 10),
                "description": "Celebrating your major career milestone with cake, dinner, and happy tears!",
                "icon": "💼",
                "display_order": 3,
            },
            {
                "title": "Another Year Wiser & Shining",
                "event_date": date(2025, 9, 1),
                "description": "Stepping into another amazing year filled with bigger dreams, bigger smiles, and unconditional love.",
                "icon": "✨",
                "display_order": 4,
            },
        ]
        for t in timeline_data:
            TimelineEvent.objects.get_or_create(
                birthday_profile=profile,
                title=t["title"],
                defaults=t
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Added {len(timeline_data)} Timeline Events"))

        # 6. Create Love Notes for Sneha
        notes_data = [
            {
                "title": "A Note of Gratitude 💖",
                "message": "Sneha, your warmth and positive energy bring light into every room you enter. Thank you for being such an extraordinary friend!",
                "icon": "💖",
                "display_order": 1,
            },
            {
                "title": "Always Keep Smiling 😊",
                "message": "From late-night phone calls to sudden coffee plans, life is so much fun with you. Wishing you all the love and happiness in the universe!",
                "icon": "😊",
                "display_order": 2,
            },
            {
                "title": "To My Partner in Crime 👭",
                "message": "Here is to many more spontaneous trips, laughing until our stomachs hurt, and making unforgettable memories together. Happy Birthday!",
                "icon": "👭",
                "display_order": 3,
            },
        ]
        for n in notes_data:
            LoveNote.objects.get_or_create(
                birthday_profile=profile,
                title=n["title"],
                defaults=n
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Added {len(notes_data)} Love Notes"))

        # 7. Create Background Music Tracks
        music_data = [
            {
                "title": "Acoustic Birthday Melody",
                "artist": "SoundHelix Chill",
                "external_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                "is_primary": True,
                "display_order": 1,
            },
            {
                "title": "Celebration Symphony",
                "artist": "SoundHelix Festive",
                "external_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                "is_primary": False,
                "display_order": 2,
            },
        ]
        for mus in music_data:
            BackgroundMusic.objects.get_or_create(
                birthday_profile=profile,
                title=mus["title"],
                defaults=mus
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Added {len(music_data)} Music Tracks"))

        # 8. Create Video Messages
        videos_data = [
            {
                "sender_name": "College Gang (Pooja & Rohan)",
                "relationship": "Best Friends",
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "message_text": "Happy Birthday Snehu! We love you so much and can't wait to celebrate with you tonight!",
                "display_order": 1,
            },
            {
                "sender_name": "Mom & Dad",
                "relationship": "Parents",
                "video_url": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
                "message_text": "May God bless you with endless happiness, good health, and success. Happy Birthday sweetheart!",
                "display_order": 2,
            },
        ]
        for v in videos_data:
            VideoMessage.objects.get_or_create(
                birthday_profile=profile,
                sender_name=v["sender_name"],
                defaults=v
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Added {len(videos_data)} Video Messages"))

        # 9. Create Secret Message for Sneha
        SecretMessage.objects.get_or_create(
            birthday_profile=profile,
            defaults={
                "title": "Surprise Gift Sealed! 🔒",
                "secret_text": "Surprise Snehu! We have booked a weekend luxury getaway trip to the hills for you! Pack your bags! 🏔️✨🎁",
                "pin_code": "1234",
                "hint": "Enter passcode PIN: 1234",
            }
        )
        self.stdout.write(self.style.SUCCESS("✓ Added Secret Message (PIN: 1234)"))

        # 10. Create Public Wish Submissions
        wishes_data = [
            {
                "sender_name": "Aunt Sunita",
                "message": "Wishing you a bright year ahead filled with happiness, good health, and immense success! Happy Birthday dear Sneha! ❤️",
                "candle_blown": True,
                "is_approved": True,
            },
            {
                "sender_name": "Vikram Seth",
                "message": "Happy Birthday Snehu! Stay blessed and keep shining as bright as ever!",
                "candle_blown": True,
                "is_approved": True,
            },
            {
                "sender_name": "Neha & Sameer",
                "message": "Sending you tons of love, hugs, and warm birthday wishes on your special day!",
                "candle_blown": False,
                "is_approved": True,
            },
        ]
        for w in wishes_data:
            WishSubmission.objects.get_or_create(
                birthday_profile=profile,
                sender_name=w["sender_name"],
                defaults=w
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Added {len(wishes_data)} Public Wishes"))

        # 11. Create Second Profile (Slug: priya) for testing multi-tenancy
        profile_priya, p2_created = BirthdayProfile.objects.get_or_create(
            slug="priya",
            defaults={
                "full_name": "Priya Verma",
                "nickname": "Pree",
                "birthday_date": date(1997, 5, 20),
                "intro_message": "A special digital birthday experience dedicated to Priya Verma!",
                "final_message": "Happy Birthday Priya! Wishing you laughter, health, and prosperity.",
                "theme": Theme.objects.filter(slug="romantic-rose").first() or theme,
                "is_active": True,
            }
        )
        self.stdout.write(self.style.SUCCESS("✓ Second Profile created: /priya/"))

        self.stdout.write(self.style.SUCCESS("\n🎉 Demo Data Seeding Completed Successfully!"))
