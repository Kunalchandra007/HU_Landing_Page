import React, { useRef } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, Navigation, Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import './AlumniCorner.css';

function AlumniCorner() {
  const swiperRef = useRef(null);

  const alumniData = [
    {
      id: 1,
      name: "Rajesh Kumar",
      batch: "2018-2022",
      position: "Software Engineer at Google",
      image: "/images/logo.jpeg",
      quote: "Haridwar University shaped my career and gave me the foundation to succeed in the tech industry."
    },
    {
      id: 2,
      name: "Priya Sharma",
      batch: "2017-2021",
      position: "Data Scientist at Microsoft",
      image: "/images/logo.jpeg",
      quote: "The faculty and infrastructure at HU provided me with world-class education and opportunities."
    },
    {
      id: 3,
      name: "Amit Verma",
      batch: "2019-2023",
      position: "Product Manager at Amazon",
      image: "/images/logo.jpeg",
      quote: "My journey at Haridwar University was transformative. The skills I learned here are invaluable."
    },
    {
      id: 4,
      name: "Sneha Patel",
      batch: "2016-2020",
      position: "Business Analyst at Deloitte",
      image: "/images/logo.jpeg",
      quote: "HU not only provided excellent academics but also helped me develop leadership and soft skills."
    },
    {
      id: 5,
      name: "Vikram Singh",
      batch: "2018-2022",
      position: "Full Stack Developer at Flipkart",
      image: "/images/logo.jpeg",
      quote: "The placement support and industry exposure at Haridwar University is unmatched."
    }
  ];

  return (
    <section className="alumni-corner">
      <div className="alumni-container">
        <div className="alumni-header">
          <h2 className="alumni-title">
            <span className="title-icon">🎓</span>
            Alumni Corner
          </h2>
          <p className="alumni-subtitle">Hear from our successful graduates</p>
        </div>

        <div className="alumni-swiper-wrapper">
          <Swiper
            ref={swiperRef}
            modules={[Autoplay, Navigation, Pagination]}
            spaceBetween={30}
            slidesPerView={1}
            autoplay={{
              delay: 3000,
              disableOnInteraction: false,
            }}
            navigation={{
              nextEl: '.alumni-button-next',
              prevEl: '.alumni-button-prev',
            }}
            pagination={{
              clickable: true,
              dynamicBullets: true,
            }}
            loop={true}
            speed={800}
            breakpoints={{
              640: {
                slidesPerView: 1,
              },
              768: {
                slidesPerView: 2,
              },
              1024: {
                slidesPerView: 3,
              },
            }}
            className="alumni-swiper"
          >
            {alumniData.map((alumni) => (
              <SwiperSlide key={alumni.id}>
                <div className="alumni-card">
                  <div className="alumni-card-header">
                    <div className="alumni-image-wrapper">
                      <img src={alumni.image} alt={alumni.name} className="alumni-image" />
                    </div>
                    <div className="alumni-info">
                      <h3 className="alumni-name">{alumni.name}</h3>
                      <p className="alumni-batch">{alumni.batch}</p>
                    </div>
                  </div>
                  <div className="alumni-card-body">
                    <p className="alumni-position">{alumni.position}</p>
                    <div className="quote-icon">"</div>
                    <p className="alumni-quote">{alumni.quote}</p>
                  </div>
                </div>
              </SwiperSlide>
            ))}
          </Swiper>

          {/* Custom Navigation Buttons */}
          <div className="alumni-navigation">
            <button className="alumni-button-prev" aria-label="Previous alumni">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <button className="alumni-button-next" aria-label="Next alumni">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export default AlumniCorner;
