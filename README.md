# worksite

[milotek.dev](https://milotek.dev) - Milo Tekchandani's personal site and portfolio.

React + Vite + TypeScript, deployed to GitHub Pages by
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) on every push to `main`.

## Running it

```sh
npm install
npm run dev        # dev server
npm run build      # typecheck, then build to dist/
npm run preview    # serve the built dist/
```

## Where things live

All page copy is data, not markup. To change what the site says, edit a file in
`src/data/` - nothing in `src/pages/` or `src/components/` needs to change.

| Path                 | What it holds                                              |
| -------------------- | ---------------------------------------------------------- |
| `src/data/site.ts`   | Name, contact address, nav items, social links             |
| `src/data/projects.ts` | Lockyn, AutoPet Feeder, EZcals                           |
| `src/data/games.ts`  | EPQ, Schism, the C# collection                             |
| `src/data/art.ts`    | The artwork gallery                                        |
| `src/data/misc.ts`   | Contribution graph, SoundCloud track, CV location          |
| `src/data/types.ts`  | The `Entry` shape shared by projects and games             |
| `src/pages/`         | One file per route                                         |
| `src/components/`    | Layout, backdrop, gallery, icons                           |
| `src/styles/`        | `tokens.css` for the palette and scale, `app.css` for rules |
| `public/`            | Images, `cv.pdf`, `CNAME`                                  |

Adding a project means appending an object to `projects`. Adding a page means a
file in `src/pages/`, a `<Route>` in `src/App.tsx` and an entry in `nav`.

## Deployment notes

- Pages must be set to **build from GitHub Actions**, not from a branch.
  Under a branch source the workflow's artifact is ignored and the raw repo is
  served instead.
- `CNAME` lives in `public/` so Vite copies it into `dist/`. Deleting it drops
  the custom domain on the next deploy.
- The build writes `dist/404.html` as a copy of `index.html`. GitHub Pages has
  no rewrite rules, so this is what stops a deep link like `/projects` from
  404ing before the router loads.

## Assets

Images came from the previous Carrd export and were renamed on the way in;
`public/art/` keeps a display-size copy plus a `_full` original for the
lightbox.
