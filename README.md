# Dr. Saurabh Shukla - academic website

The site is built from LaTeX files. Edit a file in `content/`, commit, and the site
rebuilds itself in about a minute. No HTML needed.

## One-time setup on GitHub
1. Upload everything in this folder to the repo (keep the `.github` folder).
2. Delete the old files: `index.md`, `about.md`, `research.md`, `teaching.md`,
   `publications.md`, `contact.md`, `_config.yml`, and any old `index.html`.
3. Settings -> Pages -> Source: choose **GitHub Actions**.
4. Open the **Actions** tab and watch "Build and deploy website" turn green.

## Updating the site
Replace or edit the matching file in `content/`:

| Site section | File |
|---|---|
| Intro text at the top | `about.tex` |
| Research cards | `research.tex` |
| Equation card | `equation.tex` |
| Technical skills | `skills.tex` |
| Publications | `publications.tex` |
| Experience and education | `experience.tex` |
| Talks and training | `talks.tex` |
| Honors and awards | `honors.tex` |
| Contact | `contact.tex` |

Each file starts with a `%` comment that shows its format. Copy an existing entry and edit it.
Use plain LaTeX only: `\textbf`, `\textit`, `\href{url}{text}`, `itemize`, `description`,
and maths such as `$\nu_\mu$`. Do not paste in your CV's own macros (for example
`\cventry`), because the website does not know them. Paste the text inside them instead.

### Adding a publication
Copy one `\item[...]` block in `publications.tex`, paste it at the top of the list and edit:

    \item[2026] \textbf{Title} \\
    Authors · Journal volume, page \\
    \href{https://doi.org/...}{DOI}

## Other files
- `template.html` holds the design (colours, layout, figures). Rarely needs editing.
- `build.py` turns the `.tex` files into `_site/index.html`.
- Put your photo, CV PDF or other images in the main folder. They are copied to the site.

## Preview on your computer (optional)
Install pandoc, run `python3 build.py`, then open `_site/index.html`.
