;;; tikz-mode.el ---  Mode to edit tikz file -*- lexical-binding: t; coding: utf-8 -*-

;; Copyright (C)  5 May 2020
;;

;; Author: Sébastien Le Maguer <sebastien.lemaguer@adaptcentre.ie>

;; Package-Requires: ((emacs "25.2") (auctex "11.87"))
;; Keywords:
;; Homepage:

;; tikz-mode is free software; you can redistribute it and/or modify it
;; under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 3, or (at your option)
;; any later version.
;;
;; tikz-mode is distributed in the hope that it will be useful, but WITHOUT
;; ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
;; or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
;; License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with tikz-mode.  If not, see http://www.gnu.org/licenses.

;;; Commentary:

;;; Code:

(defun auctex-compilePGF-setup ()
  "Add LatexMk command to TeX-command-list."
  (setq-default TeX-file-extensions (append '("pgf" "tikz") TeX-file-extensions)
                TeX-command-list  (cons
                                   '("CompilePGF" "compilePGF %t"
                                     TeX-run-command t (tikz-mode)
                                     :help "Run compilePGF to compile TIKZ/PGF like ktikz")
                                   TeX-command-list)))

;; Link tikz-mode and auctex
(define-derived-mode tikz-mode latex-mode "Tikz/PGF"
  "PGF/Tikz dedicated mode"
  (setq TeX-sentinel-default-function "CompilePGF"))

;; Execute global configuration
(auctex-compilePGF-setup)
(add-to-list 'auto-mode-alist '("\\.\\(pgf\\|tikz\\)" . tikz-mode))

(provide 'tikz-mode)

;;; tikz-mode.el ends here
