# Continuous Interaction Diffusion

**Paper:** *Continuous Interaction Diffusion: A Diffusion-Native Runtime for Asynchronous Tool-Augmented Reasoning*

This repository contains the LaTeX source for the CID concept paper. CID proposes a model--runtime co-designed architecture in which diffusion-language-model cognition, external perception, and user-visible generation evolve concurrently.

The current preprint focuses on read-only tools and formalizes:

- a three-channel architecture for protected facts, continuous thought, and displayed text;
- a Typed Cognitive Tensor for latent reasoning, source links, symbolic anchors, and local diffusion state;
- persistent perceptual bindings that replace one-shot tool calls;
- distinct policies for re-projecting static results and refreshing changing sources;
- asynchronous runtime transitions, training objectives, and a falsifiable evaluation protocol.

The manuscript is currently an architectural proposal and does not claim experimental results.

## Build

```bash
make build
```

The PDF is written to `build/paper.pdf`.

For structural and PDF validation:

```bash
make check
```

For an arXiv-ready source bundle:

```bash
make dist
```

## Repository layout

```text
paper.tex                 Root document
metadata.tex              Title and author metadata
sections/                  Manuscript sections
figures/                   TikZ and figure sources
config/                    LaTeX packages and commands
references.bib             Bibliography
scripts/                   Build and validation utilities
```

## Status

- Repository visibility: public
- Public PDF preview: enabled through GitHub Pages
- Scope of v1: language models and read-only external sources

## License

Repository infrastructure is derived from `fwerkor/latex-paper-template`. See `LICENSE` for the current license terms.
