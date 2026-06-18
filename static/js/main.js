document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const wrapper = document.querySelector('.wrapper');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            wrapper.classList.toggle('sidebar-collapsed');
        });
    }
});
