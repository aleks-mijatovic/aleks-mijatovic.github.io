# Aleksandar Mijatović — academic website

A compact, dark static academic website migrated from [Google Sites](https://sites.google.com/view/aleks-mijatovic/home), with a layout inspired by [Martin Hairer's website](https://www.hairer.org/index.html).

**Private draft. Keep this repository private and GitHub Pages disabled until publication is explicitly requested.** A private repository does not by itself make a GitHub Pages website private. GitHub limits private Pages hosting to eligible Enterprise organisation project sites; see [GitHub's access-control documentation](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site).

## Preview

Open `index.html` directly in a browser. All pages, navigation, paper search and topic filters work without a server or installation. You can also run `python3 -m http.server 8000 --bind 127.0.0.1` in this folder and visit `http://127.0.0.1:8000`.

## Contents

- Home: research interests, contact details, portrait and profile links.
- Research: 97 entries — 9 preprints, 79 publications, 2 edited volumes, 2 book chapters, 1 conference proceeding and 4 manuscripts.
- CV: a concise profile based on the supplied short CV, covering appointments, education, leadership, service and supervision; publications link to the Research page.
- Group: five current PhD students with locally stored portraits, plus former postdoctoral researchers and graduated PhD students.
- Videos: 34 videos grouped into 24 paper rows, with all 33 presentation PDFs stored in this repository.

Research supports topic filters, accent-insensitive text search, type filters, newest/oldest/title/topic sorting, result counts, reset and shareable filter URLs. Papers can belong to multiple topics. Sorting by topic groups each paper under its first assigned topic; filtering finds it under any of its topics.

## Editing

The site has no runtime dependencies, analytics, external fonts, build service or deployment workflow. All pages contain their content as HTML and remain readable with JavaScript disabled.

- Change paper titles, authors, years, citations, links and topic assignments in `papers.json`.
- Topic IDs and labels are defined in `topics.json`.
- Update video descriptions, short labels, `paper_id` associations, and local slide filenames in `videos.json`. Original Google Drive addresses are retained as `source_url` provenance only.
- Edit the CV in `cv-content.html` and people, profile links and image filenames in `group.json`. `group-content.html` is the original migration snapshot; it is no longer used to build the page.
- Home text and page structure are in `build.py`. Styling and filtering are in `style.css` and `research.js`.
- After changing data, content or templates, run `python3 build.py` (Python 3.12 or later recommended) and commit the regenerated HTML too. No packages are required.

## Migration notes

Content was retrieved on 15 October 2026 from the five corresponding Google Sites pages. All 33 presentation PDFs were copied from Google Drive into this repository and checked as valid, unencrypted PDFs (1,089 pages in total). The Videos page links to these local files. Paper, publisher, code and YouTube links remain external; the existing Google Drive links for two paper PDFs and four PhD theses are unchanged. The portrait is the image linked by the [Warwick profile](https://warwick.ac.uk/fac/sci/statistics/staff/academic-research/mijatovic/) and hosted by The Alan Turing Institute.

The five current student portraits are stored locally: the first three from the original Group page, and Yuanhe Zhang and Francesco Virgili from their linked university profiles. The source page contains no alumni portraits.

Research rows place authors, arXiv links, linked publication details and descriptive paper-video links together, followed by clickable topic areas. Video and presentation links have hover descriptions distilled from the original Google Sites notes. Alumni names are highlighted as individual headings. Video parts are associated with papers using their titles, matching YouTube links and the title pages of the presentation PDFs.

Topic assignments were added during migration and should be reviewed by the author. `sourceText` in each paper record retains the original citation for reference. Publication years follow the source citations; preprints and manuscripts without a separate year use their arXiv identifier. Existing bibliographic statuses and historical CV details have not been independently updated. The source Group page lists different positions for Miha Brešar in its postdoc and graduate sections; both source entries have been retained for the author to review.

The reference site informed the organisation, typography and navigation. Its code and images were not copied. The original Google Site has not been modified.
