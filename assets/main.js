// handle form submit
$('form').on('submit', (event) => {
  event.preventDefault();
  const prid = document.getElementById('prid').value;
  const payload = { prid: prid };
  grade(payload);
});

// https://gist.github.com/thiagodebastos/08ea551b97892d585f17
var mydata = JSON.parse(data);
var url = mydata[0].api_url

// ajax request
function grade(payload) {
  $.ajax({
    method: 'POST',
    url: url,
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(payload)
  })
  .done((res) => {
    if (res === 'ok') {
      $('.answer').html('All files PEP8 compliant').addClass('ok');
    } else {
      $('.answer').html('PEP8 errors: <pre>' + res.join("\n") + '</pre>').addClass('err');
    }
    console.log(res);
  })
  .catch((err) => {
    $('.answer').html('Something went terribly wrong!');
    console.log(err);
  });
}
