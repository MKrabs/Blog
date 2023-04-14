
const input = document.getElementById('id_username');

input.addEventListener("keyup",() => {
    document.getElementById('name').textContent = input.value.padEnd(5,"_");
})
