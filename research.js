(() => {
  const form = document.getElementById('filters');
  const query = document.getElementById('query');
  const section = document.getElementById('section');
  const sort = document.getElementById('sort');
  const topic = document.getElementById('topic');
  const list = document.getElementById('papers');
  const order = ['Preprints', 'Publications', 'Edited volumes', 'Book chapters', 'Conference proceedings', 'Manuscripts'];
  const names = {Publications: 'Published & accepted papers', Manuscripts: 'Unpublished manuscripts'};
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const records = Array.from(list.querySelectorAll('.paper')).map((el, index) => ({
    el, index, year: Number(el.dataset.year), section: el.dataset.section,
    topics: el.dataset.topics.split(' '), primary: el.dataset.primaryTopic,
    title: el.querySelector('h3').textContent,
    text: normalize(el.textContent + ' ' + el.dataset.topicNames)
  }));
  const slug = text => text.toLowerCase().replaceAll(' ', '-');

  function render(updateURL = true) {
    const words = normalize(query.value).trim().split(/\s+/).filter(Boolean);
    const visible = records.filter(p =>
      (topic.value === 'all' || p.topics.includes(topic.value)) &&
      (section.value === 'all' || p.section === section.value) &&
      words.every(w => p.text.includes(w)));
    const groups = document.createDocumentFragment();
    for (const kind of order) {
      const entries = visible.filter(p => p.section === kind);
      if (!entries.length) continue;
      // Earlier manuscripts retain their source order and carry no date labels.
      if (kind !== 'Manuscripts') entries.sort((a, b) => {
        if (sort.value === 'title') return a.title.localeCompare(b.title);
        if (sort.value === 'topic') return a.primary.localeCompare(b.primary) || b.year - a.year || a.index - b.index;
        return (sort.value === 'oldest' ? a.year - b.year : b.year - a.year) || a.index - b.index;
      });
      const group = document.createElement('section');
      group.className = 'research-section';
      group.id = slug(kind);
      group.dataset.section = kind;
      const heading = document.createElement('h2');
      heading.append(names[kind] || kind);
      const count = document.createElement('small');
      count.textContent = entries.length;
      heading.append(count);
      group.append(heading);
      let previousTopic;
      for (const p of entries) {
        if (sort.value === 'topic' && kind !== 'Manuscripts' && previousTopic !== p.primary) {
          const subheading = document.createElement('h3');
          subheading.className = 'group-heading';
          subheading.textContent = p.primary;
          group.append(subheading);
          previousTopic = p.primary;
        }
        group.append(p.el);
      }
      groups.append(group);
    }
    list.replaceChildren(groups);
    document.getElementById('result-count').textContent = `${visible.length} of ${records.length} research entries`;
    document.getElementById('empty').hidden = visible.length > 0;
    if (updateURL && ['http:', 'https:'].includes(location.protocol)) {
      const params = new URLSearchParams();
      if (topic.value !== 'all') params.set('topic', topic.value);
      if (query.value.trim()) params.set('q', query.value.trim());
      if (section.value !== 'all') params.set('type', section.value);
      if (sort.value !== 'newest') params.set('sort', sort.value);
      history.replaceState(null, '', location.pathname + (params.size ? '?' + params.toString() : '') + location.hash);
    }
  }
  function restore() {
    const params = new URLSearchParams(location.search);
    query.value = params.get('q') || '';
    for (const [control, key, fallback] of [[section, 'type', 'all'], [topic, 'topic', 'all'], [sort, 'sort', 'newest']]) {
      control.value = params.get(key) || fallback;
      if (!control.value) control.value = fallback;
    }
    render(false);
  }
  form.addEventListener('submit', event => event.preventDefault());
  [topic, section, sort].forEach(control => control.addEventListener('change', () => render()));
  query.addEventListener('input', () => render());
  form.addEventListener('reset', event => {
    event.preventDefault();
    query.value = ''; topic.value = 'all'; section.value = 'all'; sort.value = 'newest';
    render();
  });
  window.addEventListener('popstate', restore);
  restore();
})();
