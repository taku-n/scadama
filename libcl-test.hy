(require [libcl [*]])
(import  [libcl [*]])

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

(assert (equal (let ((two 2)
                     (three 3))
                    (+ two three))
               5)
        "let")

(assert (equal (cons 'foo '(bar baz))
               '(foo bar baz))
        "cons")

(assert (and (equal 'hoge 'hoge)
             (equal '(2 3 5) '(2 3 5))
             (equal '(2 3 5) (cons '2 '(3 5)))
             (equal 2 2)
             (equal 3.14 3.14)
             (equal "hoge" "hoge"))
        "equal")
