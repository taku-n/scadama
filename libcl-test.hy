; $ hy libcl-test.hy

(require [libcl [*]])
(import  [libcl [*]])

; defun

(defun add (x y)
  (+ x y))

(assert (equal (add 2 3)
               5)
        "defun without a document.")

(defun mul (x y)
  "Multiply x by y. x に y を掛ける。"
  (* x y))

(assert (equal (mul 2 3)
               6)
        "defun with a document.")

; let

(assert (equal (let ((two 2)
                     (three 3))
                    (+ two three))
               5)
        "let")

; setf

(setf x 2 y 3 z 5)

(assert (equal x 2)
        "x set by setf")
(assert (equal y 3)
        "y set by setf")
(assert (equal z 5)
        "z set by setf")

; typep

(assert (typep '42      hy.models.HyInteger))
(assert (typep '3.14    hy.models.HyFloat))
(assert (typep '"hoge"  hy.models.HyString))
(assert (typep '(2 3 5) hy.models.HyExpression))

; defparameter

(defun set-global-variable ()
  (defparameter *x* 41))
(set-global-variable)

(defun update-global-variable ()
  (defparameter *x* 42))
(update-global-variable)

(assert (equal *x* 42)
        "defparameter")

; equal

(assert (and (equal 'hoge 'hoge)
             (equal '(2 3 5) '(2 3 5))
             (equal '(2 3 5) (cons '2 '(3 5)))
             (equal 2 2)
             (equal 3.14 3.14)
             (equal "hoge" "hoge"))
        "equal")

; cons

(assert (equal (cons 'foo '(bar baz))
               '(foo bar baz))
        "cons")
(assert (equal (cons '42 '())
               '(42))
        "cons with empty")

; car

(assert (equal (car '(2 3 5 7))
               2)
        "car")

; cdr

(assert (equal (cdr '(2 3 5 7))
               '(3 5 7))
        "cdr")

; caar

(assert (equal (caar '((1 2 3) 20 30))
               1)
        "caar")

; cadr

(assert (equal (cadr '(2 3 5 7))
               3)
        "cadr")

; cdar

(assert (equal (cdar '((1 2 3) 20 30))
               '(2 3))
        "cdar")

; cddr

(assert (equal (cddr '(2 3 5 7))
               '(5 7))
        "cddr")

; zerop

(assert (zerop 0)
        "zerop")

; 1+

(assert (equal (1+ 41)
               42)
        "1+")

; 1-

(assert (equal (1- 43)
               42)
        "1-")

; mod

(assert (equal (mod 42 7)
               0)
        "mod")
