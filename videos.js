(() => {
  const form = document.getElementById('filters');
  const topic = document.getElementById('topic');
  const rows = Array.from(document.querySelectorAll('#videos > tr'));
  const count = document.getElementById('result-count');
  const empty = document.getElementById('empty');

  function render(updateURL = true) {
    let visible = 0;
    rows.forEach(row => {
      row.hidden = topic.value !== 'all' &&
        !row.dataset.topics.split(' ').includes(topic.value);
      if (!row.hidden) visible++;
    });
    count.textContent = `${visible} of ${rows.length} video presentations`;
    empty.hidden = visible > 0;

    if (updateURL && ['http:', 'https:'].includes(location.protocol)) {
      const params = new URLSearchParams(location.search);
      if (topic.value === 'all') params.delete('topic');
      else params.set('topic', topic.value);
      history.replaceState(null, '', location.pathname +
        (params.size ? '?' + params.toString() : '') + location.hash);
    }
  }

  function restore() {
    topic.value = new URLSearchParams(location.search).get('topic') || 'all';
    if (!topic.value) topic.value = 'all';
    render(false);
  }

  form.addEventListener('submit', event => event.preventDefault());
  topic.addEventListener('change', () => render());
  form.addEventListener('reset', event => {
    event.preventDefault();
    topic.value = 'all';
    render();
  });
  window.addEventListener('popstate', restore);
  restore();
})();
