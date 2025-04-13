document.addEventListener('DOMContentLoaded', function() {
    const commonConfig = {
        allowInput: true,
        dateFormat: "Y-m-d",
        animate: true,
        disableMobile: "auto",
        prevArrow: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M10 12L6 8L10 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`,
        nextArrow: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 12L10 8L6 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`,
    };

    // Date picker configuration
    const datePicker = flatpickr("#birthdate", {
        ...commonConfig,
        maxDate: "today",
        monthSelectorType: "static",
        yearSelectorType: "dropdown"
    });

    // Time picker configuration
    const timePicker = flatpickr("#birthtime", {
        ...commonConfig,
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        defaultHour: 1,
        minuteIncrement: 5
    });

    // Make icons clickable
    document.querySelectorAll('.input-wrap').forEach(wrap => {
        const input = wrap.querySelector('input');
        const icon = wrap.querySelector('.input-icon');
        
        if (icon) {
            icon.style.pointerEvents = 'auto';
            icon.style.cursor = 'pointer';
            
            icon.addEventListener('click', () => {
                if (input.id === 'birthdate') {
                    datePicker.open();
                } else if (input.id === 'birthtime') {
                    timePicker.open();
                }
            });
        }
    });

    // History dropdown functionality
    const historyToggle = document.querySelector('.history-toggle');
    if (historyToggle) {
        historyToggle.setAttribute('aria-expanded', 'false');
        const historyContent = document.querySelector('.history-content');
        
        historyToggle.addEventListener('click', () => {
            const isExpanded = historyToggle.getAttribute('aria-expanded') === 'true';
            historyToggle.setAttribute('aria-expanded', !isExpanded);
            historyContent.classList.toggle('show');
        });
    }
});