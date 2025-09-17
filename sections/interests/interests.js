// sections/interests/interests.js
// JavaScript функциональность для секции "Интересы"
/* Функция открытия окна */
const closeButtons = document.querySelectorAll('.interests_close-button');
  closeButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      const dialog = button.closest('dialog');
      if (!dialog) return;

      dialog.classList.add('closing');
      setTimeout(() => {
        dialog.close();
        dialog.classList.remove('closing');
      }, 300);
    });
  });