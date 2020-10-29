; (require [libcl [*]]) for macros.
; (import [libcl [*]])  for functions.

(defmacro defun [name args doc &rest body]
  (if (is (type doc) hy.models.HyString)
      `(setv ~name (fn [~@args] ~doc ~@body))
      (do (setv body (+ `(~doc) body))  ; 変数 body は，マクロ展開後残らないので問題ないはず...
                                        ; というかそもそも引数でもある 
          `(setv ~name (fn [~@args] ~@body)))))

(defmacro let [pairs &rest body]
  (setv vars (map first pairs)
        vals (map second pairs))  ; 変数 vars と vals は，マクロ展開後残らないので問題ないはず...
  `((fn [~@vars] ~@body) ~@vals))

; ドット対には非対応
(defun cons (x xs)
  (+ `(~x) xs))

(defun equal (x y)
  (= x y))
