(() => {
  const form = document.getElementById('filters');
  const query = document.getElementById('query');
  const section = document.getElementById('section');
  const sort = document.getElementById('sort');
  const list = document.getElementById('papers');
  const papers = Array.from(list.querySelectorAll('.paper'));
  const topicSelect = document.getElementById('topic');
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const records = papers.map((el, index) => ({el, index, year: Number(el.dataset.year), section: el.dataset.section,
    topics: el.dataset.topics.split(' '), text: normalize(el.textContent + ' ' + el.dataset.topicNames), title: el.querySelector('h3').textContent,
    topic: el.dataset.primaryTopic}));
  let topic = 'all';
  function restore() {
    const params = new URLSearchParams(location.search);
    query.value = params.get('q') || '';
    section.value = params.get('type') || 'all';
    if (!section.value) section.value = 'all';
    sort.value = params.get('sort') || 'newest';
    if (!sort.value) sort.value = 'newest';
    topicSelect.value = params.get('topic') || 'all';
    if (!topicSelect.value) topicSelect.value = 'all';
    topic = topicSelect.value;
    render(false);
  }
  function render(updateURL = true) {
    const words = normalize(query.value).trim().split(/\s+/).filter(Boolean);
    const visible = records.filter(p => (topic === 'all' || p.topics.includes(topic)) &&
      (section.value === 'all' || p.section === section.value) && words.every(w => p.text.includes(w)));
    visible.sort((a,b) => {
      if (sort.value === 'title') return a.title.localeCompare(b.title);
      if (sort.value === 'topic') return a.topic.localeCompare(b.topic) || b.year-a.year || a.index-b.index;
      return (sort.value === 'oldest' ? a.year-b.year : b.year-a.year) || a.index-b.index;
    });
    list.querySelectorAll('.group-heading').forEach(el => el.remove());
    records.forEach(p => { p.el.hidden = true; });
    let previousTopic;
    visible.forEach(p => {
      if (sort.value === 'topic' && p.topic !== previousTopic) {
        const heading = document.createElement('h2');
        heading.className = 'group-heading';
        heading.textContent = p.topic;
        list.append(heading);
        previousTopic = p.topic;
      }
      p.el.hidden = false;
      list.append(p.el);
    });
    topicSelect.value = topic;
    document.getElementById('result-count').textContent = `${visible.length} of ${records.length} research entries`;
    document.getElementById('empty').hidden = visible.length > 0;
    if (updateURL && ['http:', 'https:'].includes(location.protocol)) {
      const params = new URLSearchParams();
      if (topic !== 'all') params.set('topic', topic);
      if (query.value.trim()) params.set('q', query.value.trim());
      if (section.value !== 'all') params.set('type', section.value);
      if (sort.value !== 'newest') params.set('sort', sort.value);
      history.replaceState(null, '', location.pathname + (params.size ? '?' + params.toString() : '') + location.hash);
    }
  }
  form.addEventListener('submit', e => e.preventDefault());
  query.addEventListener('input', () => render());
  section.addEventListener('change', () => render());
  sort.addEventListener('change', () => render());
  topicSelect.addEventListener('change', () => { topic = topicSelect.value; render(); });
  form.addEventListener('reset', () => { query.value = ''; section.value = 'all'; sort.value = 'newest'; topic = 'all'; render(); });
  window.addEventListener('popstate', restore);
  restore();
})();
