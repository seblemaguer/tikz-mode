<!-- [![MELPA](https://melpa.org/packages/tikz-mode-badge.svg)](https://melpa.org/#/tikz-mode) -->
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# TikZ mode

TikZ mode is a derived mode of TeX-mode from [auctex](https://www.gnu.org/software/auctex/).
The purpose of this mode is to be able to edit TikZ/PGF figure on emacs.
It provides an additional command, `CompilePGF`, which is compiling a standalone PDF which can be vizualized.
This command relies on the `compilePGF.py` scripts which should be in the path.

## Installation

I suggest to use straight to do achieve the installation as the package is not yet available on melpa.

```elisp
  (use-package tikz-mode
    :ensure straight
    :straight (tikz-mode :type git :host github :repo "seblemaguer/tikz-mode"))
```
