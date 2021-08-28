(define (problem Blocks_World) 
 (:domain Blocks_World_Problem) 
(:objects A B C  - block
 T  - table
 ) 
(:init (on A B)(on B C)(on C T)(not (clear B))(not (clear C))(clear A)(clear T)(isblock A)(isblock B)(isblock C)) 
(:goal (and (on A C) (not (clear C)) (clear A) (on B T) (clear B))) 
) 
