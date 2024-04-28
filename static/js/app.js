const menuBtn = document.getElementById('menu-btn');
const sideBar = document.getElementById('side-bar');
const scrim = document.getElementById('scrim');
if(menuBtn){
  menuBtn.addEventListener('click', ()=>{
    sideBar.classList.toggle('active');
  })
}

if(scrim){
  scrim.addEventListener('click', ()=>{
    sideBar.classList.remove('active');
  })
}

const menuLinks = document.querySelectorAll('.menu-links a');

const currentURL = new URL(window.location.href);

menuLinks.forEach(link => {
  const linkURL = new URL(link.href);
  
  if (linkURL.pathname === currentURL.pathname) {
    link.classList.add('active');
  } else {
    link.classList.remove('active');
  }
});