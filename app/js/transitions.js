//SEDES
document.querySelector('.go-sedes').addEventListener ('click', function () {
  document.querySelector('#sedes').className = 'current';
  document.querySelector('[data-position="current"]').className = 'left';
});
document.querySelector('.back-sedes').addEventListener ('click', function () {
  document.querySelector('#sedes').className = 'right';
  document.querySelector('[data-position="current"]').className = 'current';
});



