// Dropdown toggle function for weather dashboard
function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close dropdown when clicking outside
window.onclick = function(event) {
    if (!event.target.matches('.modern-dropdown-btn')) {
        var dropdowns = document.getElementsByClassName("modern-dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
