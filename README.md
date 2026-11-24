# website

The source of [www.ezp2p.org](https://www.ezp2p.org): a short introduction to Puddle, Pond and Levee, and the wiki for
all of them.

- `src/`: the Jekyll site. `index.html`, `puddle.md`, `pond.md` and `levee.md` are the top pages; `src/wiki/<program>/`
  is the wiki, one folder per program (see `src/wiki/index.md` for how to add a page).
- `.github/workflows/pages.yml` builds `src/` on every pull request and publishes it on every push to `master`.

## Preview locally

With Ruby 3.3 and Bundler:

```sh
cd src
bundle install
bundle exec jekyll serve --livereload
```

Or with Docker:

```sh
docker run --rm -it -p 4000:4000 -v "$PWD/src:/site" -w /site ruby:3.3 \
  sh -c 'bundle install && bundle exec jekyll serve --host 0.0.0.0 --livereload'
```

Then open http://localhost:4000.
