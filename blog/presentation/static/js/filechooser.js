//

const readURL = (input) => {
    if (!(input.files && input.files[0])) {
        return;
    }
    const reader = new FileReader();
    reader.onload = e => {
        document.getElementById('profile_picture')
            .getElementsByTagName('img')[0]
            .setAttribute('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
}

const activateEditMode = () => {
    [...document.getElementsByClassName('invisible')].forEach(e => {
        e.classList.add('tempclass');
        e.classList.remove('invisible');
    });

    [...document.getElementsByClassName('visible')].forEach(e => {
        e.classList.add('invisible');
        e.classList.remove('visible');
    });

    [...document.getElementsByClassName('tempclass')].forEach(e => {
        e.classList.add('visible');
        e.classList.remove('invisible');
    });
}

const activateConfirmButton = () => {
    document.getElementById('confirm-form').classList.remove('d-none');
}
