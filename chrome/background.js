chrome.webNavigation.onCommitted.addListener(function(data){
  data.event_type = 'onCommitted'
  fetch('http://localhost:8080/event', {
    method: 'POST',
    body: JSON.stringify(data)
  }).then(res => {
    console.log(res);
  }).catch(err => console.log(err))
});
