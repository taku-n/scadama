; (require [libcl [*]])

(defmacro defun [name args doc &rest body]
  (if (is (type doc) hy.models.HyString)
      `(setv ~name (fn [~@args] ~doc ~@body))
      (do (setv body (+ `(~doc) body))
          `(setv ~name (fn [~@args] ~@body)))))
