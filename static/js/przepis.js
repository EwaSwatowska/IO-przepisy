(function () {
    let defaultAmount = [];
    readDefaultAmount();
    let changeAmountBtn = document.querySelector("#changeAmount");
    changeAmountBtn.addEventListener('click', () => {
        let scale = document.querySelector("#numberOfPeople");
        if (scale.value < 1) scale.value = 1;
        changeAmount(scale.value);
    });

    function changeAmount(scale) {
        document.querySelectorAll('amount').forEach((e, i) => {
            e.innerHTML = parseInt(defaultAmount[i]) * scale
        });
    }

    function readDefaultAmount() {
        document.querySelectorAll("amount").forEach((e, i) => {
            defaultAmount[i] = e.innerHTML;
        });
    }
}());