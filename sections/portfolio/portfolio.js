// sections/portfolio/portfolio.js
// JavaScript функциональность для секции "Портфолио"

function initPortfolioFilter() {
    const filterContainer = document.querySelector('.portfolio__filters');
    const filterButtons = filterContainer?.querySelectorAll('.portfolio__filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio__item');
    
    if (!filterContainer || !filterButtons.length) return;
    
    // Инициализация: показать все элементы при загрузке
    portfolioItems.forEach(item => {
        item.classList.remove('hidden');
    });
    
    filterContainer.addEventListener('click', (event) => {
        const targetButton = event.target.closest('.portfolio__filter-btn');
        if (!targetButton || targetButton.classList.contains('active')) return;

        // Обновление активной кнопки
        filterButtons.forEach(button => button.classList.remove('active'));
        targetButton.classList.add('active');

        const filterValue = targetButton.dataset.filter;
        
        // Анимированная фильтрация
        filterPortfolioItems(portfolioItems, filterValue);
    });
}

function filterPortfolioItems(items, filterValue) {
    items.forEach((item, index) => {
        const itemCategory = item.dataset.category;
        const shouldBeVisible = (filterValue === 'all' || itemCategory === filterValue);
        
        // Добавляем задержку для создания волнового эффекта
        setTimeout(() => {
            if (shouldBeVisible) {
                item.classList.remove('hidden');
                // Добавляем анимацию появления
                setTimeout(() => {
                    item.style.transform = 'translateY(0)';
                    item.style.opacity = '1';
                }, 50);
            } else {
                item.classList.add('hidden');
            }
        }, index * 100);
    });
}

// Функция для анимации элементов при прокрутке
function initScrollAnimation() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Наблюдаем за элементами портфолио
    const portfolioItems = document.querySelectorAll('.portfolio__item');
    const filterButtons = document.querySelectorAll('.portfolio__filter-btn');
    const sectionTitle = document.querySelector('.portfolio .section-title');
    
    // Инициальное скрытие элементов для анимации
    portfolioItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        item.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(item);
    });
    
    // Анимация заголовка
    if (sectionTitle) {
        sectionTitle.style.opacity = '0';
        sectionTitle.style.transform = 'translateY(-20px)';
        sectionTitle.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        observer.observe(sectionTitle);
    }
    
    // Анимация кнопок фильтра
    filterButtons.forEach((button, index) => {
        button.style.opacity = '0';
        button.style.transform = 'translateY(-10px)';
        button.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        button.style.transitionDelay = `${0.3 + index * 0.1}s`;
        observer.observe(button);
    });
}

// Функция для подсчета и отображения количества проектов
function updateProjectCount() {
    const filterButtons = document.querySelectorAll('.portfolio__filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio__item');
    
    filterButtons.forEach(button => {
        const filterValue = button.dataset.filter;
        let count = 0;
        
        if (filterValue === 'all') {
            count = portfolioItems.length;
        } else {
            portfolioItems.forEach(item => {
                if (item.dataset.category === filterValue) {
                    count++;
                }
            });
        }
        
        // Добавляем счетчик к тексту кнопки, если его еще нет
        const buttonText = button.textContent.split(' (')[0];
        button.textContent = `${buttonText} (${count})`;
    });
}

// Функция для добавления эффекта параллакса к изображениям
function initParallaxEffect() {
    const portfolioImages = document.querySelectorAll('.portfolio__item-img');
    
    const handleScroll = () => {
        portfolioImages.forEach(img => {
            const rect = img.getBoundingClientRect();
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            if (rect.bottom >= 0 && rect.top <= window.innerHeight) {
                img.style.transform = `translateY(${rate}px)`;
            }
        });
    };
    
    // Throttle scroll event для производительности
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    });
}

// Инициализация всех функций
document.addEventListener('DOMContentLoaded', () => {
    initPortfolioFilter();
    initScrollAnimation();
    updateProjectCount();
    
    // Инициализируем параллакс только на десктопе для лучшей производительности
    if (window.innerWidth > 768) {
        initParallaxEffect();
    }
});

// Экспорт функций для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initPortfolioFilter,
        initScrollAnimation,
        updateProjectCount,
        initParallaxEffect
    };
}