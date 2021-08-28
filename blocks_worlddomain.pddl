(define (domain Blocks_World_Problem ) 
(:requirements :strips :typing) 
(:types surface
block - surface
table - surface
) 
(:predicates (on ?X - block ?Y - surface) 
(isblock ?X - block) 
(clear ?Y - surface) 
) 
(:action MOVE
:parameters ( ?K - block ?Kfrom - surface ?Kto - surface) 
:precondition (and (clear ?Kto) (clear ?K) (on ?K ?Kfrom) (not (on ?K ?Kto)) (not (= ?K ?Kfrom)) (not (= ?K ?Kto)) (not (= ?Kto ?Kfrom)) )
:effect (and (not (on ?K ?Kfrom)) (on ?K ?Kto) (when (isblock ?Kto) (not (clear ?Kto))) (when (isblock ?Kfrom) (clear ?Kfrom)))
) 
) 
