// Inicializa el carrusel de la seccion galeria cuando el DOM esta listo.
document.addEventListener("DOMContentLoaded", () => {
	const track = document.querySelector(".carousel__track");
	const slides = Array.from(document.querySelectorAll(".carousel__slide"));
	const dots = Array.from(document.querySelectorAll(".carousel__dot"));
	const prevButton = document.querySelector(".carousel__control--prev");
	const nextButton = document.querySelector(".carousel__control--next");

	if (!track || slides.length === 0 || dots.length !== slides.length || !prevButton || !nextButton) {
		return;
	}

	let currentIndex = 0;

	// Actualiza posicion, estados activos y atributos ARIA en cada cambio.
	const renderCarousel = () => {
		track.style.transform = `translateX(-${currentIndex * 100}%)`;

		slides.forEach((slide, index) => {
			slide.classList.toggle("is-active", index === currentIndex);
		});

		dots.forEach((dot, index) => {
			const isSelected = index === currentIndex;
			dot.classList.toggle("is-active", isSelected);
			dot.setAttribute("aria-selected", String(isSelected));
			dot.setAttribute("tabindex", isSelected ? "0" : "-1");
		});
	};

	// Mueve el carrusel en sentido circular hacia atras o adelante.
	const moveBy = (step) => {
		const total = slides.length;
		currentIndex = (currentIndex + step + total) % total;
		renderCarousel();
	};

	prevButton.addEventListener("click", () => moveBy(-1));
	nextButton.addEventListener("click", () => moveBy(1));

	dots.forEach((dot, index) => {
		dot.addEventListener("click", () => {
			currentIndex = index;
			renderCarousel();
		});

		// Permite navegar con flechas para mejorar accesibilidad de teclado.
		dot.addEventListener("keydown", (event) => {
			if (event.key === "ArrowRight") {
				event.preventDefault();
				moveBy(1);
			}

			if (event.key === "ArrowLeft") {
				event.preventDefault();
				moveBy(-1);
			}
		});
	});

	renderCarousel();
});
