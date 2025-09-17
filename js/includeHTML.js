/* Функция для подключения HTML - файлов */
function includeHTML() {
  var z, i, elmnt, file, xhttp;
  /* Проходим по всем HTML элементам: */
  z = document.getElementsByTagName("*");
  for (i = 0; i < z.length; i++) {
    elmnt = z[i];
    /* ищем элементы с определенным атрибутом: */
    file = elmnt.getAttribute("include-html");
    if (file) {
      /* Делаем HTTP запрос, используя значение атрибута в качестве имени файла: */
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
          if (this.status == 200) {elmnt.innerHTML = this.responseText;}
          if (this.status == 404) {elmnt.innerHTML = "Страница не найдена.";}
          /* Удаляем атрибут и вызываем функцию еще раз: */
          elmnt.removeAttribute("include-html");
          includeHTML();
        }
      }
      xhttp.open("GET", file, true);
      xhttp.send();
      /* Выходим из функции: */
      return;
    }
  }
}