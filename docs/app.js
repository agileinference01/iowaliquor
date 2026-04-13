const data = window.DOC_DATA;
const results = document.getElementById('results');
const search = document.getElementById('search');

function render(items) {
  results.innerHTML = '';
  if (!items.length) {
    results.innerHTML = '<p>No results found.</p>';
    return;
  }
  for (const item of items) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div class="title">${item.name}</div>
      <div class="type">${item.type} ${item.table ? 'in <b>' + item.table + '</b>' : ''}</div>
      <div class="formula"><pre>${item.formula}</pre></div>
      <div class="desc">${item.description || '<em>No description provided.</em>'}</div>
    `;
    results.appendChild(card);
  }
}

function filter(q) {
  q = q.trim().toLowerCase();
  if (!q) return data;
  return data.filter(item =>
    item.name.toLowerCase().includes(q) ||
    (item.description && item.description.toLowerCase().includes(q)) ||
    (item.formula && item.formula.toLowerCase().includes(q)) ||
    (item.table && item.table.toLowerCase().includes(q))
  );
}

search.addEventListener('input', e => {
  render(filter(e.target.value));
});

render(data);
