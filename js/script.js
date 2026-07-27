// লাইভ সার্চ (হোমপেজে)
(function(){
  const input = document.getElementById('searchInput');
  if(!input) return;
  const cards = Array.from(document.querySelectorAll('[data-card]'));
  const emptyState = document.getElementById('emptyState');

  input.addEventListener('input', function(){
    const q = input.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach(function(card){
      const haystack = card.getAttribute('data-search');
      const match = !q || haystack.includes(q);
      card.style.display = match ? '' : 'none';
      if(match) visible++;
    });
    if(emptyState) emptyState.style.display = visible === 0 ? 'block' : 'none';
  });
})();

// ট্যাগ ফিল্টার
(function(){
  const tagLinks = document.querySelectorAll('[data-tag-filter]');
  const cards = Array.from(document.querySelectorAll('[data-card]'));
  if(!tagLinks.length) return;
  tagLinks.forEach(function(link){
    link.addEventListener('click', function(e){
      e.preventDefault();
      const tag = link.getAttribute('data-tag-filter');
      cards.forEach(function(card){
        const tags = card.getAttribute('data-tags') || '';
        card.style.display = (tag === 'all' || tags.includes(tag)) ? '' : 'none';
      });
      const input = document.getElementById('searchInput');
      if(input) input.value = '';
    });
  });
})();

// পড়ার প্রগ্রেস বার (পোস্ট পাতায়)
(function(){
  const bar = document.getElementById('progressBar');
  if(!bar) return;
  window.addEventListener('scroll', function(){
    const h = document.documentElement;
    const scrolled = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
    bar.style.width = scrolled + '%';
  });
})();

// লিংক কপি করে শেয়ার
(function(){
  const btn = document.getElementById('copyLinkBtn');
  if(!btn) return;
  btn.addEventListener('click', function(){
    navigator.clipboard.writeText(window.location.href).then(function(){
      const original = btn.textContent;
      btn.textContent = 'লিংক কপি হয়েছে ✓';
      setTimeout(function(){ btn.textContent = original; }, 1800);
    });
  });
})();
