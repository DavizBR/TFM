const carouselContainer = document.querySelector('.carousel-container');
const prevButton = document.getElementById('prevBtn');
const nextButton = document.getElementById('nextBtn');
const slides = document.querySelectorAll('.carousel-slide');
let currentIndex = 0;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.transform = `translateX(${100 * (i - index)}%)`;
    });
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
}

nextButton.addEventListener('click', nextSlide);

function autoSlide() {
    nextSlide();
    setTimeout(autoSlide, 3000); // Change slide every 3 seconds (adjust as needed)
}

autoSlide();

showSlide(currentIndex);
