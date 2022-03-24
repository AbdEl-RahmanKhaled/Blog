set_new_pass = document.getElementById('set_new_pass');
set_new_confirm_pass = document.getElementById('set_new_confirm_pass');
btn_set_new_pass = document.getElementById('btn_set_new_pass');


function is_valid() {
    let pass1 = set_new_pass.value;
    let pass2 = set_new_confirm_pass.value;
    return pass1 === pass2
}

btn_set_new_pass.addEventListener('click', function (e) {
    if (!is_valid()) {
        e.preventDefault();
    }
});