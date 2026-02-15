from app import app
from models import db, Happening

def add_happenings():
    with app.app_context():
        # Check if happenings already exist
        existing_count = Happening.query.count()
        
        happenings_data = [
            {
                'title': 'Memorandum of Understanding (MoU) with IIT Roorkee',
                'description': 'A significant milestone was achieved as the Indian Institute of Technology (IIT) Roorkee and Haridwar University, Roorkee formalized their collaboration through the signing of a Memorandum of Understanding (MoU). This strategic partnership aims to strengthen academic cooperation, promote research and innovation, and create opportunities for knowledge exchange between the two esteemed institutions. The MoU is expected to facilitate collaborative research projects, expert lectures, skill development programs, internships, and other academic initiatives that will benefit students and faculty members alike.',
                'image_path': 'images/mou1.jpeg'
            },
            {
                'title': 'B.Sc. Agriculture Campus Placement Drive by Nurture Farm',
                'description': 'Haridwar University, Roorkee proudly hosted a Campus Placement Drive by Nurture Farm for B.Sc Agriculture Students offering students a valuable opportunity to begin their professional journey with a global organization. This achievement highlights Haridwar University\'s continuous commitment to enhancing employability, strengthening industry partnerships, and creating impactful career opportunities for its students. Congratulations to all the selected candidates, and best wishes for a successful future ahead!',
                'image_path': 'images/nurture_foundations.jpeg'
            },
            {
                'title': 'Guest Lecture On Entrepreneurship',
                'description': 'Haridwar University, Roorkee is organizing a Guest Lecture on Entrepreneurship under the aegis of the MoU\'s Innovation Cell (Government of India) and the Institution\'s Innovation Council (Ministry of Education Initiative) on 14th February, 2026, from 10:30 AM onwards at the HU Auditorium. The session will feature two distinguished speakers: Abhay Singh, Founder - Topic: "From Student to Startup Founder - Building AgriSaarthi" and Arun Kumar Bhate Co-Founder, AgriSaarthi - Topic: "From Industry to Innovation.',
                'image_path': 'images/gueston14.jpeg'
            }
        ]
        
        for happening_data in happenings_data:
            # Check if this happening already exists
            existing = Happening.query.filter_by(title=happening_data['title']).first()
            if not existing:
                happening = Happening(**happening_data)
                db.session.add(happening)
                print(f"Added: {happening_data['title']}")
            else:
                print(f"Already exists: {happening_data['title']}")
        
        db.session.commit()
        print(f"\nTotal happenings in database: {Happening.query.count()}")

if __name__ == '__main__':
    add_happenings()
