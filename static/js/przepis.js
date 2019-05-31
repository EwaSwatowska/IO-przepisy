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

function convertCookieToArray(cookie) {
    var result;
    if (typeof cookie !== 'undefined') {
        result = JSON.parse(cookie);
    } else {
        result = [];
    }
    return result;
}

function updateMark(cur_recipe, value, url) {
    $.ajax({
        url: url,
        data: {recipe_id: cur_recipe, mark: value},
        type: 'GET',
        success: function (data) {
            if (data['ok']) {
                voted_recipes.push(cur_recipe);
                $.cookie('voted_recipes', JSON.stringify(voted_recipes), {expires: 1000});
            } else {
                alert('Wystąpił błąd przy dodawaniu oceny!');
            }
        }
    });
}
