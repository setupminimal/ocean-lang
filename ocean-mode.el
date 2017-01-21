;;; ocean-mode.el --- major mode for editing Ocean and similar languages

;; Copyright (C) 2017 Daroc Alden

;; Author:     Daroc Alden
;; Maintainer: setupminimal@gmail.com
;; Created:    2017-01-21
;; Keywords:   ocean languages

;; This code is licenced under the GPLv2, or any later version, at your option.

;;; Indentation

(defun oc-indent-line ()
  "Indent current line as Ocean code"
  (interactive)
  (beginning-of-line)
  (if (bobp) ; Start of Buffer
      (indent-line-to 0)
    (let ((not-indented t) cur-indent)
      (if (looking-at "^[ \t]*\\(return\\|else\\)") ; We should dedent
	  (progn
	    (save-excursion
	      (forward-line -1)
	      (setq cur-indent (- (current-indentation) default-tab-width)))
	    (if (< cur-indent 0)
		(setq cur-indent 0)))
	(save-excursion
	  (while not-indented ; Iterate backwards until we find a hint
	    (forward-line -1)
	    (if (looking-at "^[ \t]*\\(return\\)")
		(progn
		  (setq cur-indent (current-indentation))
		  (setq not-indented nil))
	      (if (looking-at "^[ \t]*.*?\\:")
		  (progn
		    (setq cur-indent (+ (current-indentation) default-tab-width))
		    (setq not-indented nil))
		(if (bobp)
		    (setq not-indented nil)))))))
      (if cur-indent
	  (indent-line-to cur-indent)
	(indent-line-to 0)))))

;; MODE

(require 'generic-x)

(define-generic-mode
    'ocean-mode
  '("//" ("/*" . "*/"))
  '("if" "else" "for" "while" "return")
  '(
    ("^[ \t]*\\(.*\\) \\$" 1 font-lock-function-name-face) ; Function application
    (".*? \\(.*\\) ←" (1 font-lock-function-name-face)) ; Function declaration
    ("\\(\\#.*\\)$" 1 font-lock-preprocessor-face) ; #includes, #defines, etc.
    ("\\(int\\|float\\|double\\|void\\|short\\|char\\|byte\\|long\\)" 
     (1 font-lock-type-face)); Types
    ("\\(int\\|float\\|double\\|short\\|char\\|byte\\|long\\) \\([^ ]*\\)" 2 font-lock-variable-name-face)
    ("\\([[:upper:]]+\\)" 1 font-lock-constant-face)
   )
  '("\\.ca$" "\\.oc$" "\\.ocean$")
  (list
   (function
    (lambda () 
      (set 
       (make-local-variable 'indent-line-function) 
       'oc-indent-line))))
  "A mode to color Ocean files"
)

;(defun ocean-mode ()
;  "Major mode for editing Ocean code"
;  (interactive)
;  (kill-all-local-variables)
;  (set-syntax-table oc-mode-syntax-table)
;  (use-local-map oc-mode-map)
;  (set (make-local-variable 'font-lock-defaults) '(ocean-font-lock-keywords))
;  (set (make-local-variable 'indent-line-function) 'oc-indent-line)
;  (setq major-mode 'ocean-mode)
;  (setq mode-name "Ocean")
;  (run-hooks 'oc-mode-hook))

(provide 'ocean-mode)
