; (require [libcl [*]]) for macros.
; (import  [libcl [*]]) for functions.

(defmacro defun [name args doc &rest body]
  (if (is (type doc) hy.models.HyString)  ; hy.models.* は defmacro 内しか使えないみたい。defun ムリ
      `(setv ~name (fn [~@args] ~doc ~@body))
      (do (setv body (+ `(~doc) body))    ; 変数 body は，マクロ展開後残らないので問題ないはず...
                                          ; というかそもそも引数でもある 
          `(setv ~name (fn [~@args] ~@body)))))

(defmacro let [pairs &rest body]
  (setv vars (map first pairs)
        vals (map second pairs))  ; 変数 vars と vals は，マクロ展開後残らないので問題ないはず...
  `((fn [~@vars] ~@body) ~@vals))

; If the values must not invoke twice, use setv.
; e.g. (setf root (Tk)) makes an unexpected result being two windows.
(defmacro setf [&rest args]  ; (setf x 2 y (+ 2 3) z (* 2 3)) -> args: (x 2 y (+ 2 3) z (* 2 3))
  `(do (setv ~@args)
       (last ~args)))    ; (do (setv x 2 y (+ 2 3) z (* 2 3)) (last [x 2 y (+ 2 3) z (* 2 3)]))

(defmacro typep (obj objtype)  ; objtype は，hy.models.* なので，defmacro を使った
  `(is (type ~obj) ~objtype))

(defmacro defparameter (var val)
  `(do (global ~var)
       (setv ~var ~val)))

(setf nil '())

(defun equal (x y)
  (= x y))

; ドットリストには非対応
(defun cons (x xs)
  (+ `(~x) xs))

(defun car (xs)
  (first xs))

(defun cdr (xs)
  (cut xs 1))

(defun caar (xs)
  (first (first xs)))

(defun cadr (xs)
  (second xs))

(defun cdar (xs)
  (cdr (first xs)))

(defun cddr (xs)
  (cdr (cdr xs)))

(defun zerop (x)
  (equal x 0))

(defun 1+ (x)
  (+ x 1))

(defun 1- (x)
  (- x 1))

(defun mod (x y)
  (% x y))
