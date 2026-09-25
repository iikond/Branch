// Карта соответствия хэшей и файлов
const routes = {
    '#board': 'pages/board.html',
    '#chats': 'pages/chats.html',
    '#tasks': 'pages/tasks.html',
    '#notes': 'pages/notes.html',
    '#events': 'pages/events.html'
};

const mainContainer = document.getElementById('app-content');
const navLinks = document.querySelectorAll('#nav-menu a');

// Главная функция загрузки страницы
async function loadPage() {
    // Если хэша нет или он неизвестен — открываем доску по умолчанию
    const hash = window.location.hash || '#board';
    const pageUrl = routes[hash] || routes['#board'];

    // Индикация загрузки
    mainContainer.innerHTML = '<div class="loader">Загрузка...</div>';

    try {
        const response = await fetch(pageUrl);
        
        if (!response.ok) {
            throw new Error(`Ошибка загрузки: ${response.status}`);
        }

        const html = await response.text();
        mainContainer.innerHTML = html;

        // Обновляем активную ссылку в сайдбаре
        updateActiveLink(hash);

    } catch (error) {
        console.error(error);
        mainContainer.innerHTML = '<h2>Ошибка 404: Страница не найдена</h2>';
    }
}

// Подсветка активной ссылки в меню
function updateActiveLink(currentHash) {
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentHash) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Слушаем изменения хэша в URL (при кликах по меню)
window.addEventListener('hashchange', loadPage);

// Загружаем начальную страницу при запуске
window.addEventListener('DOMContentLoaded', loadPage);