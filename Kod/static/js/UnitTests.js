//test zmieniania rozmiaru ostatnio zapisanych przepisów

$(document).ready(function(){
        testArray([1,2,3,4,5,6],[2,3,4,5,6]);
        testArray([1,2,3],[1,2,3]);
        testArray(['ala','ma','kota'],['ala','ma','kota']);
        testArray([],[]);
        testArray([1,2,3,4,5,6,7,8,9],[5,6,7,8,9]);
        let result='Spośród '+results.total+' przeprowadzonych testów nie powiodło się '+results.bad+', a powiodło się ' +(results.total-results.bad);
        alert(result);
    });

    var results = {
        total:0,
        bad:0
    };

    function testArray(array,outcome){
        results.total++;
        array=cut(array);
        if (JSON.stringify(array) !== JSON.stringify(outcome)) {
            results.bad++;
        }
    }

//test funkcji convertCookieToArray

$(document).ready(function(){
        testConversion();
    });

function testConversion(){
        testTab([1,2,3]);
        testTab([]);
        testTab(['ala','ma','kota']);
        let result='Spośród '+results.total+' przeprowadzonych testów nie powiodło się '+results.bad+', a powiodło się ' +(results.total-results.bad);
        alert(result);
    }

    function testTab(tabname){
        results.total++;
        $.cookie('tabname', JSON.stringify(tabname));
        let newcookie = $.cookie('tabname');
        let result = convertCookieToArray(newcookie);
        if(JSON.stringify(tabname) !== JSON.stringify(result)) results.bad++;
    }

    function convertCookieToArray(cookie) {
        let result;
        if (typeof cookie !== 'undefined') {
            result = JSON.parse(cookie);
        } else {
            result = [];
        }
        return result;
    }