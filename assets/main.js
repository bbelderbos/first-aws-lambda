// handle form submit
$('form').on('submit', (event) => {
  event.preventDefault();
  const prid = document.getElementById('prid').value;
  const payload = { prid: prid };
  grade(payload);
});

// ajax request
function grade(payload) {
  $.ajax({
    method: 'POST',
    url: 'tbd'
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(payload)
  })
  .done((res) => {
    let message = 'Incorrect. Please try again.';
    if (res) {
      message = 'Correct!';
    }
    $('.answer').html(message);
    console.log(res);
    console.log(message);
  })
  .catch((err) => {
    $('.answer').html('Something went terribly wrong!');
    console.log(err);
  });
}
