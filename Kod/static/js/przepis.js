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
            e.innerHTML = parseFloat(defaultAmount[i]) * scale
        });
    }

    function readDefaultAmount() {
        document.querySelectorAll("amount").forEach((e, i) => {
            defaultAmount[i] = e.innerHTML;
        });
    }
}());

function convertCookieToArray(cookie) {
    let result;
    if (typeof cookie !== 'undefined') {
        result = JSON.parse(cookie);
    } else {
        result = [];
    }
    return result;
}

function updateMarkInDB(cur_recipe, value, url, voted_recipes) {
    $.ajax({
        url: url,
        data: {recipe_id: cur_recipe, mark: value},
        type: 'GET',
        success: function (data) {
            if (!data['ok']) {
                alert('Wystąpił błąd przy dodawaniu oceny!');
            } else {
                updateVotingCookie(voted_recipes, cur_recipe);
                updateMarkOnPage(data);
            }
        }
    });
}

function updateVotingCookie(voted_recipes, cur_recipe) {
    voted_recipes.push(cur_recipe);
    $.cookie('voted_recipes', JSON.stringify(voted_recipes), {expires: 1000, path: '/'});
}

function updateMarkOnPage(data) {
    $('rate').text(data['rate']);
    $('amount_rates').text(data['amount_of_rates']);
}
