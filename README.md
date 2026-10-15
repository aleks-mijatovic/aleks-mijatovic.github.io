# Aleksandar Mijatović — academic website

A static academic website migrated from [Google Sites](https://sites.google.com/view/aleks-mijatovic/home), with a layout inspired by [Martin Hairer's website](https://www.hairer.org/index.html).

**Private draft. Keep this repository private and GitHub Pages disabled until publication is explicitly requested.** A private repository does not by itself make a GitHub Pages website private. GitHub limits private Pages hosting to eligible Enterprise organisation project sites; see [GitHub's access-control documentation](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site).

## Preview

Open `index.html` directly in a browser. All pages, navigation, paper search and topic filters work without a server or installation. You can also run `python3 -m http.server 8000 --bind 127.0.0.1` in this folder and visit `http://127.0.0.1:8000`.

## Contents

- Home: research interests, contact details, portrait and profile links.
- Research: 97 entries — 9 preprints, 79 publications, 2 edited volumes, 2 book chapters, 1 conference proceeding and 4 manuscripts.
- CV: the education, employment, teaching, talks, lecture courses and professional activities from the source site.
- Group: current PhD students, former postdoctoral researchers and graduated PhD students.
- Videos: 34 videos with 33 accompanying slide links.

Research supports topic filters, accent-insensitive text search, type filters, newest/oldest/title/topic sorting, result counts, reset and shareable filter URLs. Papers can belong to multiple topics. Sorting by topic groups each paper under its first assigned topic; filtering finds it under any of its topics.

## Editing

The site has no runtime dependencies, analytics, external fonts, build service or deployment workflow. All pages contain their content as HTML and remain readable with JavaScript disabled.

- Change paper titles, authors, years, citations, links and topic assignments in `papers.json`.
- Topic IDs and labels are defined in `topics.json`.
- Update videos and slide links in `videos.json`.
- Edit the CV and group content in `cv-content.html` and `group-content.html`.
- Home text and page structure are in `build.py`. Styling and filtering are in `style.css` and `research.js`.
- After changing data, content or templates, run `python3 build.py` (Python 3.12 or later recommended) and commit the regenerated HTML too. No packages are required.

## Migration notes

Content was retrieved on 15 October 2026 from the five corresponding Google Sites pages. Existing paper, publisher, code, YouTube and Google Drive links were retained as external destinations; linked PDFs and slide files are not copied into this repository. The portrait is the image linked by the [Warwick profile](https://warwick.ac.uk/fac/sci/statistics/staff/academic-research/mijatovic/) and hosted by The Alan Turing Institute.

Topic assignments were added during migration and should be reviewed by the author. `sourceText` in each paper record retains the original citation for reference. Publication years follow the source citations; preprints and manuscripts without a separate year use their arXiv identifier. Existing bibliographic statuses and historical CV details have not been independently updated. The source Group page lists different positions for Miha Brešar in its postdoc and graduate sections; both source entries have been retained for the author to review.

The reference site informed the organisation, typography and navigation. Its code and images were not copied. The original Google Site has not been modified.
