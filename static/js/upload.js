let main_element = document.getElementById('photo-input');
let input_text = document.getElementById('photo-input-text');

main_element.addEventListener('change', function () {
    let countFiles = '';

    if (this.files && this.files.length >= 1)
        countFiles = this.files.length;
        input_text.innerText = `Выбрано файлов: ${countFiles}`
});
