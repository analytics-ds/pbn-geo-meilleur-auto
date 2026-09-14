const toggle = document.querySelector('.menu-toggle');
const mobile = document.querySelector('#mobile-nav');
const disclosures = [...document.querySelectorAll('.mega-menu')];
function closeTopics() { disclosures.forEach(menu => { menu.open = false; }); }
function closeMobile() {
  if (!toggle || !mobile) return;
  toggle.setAttribute('aria-expanded', 'false');
  mobile.hidden = true;
  closeTopics();
}
if (toggle && mobile) {
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    mobile.hidden = open;
    if (open) closeTopics();
  });
  mobile.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMobile));
  matchMedia('(min-width: 1051px)').addEventListener('change', closeMobile);
}
disclosures.forEach(menu => {
  menu.addEventListener('toggle', () => {
    if (menu.open) disclosures.forEach(other => { if (other !== menu) other.open = false; });
  });
  menu.addEventListener('focusout', event => {
    if (event.relatedTarget && !menu.contains(event.relatedTarget)) menu.open = false;
  });
});
document.addEventListener('click', event => {
  disclosures.forEach(menu => { if (!menu.contains(event.target)) menu.open = false; });
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const open = disclosures.find(menu => menu.open);
  if (open) { open.open = false; open.querySelector('summary').focus(); }
  else if (toggle && toggle.getAttribute('aria-expanded') === 'true') { closeMobile(); toggle.focus(); }
});
