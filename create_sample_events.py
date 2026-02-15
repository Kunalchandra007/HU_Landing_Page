#!/usr/bin/env python
"""Script to create sample events for the event management system"""

from app import app, db
from models import Event
from datetime import date

def create_sample_events():
    """Create sample events"""
    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()
        
        # Sample events data
        sample_events = [
            {
                'title': 'Canvas Competition',
                'description': 'Unleash your creativity in this exciting canvas art competition. Showcase your artistic talent and win amazing prizes...',
                'event_date': date(2026, 2, 14),
                'image_path': 'images/canvacomp.jpeg'
            },
            {
                'title': 'DJ Night',
                'description': 'Dance the night away with electrifying music and performances by top DJs. An unforgettable evening of entertainment...',
                'event_date': date(2026, 2, 15),
                'image_path': 'images/djnight.jpeg'
            },
            {
                'title': 'Photography Competition',
                'description': 'Capture the essence of moments. Participate in our photography competition and exhibit your best work...',
                'event_date': date(2026, 2, 14),
                'image_path': 'images/photographycomp.jpeg'
            },
            {
                'title': 'Ramp Walk',
                'description': 'Showcase fashion and style on the ramp. A glamorous event featuring the latest trends and talented models...',
                'event_date': date(2026, 2, 15),
                'image_path': 'images/rampwalk.jpeg'
            }
        ]
        
        # Check if events already exist
        for event_data in sample_events:
            existing = Event.query.filter_by(title=event_data['title']).first()
            if not existing:
                event = Event(
                    title=event_data['title'],
                    description=event_data['description'],
                    event_date=event_data['event_date'],
                    image_path=event_data['image_path'],
                    is_active=True
                )
                db.session.add(event)
                print(f"✓ Added: {event_data['title']}")
            else:
                print(f"- Already exists: {event_data['title']}")
        
        db.session.commit()
        print("\nSample events created successfully!")

if __name__ == '__main__':
    create_sample_events()
