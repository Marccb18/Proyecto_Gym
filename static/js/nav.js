window.addEventListener('scroll', function() {
    const header = document.querySelector('#header');
    header.classList.toggle('shrink', window.scrollY > 0);
});