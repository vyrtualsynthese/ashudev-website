require('normalize.css/normalize.css')
require('./css/materialize.css')
require('./css/all.css')
require('./css/style.css')

const img = require('./img/profile.jpg');

const app = document.querySelectorAll('.avatar')

app.forEach(element => {
  const avatar = document.createElement('img')
  avatar.src = img
  avatar.classList.add('responsive-img', 'z-depth-1');
  avatar.alt = 'Valentin RONTEIX';
  element.append(avatar)
})
console.log(app)
