// State management
let currentDate = null;
let availableDates = [];

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await loadAvailableDates();
    await loadTodayArticles();
});

// Load available dates
async function loadAvailableDates() {
    try {
        const response = await fetch('/api/available-dates');
        const data = await response.json();
        availableDates = data.dates;

        // Always include today if not in list
        const today = new Date().toISOString().split('T')[0];
        if (!availableDates.includes(today)) {
            availableDates.unshift(today);
        }

        renderDateTabs();
    } catch (error) {
        console.error('Error loading dates:', error);
    }
}

// Render date tabs
function renderDateTabs() {
    const tabsContainer = document.getElementById('dateTabs');
    tabsContainer.innerHTML = '';

    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

    availableDates.slice(0, 10).forEach((dateStr, index) => {
        const tab = document.createElement('div');
        tab.className = 'date-tab';

        // Format label
        let label;
        if (dateStr === today) {
            label = 'Today';
        } else if (dateStr === yesterday) {
            label = 'Yesterday';
        } else {
            const date = new Date(dateStr + 'T00:00:00');
            label = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }

        tab.textContent = label;
        tab.dataset.date = dateStr;

        // Set active state
        if (dateStr === currentDate) {
            tab.classList.add('active');
        }

        tab.addEventListener('click', () => loadArticles(dateStr));
        tabsContainer.appendChild(tab);
    });
}

// Load today's articles
async function loadTodayArticles() {
    const today = new Date().toISOString().split('T')[0];
    await loadArticles(today);
}

// Load articles for a specific date
async function loadArticles(dateStr) {
    const grid = document.getElementById('newsGrid');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');

    // Update state
    currentDate = dateStr;

    // Show loading
    grid.innerHTML = '';
    loading.style.display = 'block';
    error.style.display = 'none';

    // Update active tab
    document.querySelectorAll('.date-tab').forEach(tab => {
        if (tab.dataset.date === dateStr) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    try {
        const response = await fetch(`/api/articles/${dateStr}`);

        if (!response.ok) {
            throw new Error('Failed to load articles');
        }

        const data = await response.json();
        renderArticles(data.articles);
        loading.style.display = 'none';
    } catch (err) {
        console.error('Error loading articles:', err);
        loading.style.display = 'none';
        error.style.display = 'block';
    }
}

// Render articles as tiles
function renderArticles(articles) {
    const grid = document.getElementById('newsGrid');
    grid.innerHTML = '';

    articles.forEach((article, index) => {
        const tile = document.createElement('div');
        tile.className = 'news-tile';
        tile.style.animationDelay = `${index * 0.05}s`;

        // Determine source color class
        const sourceClass = getSourceClass(article.source_name);

        // Format date
        const publishedDate = new Date(article.published_date);
        const timeAgo = getTimeAgo(publishedDate);

        tile.innerHTML = `
            <div>
                <div class="source-badge ${sourceClass}">
                    ${article.source_name}
                </div>
                <div class="title">${escapeHtml(article.title)}</div>
                <div class="summary">${escapeHtml(article.summary || article.description || '')}</div>
            </div>
            <div class="meta">
                <span>${timeAgo}</span>
                <span class="score">Score: ${article.score.toFixed(1)}</span>
            </div>
        `;

        tile.addEventListener('click', () => {
            window.open(article.url, '_blank');
        });

        grid.appendChild(tile);
    });
}

// Get source color class
function getSourceClass(sourceName) {
    const sourceMap = {
        'Industrial AI Podcast': 'source-industrial-ai',
        'IoT Use Case Podcast': 'source-iot-usecase',
        'Hugging Face Daily Papers': 'source-huggingface',
        'Doppelgänger Tech Talk': 'source-doppelganger',
        'Super Data Science': 'source-super-data',
        'Exponential Industry': 'source-exponential',
        'The Sequence': 'source-sequence',
        'Hacker News': 'source-hackernews',
        'Where\'s Your Ed At': 'source-wheres-ed',
        'Manufacturing Happy Hour': 'source-manufacturing'
    };

    return sourceMap[sourceName] || 'source-default';
}

// Get time ago string
function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);

    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };

    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
        }
    }

    return 'Just now';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
