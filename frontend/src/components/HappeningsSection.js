import React, { useRef } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Autoplay } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import './HappeningsSection.css';

function HappeningsSection({ happenings }) {
  const swiperRef = useRef(null);

  const defaultHappenings = [
    {
      id: 1,
      title: 'Campus Placement Drive by ROVO AUTOMATIONS',
      description: 'Haridwar University, Roorkee proudly hosted a Campus Placement Drive by ROVO Automation offering students a valuable opportunity to begin their professional journey with a global organization. The recruitment process witnessed enthusiastic participation from students across various disciplines.',
      image_path: 'images/mou1.jpeg'
    },
    {
      id: 2,
      title: 'Memorandum of Understanding (MoU) with IIT Roorkee',
      description: 'A significant milestone was achieved as the Indian Institute of Technology (IIT) Roorkee and Haridwar University, Roorkee formalized their collaboration through the signing of a Memorandum of Understanding (MoU). This strategic partnership aims to strengthen academic cooperation, promote research and innovation, and create opportunities for knowledge exchange between the two esteemed institutions. The MoU is expected to facilitate collaborative research projects, expert lectures, skill development programs, internships, and other academic initiatives that will benefit students and faculty members alike.',
      image_path: 'images/mou2.jpeg'
    },
    {
      id: 3,
      title: 'B.Sc. Agriculture Campus Placement Drive by Nurture Farm',
      description: 'Haridwar University, Roorkee proudly hosted a Campus Placement Drive by Nurture Farm for B.Sc. Agriculture Students offering students a valuable opportunity to begin their professional journey with a global organization. This achievement highlights Haridwar University\'s continuous commitment to enhancing employability, strengthening industry partnerships, and creating impactful career opportunities for its students. Congratulations to all the selected candidates, and best wishes for a successful future ahead!',
      image_path: 'images/mou3.jpeg'
    }
  ];

  const displayHappenings = Array.isArray(happenings) && happenings.length > 0 ? happenings : defaultHappenings;

  return (
    <section className="happenings-section">
      <div className="happenings-container">
        <h2>HAPPENINGS AT HARIDWAR UNIVERSITY</h2>
        <Swiper
          ref={swiperRef}
          modules={[Navigation, Autoplay]}
          spaceBetween={24}
          slidesPerView={1}
          loop={true}
          autoplay={{ delay: 5000, disableOnInteraction: false }}
          breakpoints={{
            640: { slidesPerView: 2 },
            1024: { slidesPerView: 3 }
          }}
          className="happenings-swiper"
        >
          {displayHappenings.map((happening) => (
            <SwiperSlide key={happening.id}>
              <div className="happening-card">
                <img src={`/${happening.image_path}`} alt={happening.title} />
                <div className="happening-content">
                  <h3>{happening.title}</h3>
                  <p>{happening.description}</p>
                </div>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
        <div className="swiper-navigation">
          <button onClick={() => swiperRef.current?.swiper.slidePrev()}>←</button>
          <button onClick={() => swiperRef.current?.swiper.slideNext()}>→</button>
        </div>
      </div>
    </section>
  );
}

export default HappeningsSection;
