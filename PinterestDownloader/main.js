// var a = document.getElementsByClassName('pinImageWrapper draggable');

// for (var i in a) {
//     console.log(a[i].href);
// }


var a = document.getElementsByClassName('pinHolder');

for (var i in a) {
    if (a[i].appendChild) {
		var d = document.createElement('button');
		d.innerHTML = "<strong>Привет, Настя!</strong>";
        a[i].appendChild(d);
    }
}
