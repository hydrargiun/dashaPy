function modal(id) {
    var modal = document.getElementById(id);
    var close = document.querySelectorAll('[data-close="true"]');
    modal.style.display = 'block';
    for (var i = 0; i < close.length; i++) {
        close[i].onclick = function () {
            modal.style.display = 'none';
        }
    }
    window.onclick = function (e) {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    };
    document.onkeydown = function (e) {
        if (e.keyCode == 27) {
            modal.style.display = 'none';
        }
    };
}

function close_it(id) {
    var modal = document.getElementById(id);
    modal.style.display = "none";

}
function func_task(day_id, year_id, month_id){
	window.location.href = "/add_task?day_id=" + day_id + "&" + "year_id=" + year_id + "&" +"month_id=" + month_id;
}
function get_task(day_id, year_id, month_id){
	window.location.href = "/get_task?day_id=" + day_id + "&" + "year_id=" + year_id + "&" +"month_id=" + month_id;
}
function move_right(month,year){
    if (month === 12) {
        year = year + 1
        month = 0
    }
	window.location.href = "/?month=" + (month + 1) + "&" + "year=" + year;
}
function move_left(month,year){
    if (month === 1) {
        year = year -1
        month = 13
    }
	window.location.href = "/?month=" + (month - 1) + "&" + "year=" + year;
}
